# 🔍 ReconMail — Email OSINT & Threat Reconnaissance Framework

[![Python](https://img.shields.io/badge/Python-3.9%20%7C%203.10%20%7C%203.11%20%7C%203.12%20%7C%203.14-blue?logo=python&logoColor=white)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Cybersecurity](https://img.shields.io/badge/Security-OSINT%20%26%20Recon-red)](https://github.com/Imranpasha30/infoga)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/Imranpasha30/infoga/pulls)

> **ReconMail** is a lightweight, modular Open-Source Intelligence (OSINT) and Reconnaissance framework designed for security operations analysts (SOC), penetration testers, and threat hunters. It automates the discovery, extraction, validation, and analysis of email addresses, mail server configurations, DNS security records (MX, SPF), and breach footprints across public sources with both an interactive Web UI and a high-speed CLI.

---

## 📑 Table of Contents

- [Key Features](#-key-features)
- [Web UI Dashboard & Interactive Mode](#-interactive-web-ui-dashboard)
- [Architecture & Data Flow](#-architecture--data-flow)
- [Installation & Setup](#-installation--setup)
- [Usage & Examples](#-usage--examples)
  - [One-Click Interactive Dashboard](#one-click-interactive-web-dashboard)
  - [Domain Reconnaissance (CLI)](#1-domain-email-reconnaissance-cli)
  - [Targeted Email Investigation (CLI)](#2-targeted-email-investigation-cli)
  - [Exporting Reports](#3-exporting-results)
- [Supported Intelligence Sources](#-supported-intelligence-sources)
- [Role in SOC & Incident Response](#-role-in-soc--incident-response)
- [Project Structure](#-project-structure)
- [Contributing](#-contributing)
- [Disclaimer & License](#-disclaimer--license)

---

## ⚡ Key Features

* 🖥️ **Interactive Cyber Web UI:** Real-time dark-mode security console on port `5050` with live status terminal, single-click email copying, and DNS inspection cards.
* 🔎 **Multi-Engine Email Harvesting:** Scrapes and extracts corporate and personal email addresses from search engines (Google, Bing, Yahoo, DuckDuckGo) without requiring paid API keys.
* 🔑 **PGP Key Server Reconnaissance:** Queries Ubuntu HKP and public PGP keyservers to uncover real identities, employee names, and cryptographic keys tied to the target.
* 🛡️ **DNS & Mail Infrastructure Profiling:** Resolves and validates MX (Mail Exchange), SPF (Sender Policy Framework), and anti-spoofing postures.
* 🚨 **Breach & Exposure Checking:** Verifies if harvested email addresses have appeared in known public credential breaches and dump repositories.
* 📊 **Structured Multi-Format Exports:** Output findings directly to clean console tables, structured **JSON**, delimited **CSV**, or formatted PDF printouts.
* 🚀 **One-Click Windows Launchers:** Includes double-clickable `run_reconmail.bat` and PowerShell `start_reconmail_ui.ps1` for instant interview and demonstration setups.

---

## 🖥️ Interactive Web UI Dashboard

ReconMail features a built-in lightweight REST API server and dashboard.
To launch the interactive dashboard:

```bash
# Windows Batch (Double-click or run from terminal)
run_reconmail.bat

# Or PowerShell:
.\start_reconmail_ui.ps1

# Or via Python directly:
py app.py
```

Then navigate to `http://localhost:5050` in any web browser to access:
* Live Domain OSINT & Single Email investigation panels
* Real-time activity log terminal
* Instant CSV & JSON report export buttons
* One-click clipboard copy for discovered corporate emails

---

## 🏗️ Architecture & Data Flow

```text
       Target Domain / Email Target
                    │
                    ▼
       ┌────────────────────────┐
       │ ReconMail Core Engine  │
       └────────────┬───────────┘
                    │
     ┌──────────────┼──────────────┐
     │              │              │
     ▼              ▼              ▼
┌──────────┐  ┌──────────┐  ┌─────────────┐
│  Search  │  │ PGP Key  │  │ DNS Records │
│ Engines  │  │ Servers  │  │ (MX / SPF)  │
└────┬─────┘  └────┬─────┘  └──────┬──────┘
     │              │              │
     └──────────────┼──────────────┘
                    │
                    ▼
       ┌────────────────────────┐
       │  Parser & Deduplicator │
       └────────────┬───────────┘
                    │
                    ▼
       ┌────────────────────────┐
       │ Threat Intelligence    │
       │   & Breach Analysis    │
       └────────────┬───────────┘
                    │
                    ▼
       ┌────────────────────────┐
       │ Outputs: CLI / JSON /  │
       │   CSV / Web Dashboard  │
       └────────────────────────┘
```

---

## 🚀 Installation & Setup

### Prerequisites
* Python 3.9 or higher
* Git

### Step-by-Step Installation

```bash
# 1. Clone the repository
git clone https://github.com/Imranpasha30/infoga.git

# 2. Navigate to the project directory
cd infoga

# 3. Create and activate a virtual environment (Recommended)
python -m venv venv
# On Linux / macOS:
source venv/bin/activate
# On Windows (PowerShell):
.\venv\Scripts\Activate.ps1

# 4. Install dependencies
pip install -r requirements.txt
```

---

## 💻 Usage & Examples

### One-Click Interactive Web Dashboard
```bash
py app.py
# Opens dashboard at http://localhost:5050
```

### 1. Domain Email Reconnaissance (CLI)
Harvest all public email addresses associated with a target corporate domain across all intelligence sources:

```bash
py run.py --domain example.com --source all
```

To target specific search engines:
```bash
py run.py --domain targetcompany.com --source google,bing,pgp -v
```

### 2. Targeted Email Investigation (CLI)
Inspect a single email address for owner details, PGP keys, mail server reputation, and breach history:

```bash
py run.py --email analyst@targetcompany.com --breach-check
```

### 3. Exporting Results
Save parsed findings directly to JSON or text for automated pipelines:

```bash
py run.py --domain example.com --output reports/example_recon.json --format json
```

### Command-Line Arguments Reference

| Flag | Long Flag | Description | Default |
| :--- | :--- | :--- | :--- |
| `-d` | `--domain` | Target domain to profile (e.g. `company.com`) | `None` |
| `-e` | `--email` | Specific email address to investigate | `None` |
| `-s` | `--source` | Data sources: `all`, `google`, `bing`, `yahoo`, `pgp` | `all` |
| `-b` | `--breach-check` | Query breach databases for credential exposure | `False` |
| `-o` | `--output` | Destination file path for saved results | `None` |
| `-f` | `--format` | Output format: `json`, `text` | `text` |
| `-v` | `--verbose` | Enable detailed debug output and request logs | `False` |

---

## 🌐 Supported Intelligence Sources

| Source | Method | Data Gathered |
| :--- | :--- | :--- |
| **Google Search** | Dorking & HTML Scraping | Indexed public employee contact emails, press releases |
| **Bing & Yahoo** | Web scraping & SERP parsing | Secondary public mentions and directory listings |
| **Ubuntu / MIT PGP Keyservers** | HKP / HTTP Key Query | Developer emails, verified full names, PGP key IDs |
| **DNS Resolvers** | DNS MX / TXT queries | Inbound mail gateways, mail security providers (Proofpoint, M365) |
| **HaveIBeenPwned / LeakFeeds** | API / Open Dumps | Historical breach involvement and exposed data types |

---

## 🛡️ Role in SOC & Incident Response

While ReconMail is an essential reconnaissance tool, it plays a vital defensive role in **Security Operations (SOC)** and **Threat Hunting**:

1. **Phishing Campaign Analysis:** When malicious emails target an organization, SOC analysts use ReconMail to determine how the attacker harvested internal employee addresses (evaluating the company's external digital footprint).
2. **Executive & VIP Attack Surface Management:** Identify exposed personal and professional email addresses of C-level executives that may be targeted for Business Email Compromise (BEC) and spear-phishing.
3. **Third-Party Vendor Risk Assessment:** Audit supplier domains for insecure mail configurations, missing SPF/DMARC enforcement, or leaked employee credentials.

---

## 📁 Project Structure

```text
ReconMail/
├── .gitignore              # Git ignore rules for Python / IDE artifacts
├── README.md               # Project documentation & operational guide
├── requirements.txt        # Python dependency manifest
├── config.py               # Engine configuration, request headers, API endpoints
├── run.py                  # CLI entry point and execution coordinator
├── app.py                  # Local REST API & Web Server (Port 5050)
├── run_reconmail.bat       # Windows double-click launcher
├── start_reconmail_ui.ps1  # PowerShell launcher script
└── web/
    └── index.html          # Interactive Cyber-themed OSINT Dashboard UI
```

---

## 🤝 Contributing

Contributions, bug reports, and feature suggestions are welcome!

1. Fork the Project (`https://github.com/Imranpasha30/infoga/fork`)
2. Create your Feature Branch (`git checkout -b feature/NewSource`)
3. Commit your Changes (`git commit -m 'Add DuckDuckGo search provider'`)
4. Push to the Branch (`git push origin feature/NewSource`)
5. Open a Pull Request

---

## ⚖️ Disclaimer & License

> **⚠️ Disclaimer:** ReconMail is developed exclusively for educational purposes, authorized security testing, and defensive threat analysis. Gathering information without proper consent may violate applicable terms of service and local legal statutes. The author assumes no liability for unauthorized or illicit usage.

Distributed under the **MIT License**. See `LICENSE` for more information.

---

<p align="center">
  <b>Developed & Maintained by <a href="https://github.com/Imranpasha30">Imran Pasha</a></b>
</p>

