import os
from dotenv import load_dotenv
from typing import List

load_dotenv()

class Settings:
    """Application configuration settings"""
    
    # Application settings
    APP_NAME: str = "Email Security Tool"
    APP_VERSION: str = "2.0.0"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    
    # Server settings
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", 8000))
    
    # Security settings
    ALLOWED_HOSTS: List[str] = os.getenv("ALLOWED_HOSTS", "*").split(",")
    CORS_ORIGINS: List[str] = os.getenv("CORS_ORIGINS", "*").split(",")
    
    # Rate limiting
    RATE_LIMIT_ENABLED: bool = os.getenv("RATE_LIMIT_ENABLED", "True").lower() == "true"
    RATE_LIMIT_REQUESTS: int = int(os.getenv("RATE_LIMIT_REQUESTS", 100))
    RATE_LIMIT_PERIOD: int = int(os.getenv("RATE_LIMIT_PERIOD", 3600))
    
    # Discovery settings
    MAX_DISCOVERY_RESULTS: int = int(os.getenv("MAX_DISCOVERY_RESULTS", 500))
    DISCOVERY_TIMEOUT: int = int(os.getenv("DISCOVERY_TIMEOUT", 30))
    
    # Email analysis settings
    MAX_EMAIL_SIZE: int = int(os.getenv("MAX_EMAIL_SIZE", 10485760))  # 10MB
    ANALYSIS_TIMEOUT: int = int(os.getenv("ANALYSIS_TIMEOUT", 60))
    
    # External API settings
    VIRUSTOTAL_API_KEY: str = os.getenv("VIRUSTOTAL_API_KEY", "")
    HAVEIBEENPWNED_API_KEY: str = os.getenv("HAVEIBEENPWNED_API_KEY", "")
    
    # Cache settings
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    CACHE_TTL: int = int(os.getenv("CACHE_TTL", 3600))
    
    # DNS settings
    DNS_TIMEOUT: int = int(os.getenv("DNS_TIMEOUT", 10))
    DNS_SERVERS: List[str] = os.getenv("DNS_SERVERS", "8.8.8.8,1.1.1.1").split(",")

settings = Settings()