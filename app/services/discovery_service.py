import requests
import re
from typing import List, Dict
from app.models.discovery_models import DiscoveredEmail

class EmailDiscoveryService:
    def __init__(self):
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': self.user_agent})
    
    def discover_emails(self, domain: str, sources: List[str]) -> List[DiscoveredEmail]:
        """Main discovery method"""
        all_emails = []
        
        for source in sources:
            try:
                if source == "google":
                    emails = self.search_google(domain)
                    all_emails.extend(emails)
                elif source == "bing":
                    emails = self.search_bing(domain)
                    all_emails.extend(emails)
                elif source == "pgp":
                    emails = self.search_pgp(domain)
                    all_emails.extend(emails)
            except Exception as e:
                print(f"Error searching {source}: {e}")
        
        # Remove duplicates
        unique_emails = {}
        for email in all_emails:
            if email.email not in unique_emails:
                unique_emails[email.email] = email
        
        return list(unique_emails.values())
    
    def search_google(self, domain: str) -> List[DiscoveredEmail]:
        """Search Google for emails"""
        emails = []
        try:
            # Search for emails with @ symbol + domain
            query = f'site:{domain} OR "@{domain}"'
            url = f"https://www.google.com/search?q={query}&num=50"
            
            response = self.session.get(url, timeout=10)
            
            # Extract emails from response
            email_pattern = rf'\b[\w\.-]+@[\w\.-]*{re.escape(domain)}\b'
            found_emails = re.findall(email_pattern, response.text, re.IGNORECASE)
            
            for email in set(found_emails):  # Remove duplicates
                if self.is_valid_email(email):
                    emails.append(DiscoveredEmail(
                        email=email.lower(),
                        source="google",
                        context="Google search results"
                    ))
        except Exception as e:
            print(f"Google search error: {e}")
        
        return emails
    
    def search_bing(self, domain: str) -> List[DiscoveredEmail]:
        """Search Bing for emails"""
        emails = []
        try:
            query = f'site:{domain} OR "@{domain}"'
            url = f"https://www.bing.com/search?q={query}&count=50"
            
            response = self.session.get(url, timeout=10)
            email_pattern = rf'\b[\w\.-]+@[\w\.-]*{re.escape(domain)}\b'
            
            found_emails = re.findall(email_pattern, response.text, re.IGNORECASE)
            
            for email in set(found_emails):
                if self.is_valid_email(email):
                    emails.append(DiscoveredEmail(
                        email=email.lower(),
                        source="bing",
                        context="Bing search results"
                    ))
        except Exception as e:
            print(f"Bing search error: {e}")
        
        return emails
    
    def search_pgp(self, domain: str) -> List[DiscoveredEmail]:
        """Search PGP servers for emails"""
        emails = []
        try:
            url = f"https://pgp.mit.edu/pks/lookup?search={domain}&op=index"
            response = self.session.get(url, timeout=10)
            
            email_pattern = rf'\b[\w\.-]+@[\w\.-]*{re.escape(domain)}\b'
            found_emails = re.findall(email_pattern, response.text, re.IGNORECASE)
            
            for email in set(found_emails):
                if self.is_valid_email(email):
                    emails.append(DiscoveredEmail(
                        email=email.lower(),
                        source="pgp",
                        context="PGP key server"
                    ))
        except Exception as e:
            print(f"PGP search error: {e}")
        
        return emails
    
    def is_valid_email(self, email: str) -> bool:
        """Basic email validation"""
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(email_regex, email) is not None
