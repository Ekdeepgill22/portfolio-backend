#!/usr/bin/env python3
"""
Development server runner for Portfolio Backend API
"""
import uvicorn
from app.config import settings

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.is_development,
        log_level="info",
        access_log=True,
        loop="auto"
    )