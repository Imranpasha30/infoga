from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

class EmailDiscoveryRequest(BaseModel):
    domain: str
    max_results: int = 100
    search_engines: List[str] = ["google", "bing", "pgp"]

class DiscoveredEmail(BaseModel):
    email: EmailStr
    source: str  # "google", "bing", "pgp", etc.
    context: Optional[str] = None  # Where it was found

class EmailDiscoveryResponse(BaseModel):
    domain: str
    total_found: int
    emails: List[DiscoveredEmail]
    sources_used: List[str]
    discovery_timestamp: datetime
