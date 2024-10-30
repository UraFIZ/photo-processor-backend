from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from .api.routes import router
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(title=settings.PROJECT_NAME)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development, replace with actual origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add routes
app.include_router(router, prefix=settings.API_PREFIX)

@app.on_event("startup")
async def startup_event():
    logger.info("Starting FastAPI application")
    logger.info(f"CORS Origins: {settings.get_cors_origins()}")
    logger.info(f"API Prefix: {settings.API_PREFIX}")