import dkim
from typing import Dict
from app.models.email_models import AuthStatus

class DKIMService:
    def verify_dkim(self, email_content: str) -> Dict[str, any]:
        """Verify DKIM signature"""
        try:
            # Convert string to bytes
            email_bytes = email_content.encode('utf-8')
            
            # Verify DKIM signature
            is_valid = dkim.verify(email_bytes)
            
            return {
                'valid': is_valid,
                'status': AuthStatus.PASS if is_valid else AuthStatus.FAIL,
                'details': 'DKIM signature valid' if is_valid else 'DKIM signature invalid or missing'
            }
        except Exception as e:
            return {
                'valid': False,
                'status': AuthStatus.FAIL,
                'details': f'DKIM verification failed: {str(e)}'
            }
