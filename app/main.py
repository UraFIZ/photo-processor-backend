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
    allow_origins=settings.get_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add routes
app.include_router(router, prefix=settings.API_PREFIX)

# Startup and shutdown events
@app.on_event("startup")
async def startup_event():
    logger.info("Starting FastAPI application")
    logger.info(f"CORS Origins: {settings.get_cors_origins()}")
    logger.info(f"API Prefix: {settings.API_PREFIX}")
    logger.info(f"Environment: {'Production' if settings.IS_PRODUCTION else 'Development'}")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down FastAPI application")

# Exception handling
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Global exception: {exc}", exc_info=True)
    return {"detail": "Internal server error"}

if __name__ == "__main__":
    import uvicorn
    logger.info(f"Starting server on {settings.HOST}:{settings.PORT}")
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True
    )