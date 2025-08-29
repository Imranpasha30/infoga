import dns.resolver
from typing import Dict

class DMARCService:
    def __init__(self):
        self.resolver = dns.resolver.Resolver()
    
    def check_dmarc(self, domain: str) -> Dict[str, any]:
        """Check DMARC record for domain"""
        try:
            dmarc_domain = f"_dmarc.{domain}"
            txt_records = self.resolver.resolve(dmarc_domain, 'TXT')
            
            for record in txt_records:
                record_str = str(record).strip('"')
                if record_str.startswith('v=DMARC1'):
                    return {
                        'valid': True,
                        'record': record_str,
                        'policy': self._extract_policy(record_str),
                        'details': 'DMARC record found'
                    }
            
            return {
                'valid': False,
                'record': None,
                'policy': None,
                'details': 'No DMARC record found'
            }
            
        except Exception as e:
            return {
                'valid': False,
                'record': None,
                'policy': None,
                'details': f'DMARC check failed: {str(e)}'
            }
    
    def _extract_policy(self, dmarc_record: str) -> str:
        """Extract policy from DMARC record"""
        import re
        policy_match = re.search(r'p=([^;]+)', dmarc_record)
        return policy_match.group(1) if policy_match else 'unknown'
