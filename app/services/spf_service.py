import dns.resolver
import ipaddress
from typing import Dict, Optional

class SPFService:
    def __init__(self):
        self.resolver = dns.resolver.Resolver()
    
    def check_spf(self, sender_ip: str, sender_domain: str) -> Dict[str, any]:
        """Check SPF record for sender domain"""
        try:
            # Query TXT records for SPF
            txt_records = self.resolver.resolve(sender_domain, 'TXT')
            spf_record = None
            
            for record in txt_records:
                record_str = str(record).strip('"')
                if record_str.startswith('v=spf1'):
                    spf_record = record_str
                    break
            
            if not spf_record:
                return {
                    'valid': False,
                    'result': 'No SPF record found',
                    'record': None
                }
            
            # Basic SPF validation (you can expand this)
            if 'include:' in spf_record or 'a:' in spf_record or 'mx:' in spf_record:
                return {
                    'valid': True,
                    'result': 'SPF record found and appears valid',
                    'record': spf_record
                }
            
            return {
                'valid': None,
                'result': 'SPF record found but requires detailed analysis',
                'record': spf_record
            }
            
        except Exception as e:
            return {
                'valid': False,
                'result': f'SPF check failed: {str(e)}',
                'record': None
            }
