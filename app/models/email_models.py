from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional, Dict
from datetime import datetime
from enum import Enum

class AuthStatus(str, Enum):
    PASS = "pass"
    FAIL = "fail"
    NEUTRAL = "neutral"
    UNKNOWN = "unknown"

class EmailHeaders(BaseModel):
    received: List[str] = Field(default=[], description="Received headers")
    return_path: Optional[str] = Field(None, description="Return-Path header")
    authentication_results: Optional[str] = Field(None, description="Authentication-Results header")
    dkim_signature: Optional[str] = Field(None, description="DKIM-Signature header")
    message_id: Optional[str] = Field(None, description="Message-ID header")
    date: Optional[str] = Field(None, description="Date header")
    sender: Optional[str] = Field(None, description="From header")

class SPFResult(BaseModel):
    status: AuthStatus = AuthStatus.UNKNOWN
    record: Optional[str] = None
    details: Optional[str] = None
    sender_ip: Optional[str] = None

class DKIMResult(BaseModel):
    status: AuthStatus = AuthStatus.UNKNOWN
    domain: Optional[str] = None
    selector: Optional[str] = None
    details: Optional[str] = None

class DMARCResult(BaseModel):
    status: AuthStatus = AuthStatus.UNKNOWN
    policy: Optional[str] = None
    record: Optional[str] = None
    details: Optional[str] = None

class EmailAnalysisRequest(BaseModel):
    email_content: str = Field(..., description="Complete email content including headers")

class EmailAnalysisResponse(BaseModel):
    sender_email: Optional[EmailStr] = None
    sender_domain: Optional[str] = None
    headers: EmailHeaders
    spf_result: SPFResult
    dkim_result: DKIMResult
    dmarc_result: DMARCResult
    overall_score: int = Field(0, ge=0, le=100, description="Overall authentication score")
    is_authentic: bool = False
    warnings: List[str] = []
    analysis_timestamp: datetime = Field(default_factory=datetime.now)
