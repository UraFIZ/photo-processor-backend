import os
from typing import List
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Existing settings
    PORT = int(os.getenv("PORT", 5001))
    HOST = os.getenv("HOST", "0.0.0.0")
    
    # CORS settings
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",           # Local development
        "https://urafiz.github.io"         # Your GitHub Pages domain
    ]
    
    # Additional API settings
    API_PREFIX: str = "/api"
    PROJECT_NAME: str = "Photo Processor API"
    
    # You might want to add these for Azure
    IS_PRODUCTION: bool = os.getenv("ENVIRONMENT", "development") == "production"
    
    def get_cors_origins(self) -> List[str]:
        """Get CORS origins based on environment"""
        if self.IS_PRODUCTION:
            return self.CORS_ORIGINS
        # In development, allow all origins
        return ["*"]
    
settings = Settings()