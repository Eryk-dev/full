import os
from typing import List

class Settings:
    """Configurações da aplicação"""
    
    # API Settings
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", "5555"))
    API_DEBUG: bool = os.getenv("API_DEBUG", "False").lower() == "true"
    
    # Processing Settings
    MAX_FILE_SIZE_MB: int = int(os.getenv("MAX_FILE_SIZE_MB", "50"))
    ALLOWED_FILE_TYPES: List[str] = ["pdf"]
    
    # CORS Settings
    CORS_ORIGINS: List[str] = ["*"]
    
    # Log Settings
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # API Metadata
    API_TITLE: str = "Full Extractor API"
    API_DESCRIPTION: str = "API para extrair SKUs e quantidades de PDFs de preparação de envio"
    API_VERSION: str = "1.0.0"

settings = Settings() 