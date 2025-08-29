from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from datetime import datetime
import traceback

# Import your services and models
from app.utils.email_parser import ModernEmailParser
from app.services.spf_service import SPFService
from app.models.email_models import EmailHeaders, SPFResult, DKIMResult, DMARCResult
from app.services.discovery_service import EmailDiscoveryService
from app.models.discovery_models import DiscoveredEmail,EmailDiscoveryResponse
app = FastAPI(
    title="Email Authentication Checker",
    description="A tool to verify email authenticity using SPF, DKIM, and DMARC",
    version="1.0.0"
)

# Fix: Update both paths to use app/ directory
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})




# Add these imports
from app.services.discovery_service import EmailDiscoveryService
from app.models.discovery_models import EmailDiscoveryRequest, EmailDiscoveryResponse
@app.post("/discover", response_class=HTMLResponse)
async def discover_emails(
    request: Request,
    domain: str = Form(...),
    sources: list[str] = Form(...),
    max_results: int = Form(100)
):
    """Discover emails for a domain"""
    try:
        if not domain.strip():
            raise HTTPException(status_code=400, detail="Domain cannot be empty")
        
        # Clean domain input
        domain = domain.strip().lower().replace('http://', '').replace('https://', '').split('/')[0]
        
        # Initialize discovery service
        discovery_service = EmailDiscoveryService()
        
        # Search for emails from the selected sources
        discovered_emails = discovery_service.discover_emails(domain, sources)
        
        # Limit results
        if len(discovered_emails) > max_results:
            discovered_emails = discovered_emails[:max_results]
        
        # --- THE FIX IS HERE ---
        # Instead of a raw dict, create an instance of your Pydantic model.
        # Pydantic will handle the datetime serialization correctly.
        discovery_result = EmailDiscoveryResponse(
            domain=domain,
            total_found=len(discovered_emails),
            emails=discovered_emails,
            sources_used=sources,
            discovery_timestamp=datetime.now()
        )
        
        return templates.TemplateResponse("discovery_results.html", {
            "request": request,
            "result": discovery_result  # Pass the Pydantic model instance
        })
        
    except Exception as e:
        traceback.print_exc() # For better debugging
        raise HTTPException(status_code=500, detail=f"Discovery failed: {str(e)}")

@app.post("/analyze", response_class=HTMLResponse)
async def analyze_email(
    request: Request,
    email_content: str = Form(...)
):
    try:
        if not email_content.strip():
            raise HTTPException(status_code=400, detail="Email content cannot be empty")
        
        # Parse email using your service
        parser = ModernEmailParser(email_content)
        headers = parser.extract_headers()
        sender_info = parser.extract_sender_info()
        
        # Initialize services
        spf_service = SPFService()
        
        # Perform SPF check
        spf_result = SPFResult()
        if sender_info['domain']:
            spf_check = spf_service.check_spf('0.0.0.0', sender_info['domain'])
            spf_result.status = "pass" if spf_check['valid'] else "fail"
            spf_result.details = spf_check['result']
            spf_result.record = spf_check['record']
        
        # Create analysis result
        analysis_result = {
            "sender_email": sender_info['email'],
            "sender_domain": sender_info['domain'],
            "headers": headers,
            "spf_result": spf_result,
            "timestamp": datetime.now()
        }
        
        return templates.TemplateResponse("results.html", {
            "request": request, 
            "analysis": analysis_result
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "Email Auth API is running"}
