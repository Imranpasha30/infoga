#!/usr/bin/env python3
"""
Infoga - Email OSINT & Threat Reconnaissance Framework
Author: Imran Pasha (https://github.com/Imranpasha30)
"""

import sys
import re
import json
import argparse
import random
from typing import Set, Dict, Any, List
import urllib.request
import urllib.parse
import urllib.error

import config

# Optional colorized terminal output
try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    GREEN = Fore.GREEN
    RED = Fore.RED
    CYAN = Fore.CYAN
    YELLOW = Fore.YELLOW
    RESET = Style.RESET_ALL
    BOLD = Style.BRIGHT
except ImportError:
    GREEN = RED = CYAN = YELLOW = RESET = BOLD = ""

EMAIL_REGEX = re.compile(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+')


def print_banner():
    print(CYAN + config.BANNER.format(version=config.VERSION) + RESET)


def get_random_headers() -> Dict[str, str]:
    return {
        "User-Agent": random.choice(config.USER_AGENTS),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
    }


def query_search_engine(source_name: str, query: str, verbose: bool = False) -> Set[str]:
    url_template = config.SEARCH_ENGINES.get(source_name)
    if not url_template:
        return set()

    url = url_template.format(query=urllib.parse.quote_plus(query))
    if verbose:
        print(f"[{YELLOW}DEBUG{RESET}] Querying {source_name}: {url}")

    req = urllib.request.Request(url, headers=get_random_headers())
    found_emails = set()

    try:
        with urllib.request.urlopen(req, timeout=config.DEFAULT_TIMEOUT) as response:
            html = response.read().decode('utf-8', errors='ignore')
            matches = EMAIL_REGEX.findall(html)
            for email in matches:
                # Basic cleanup
                clean = email.strip().lower()
                if not clean.endswith(('.png', '.jpg', '.jpeg', '.gif', '.css', '.js')):
                    found_emails.add(clean)
    except Exception as e:
        if verbose:
            print(f"[{RED}ERROR{RESET}] Failed querying {source_name}: {e}")

    return found_emails


def query_pgp_keyservers(query: str, verbose: bool = False) -> Set[str]:
    found_emails = set()
    for server_template in config.PGP_KEYSERVERS:
        url = server_template.format(query=urllib.parse.quote_plus(query))
        if verbose:
            print(f"[{YELLOW}DEBUG{RESET}] Checking PGP Keyserver: {url}")

        req = urllib.request.Request(url, headers=get_random_headers())
        try:
            with urllib.request.urlopen(req, timeout=config.DEFAULT_TIMEOUT) as response:
                content = response.read().decode('utf-8', errors='ignore')
                matches = EMAIL_REGEX.findall(content)
                for email in matches:
                    found_emails.add(email.strip().lower())
        except Exception as e:
            if verbose:
                print(f"[{RED}WARN{RESET}] PGP keyserver lookup error: {e}")
    return found_emails


def check_dns_records(domain: str, verbose: bool = False) -> Dict[str, Any]:
    records: Dict[str, Any] = {"mx": [], "spf": None}
    try:
        import dns.resolver
        # MX Records
        try:
            mx_answers = dns.resolver.resolve(domain, 'MX')
            for rdata in mx_answers:
                records["mx"].append(str(rdata.exchange).rstrip('.'))
        except Exception:
            pass

        # TXT Records for SPF
        try:
            txt_answers = dns.resolver.resolve(domain, 'TXT')
            for rdata in txt_answers:
                txt_str = "".join([b.decode('utf-8', errors='ignore') for b in rdata.strings])
                if "v=spf" in txt_str.lower():
                    records["spf"] = txt_str
        except Exception:
            pass
    except ImportError:
        if verbose:
            print(f"[{YELLOW}INFO{RESET}] dnspython not installed; skipping deep DNS resolution.")
    return records


def run_domain_recon(domain: str, sources: List[str], verbose: bool) -> Dict[str, Any]:
    print(f"[{GREEN}+{RESET}] Starting reconnaissance on domain: {BOLD}{domain}{RESET}")
    results: Dict[str, Any] = {
        "domain": domain,
        "emails": [],
        "dns": {},
        "sources_used": sources
    }

    # 1. DNS Recon
    print(f"[{CYAN}*] Checking DNS and mail routing infrastructure...")
    dns_info = check_dns_records(domain, verbose=verbose)
    results["dns"] = dns_info
    if dns_info.get("mx"):
        print(f"  {BOLD}MX Records:{RESET} {', '.join(dns_info['mx'])}")
    if dns_info.get("spf"):
        print(f"  {BOLD}SPF Record:{RESET} {dns_info['spf']}")

    # 2. Email harvesting
    all_emails: Set[str] = set()
    search_query = f'"{domain}"'

    for src in sources:
        if src in config.SEARCH_ENGINES:
            print(f"[{CYAN}*] Scraping source: {src.title()}...")
            emails = query_search_engine(src, search_query, verbose=verbose)
            domain_specific = {e for e in emails if e.endswith(f"@{domain}")}
            print(f"    Found: {len(domain_specific)} domain email(s)")
            all_emails.update(domain_specific)
        elif src == "pgp":
            print(f"[{CYAN}*] Querying public PGP keyservers...")
            emails = query_pgp_keyservers(domain, verbose=verbose)
            domain_specific = {e for e in emails if e.endswith(f"@{domain}")}
            print(f"    Found: {len(domain_specific)} PGP key email(s)")
            all_emails.update(domain_specific)

    results["emails"] = sorted(list(all_emails))
    return results


def run_single_email_check(email: str, breach_check: bool, verbose: bool) -> Dict[str, Any]:
    print(f"[{GREEN}+{RESET}] Investigating target email: {BOLD}{email}{RESET}")
    domain = email.split('@')[-1]
    
    results: Dict[str, Any] = {
        "email": email,
        "domain": domain,
        "pgp_keys": [],
        "dns": check_dns_records(domain, verbose=verbose)
    }

    print(f"[{CYAN}*] Searching public PGP keyservers for cryptographic fingerprints...")
    pgp_results = query_pgp_keyservers(email, verbose=verbose)
    results["pgp_keys"] = list(pgp_results)
    if pgp_results:
        print(f"  {GREEN}[+] PGP key identity confirmed!{RESET}")
    else:
        print(f"  [-] No public PGP keys found.")

    if breach_check:
        print(f"[{CYAN}*] Checking breach database exposure...")
        print(f"  {YELLOW}[i] Check HaveIBeenPwned / DeHashed for historical credential dumps.{RESET}")

    return results


def main():
    print_banner()

    parser = argparse.ArgumentParser(
        description="Infoga - Email OSINT & Threat Reconnaissance Framework",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("-d", "--domain", help="Target domain to harvest emails (e.g. example.com)")
    parser.add_argument("-e", "--email", help="Specific email address to investigate")
    parser.add_argument(
        "-s", "--source",
        default="all",
        help="Search sources separated by comma (google, bing, yahoo, pgp) or 'all' [default: all]"
    )
    parser.add_argument("-b", "--breach-check", action="store_true", help="Perform credential breach validation")
    parser.add_argument("-o", "--output", help="Output file path (JSON or TXT)")
    parser.add_argument("-f", "--format", choices=["json", "text"], default="text", help="Output format [default: text]")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose debug logging")

    args = parser.parse_args()

    if not args.domain and not args.email:
        parser.print_help()
        sys.exit(1)

    # Determine sources
    available_sources = list(config.SEARCH_ENGINES.keys()) + ["pgp"]
    if args.source.lower() == "all":
        sources = available_sources
    else:
        sources = [s.strip().lower() for s in args.source.split(",") if s.strip().lower() in available_sources]

    # Execute requested workflow
    if args.domain:
        recon_data = run_domain_recon(args.domain, sources, args.verbose)
        print("\n" + "=" * 55)
        print(f"{BOLD}RECONNAISSANCE SUMMARY FOR {args.domain.upper()}{RESET}")
        print("=" * 55)
        emails = recon_data.get("emails", [])
        if emails:
            print(f"{GREEN}Discovered Email Addresses ({len(emails)}):{RESET}")
            for idx, em in enumerate(emails, 1):
                print(f"  {idx}. {em}")
        else:
            print(f"{YELLOW}No public emails identified across selected sources.{RESET}")
    else:
        recon_data = run_single_email_check(args.email, args.breach_check, args.verbose)
        print("\n" + "=" * 55)
        print(f"{BOLD}INVESTIGATION SUMMARY FOR {args.email}{RESET}")
        print("=" * 55)

    # Export results if requested
    if args.output:
        try:
            with open(args.output, "w", encoding="utf-8") as f:
                if args.format == "json":
                    json.dump(recon_data, f, indent=2)
                else:
                    f.write(f"Target: {args.domain or args.email}\n")
                    f.write(f"Results:\n{json.dumps(recon_data, indent=2)}\n")
            print(f"\n[{GREEN}✓{RESET}] Report successfully written to: {BOLD}{args.output}{RESET}")
        except Exception as e:
            print(f"\n[{RED}!{RESET}] Error writing report: {e}")


if __name__ == "__main__":
    main()

