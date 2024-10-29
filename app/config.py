import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PORT = int(os.getenv("PORT", 5001))
    HOST = os.getenv("HOST", "0.0.0.0")
    
settings = Settings()