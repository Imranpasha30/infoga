import email
import re
from typing import Dict, List
from app.models.email_models import EmailHeaders  # Fixed import

class ModernEmailParser:
    def __init__(self, email_content: str):
        self.email_content = email_content
        self.message = email.message_from_string(email_content)
    
    def extract_headers(self) -> EmailHeaders:
        """Extract all relevant headers for authentication"""
        return EmailHeaders(
            received=self.message.get_all('Received') or [],
            return_path=self.message.get('Return-Path'),
            authentication_results=self.message.get('Authentication-Results'),
            dkim_signature=self.message.get('DKIM-Signature'),
            message_id=self.message.get('Message-ID'),
            date=self.message.get('Date'),
            sender=self.message.get('From')  # Added sender field
        )
    
    def extract_sender_info(self) -> Dict[str, str]:
        """Extract sender email and domain"""
        from_header = self.message.get('From', '')
        email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', from_header)
        
        if email_match:
            sender_email = email_match.group(0)
            sender_domain = sender_email.split('@')[1]
            return {
                'email': sender_email,
                'domain': sender_domain
            }
        return {'email': None, 'domain': None}
    
    def get_body_content(self) -> str:
        """Extract email body for analysis"""
        if self.message.is_multipart():
            for part in self.message.walk():
                if part.get_content_type() == "text/plain":
                    return part.get_payload(decode=True).decode('utf-8', errors='ignore')
        else:
            return self.message.get_payload(decode=True).decode('utf-8', errors='ignore')
        return ""
