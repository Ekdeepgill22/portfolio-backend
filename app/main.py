# FastAPI app with middleware
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import logging
import uvicorn
from pathlib import Path
import os

# Import configuration and services
from app.config import settings
from app.services.db import connect_to_mongo, close_mongo_connection

# Import routes
from app.routes.contact import router as contact_router
from app.routes.static import router as static_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title=settings.project_name,
    description="Backend API for portfolio website with contact form and static file serving",
    version="1.0.0",
    docs_url="/docs" if settings.is_development else None,
    redoc_url="/redoc" if settings.is_development else None,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=False,  # Set to False when using "*"
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Mount static files (for direct file access)
BASE_DIR = Path(__file__).resolve().parent
static_path = BASE_DIR / "static"
if static_path.exists():
    app.mount(
        "/static",
        StaticFiles(
            directory=str(static_path),
            html=False
        ),
        name="static"
    )

# Include routers
app.include_router(contact_router, prefix=settings.api_v1_str, tags=["Contact"])
app.include_router(static_router, prefix=settings.api_v1_str, tags=["Static Files"])

# Database event handlers
@app.on_event("startup")
async def startup_event():
    """Initialize database connection on startup"""
    try:
        await connect_to_mongo()
        logger.info("Application startup completed successfully")
    except Exception as e:
        logger.error(f"Failed to start application: {e}")
        raise e

@app.on_event("shutdown")
async def shutdown_event():
    """Close database connection on shutdown"""
    await close_mongo_connection()
    logger.info("Application shutdown completed")

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler for unhandled errors"""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": "An unexpected error occurred. Please try again later."
        }
    )

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Portfolio Backend API",
        "version": "1.0.0",
        "docs_url": "/docs" if settings.is_development else "Not available in production",
        "endpoints": {
            "contact": f"{settings.api_v1_str}/contact",
            "resume": f"{settings.api_v1_str}/resume",
            "certifications": f"{settings.api_v1_str}/certifications"
        }
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "environment": settings.environment,
        "database": "connected" if settings.mongodb_uri else "not configured"
    }

# API v1 root
@app.get(f"{settings.api_v1_str}/")
async def api_v1_root():
    """API v1 root endpoint"""
    return {
        "message": "Portfolio Backend API v1",
        "endpoints": {
            "contact": "/contact",
            "resume": "/resume",
            "certifications": "/certifications"
        }
    }

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.is_development,
        log_level="info"
    )