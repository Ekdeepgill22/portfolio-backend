# Static file serving
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import FileResponse
from pathlib import Path
import os
import logging
from functools import lru_cache

logger = logging.getLogger(__name__)
router = APIRouter()

BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "static"


@router.get("/resume")
async def download_resume():
    """
    Download resume PDF file
    """
    try:
        resume_path = STATIC_DIR / "resume" / "resume.pdf"
        
        if not resume_path.exists():
            logger.error(f"Resume file not found at: {resume_path}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Resume file not found"
            )
        
        return FileResponse(
            path=str(resume_path),
            filename="resume.pdf",
            media_type="application/pdf",
            headers={
                "Content-Disposition": "attachment; filename=resume.pdf",
                "Cache-Control": "no-cache"
            }
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error serving resume: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while serving the resume file"
        )


@router.get("/static/resume/resume.pdf")
async def serve_resume_direct():
    """
    Direct link to resume PDF (alternative endpoint)
    """
    return await download_resume()


@lru_cache(maxsize=1)
def get_certifications_list():
    cert_dir = STATIC_DIR / "certifications"
    image_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg'}
    certifications = []
    for file_path in cert_dir.iterdir():
        if file_path.is_file() and file_path.suffix.lower() in image_extensions:
            certifications.append({
                "filename": file_path.name,
                "url": f"/static/certifications/{file_path.name}",
                # "size": file_path.stat().st_size,  # Optional: remove if not needed
            })
    certifications.sort(key=lambda x: x['filename'])
    return certifications

@router.get("/certifications")
async def list_certifications():
    try:
        certifications = get_certifications_list()
        return {
            "certifications": certifications,
            "total": len(certifications)
        }
    except Exception as e:
        logger.error(f"Error listing certifications: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while listing certifications"
        )


@router.get("/static/certifications/{filename}")
async def serve_certification(filename: str):
    """
    Serve a specific certification image
    """
    try:
        cert_path = STATIC_DIR / "certifications" / filename
        
        if not cert_path.exists() or not cert_path.is_file():
            logger.error(f"Certification file not found: {cert_path}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Certification file not found"
            )
        
        # Determine media type based on file extension
        extension = cert_path.suffix.lower()
        media_type_map = {
            '.png': 'image/png',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.gif': 'image/gif',
            '.webp': 'image/webp',
            '.svg': 'image/svg+xml'
        }
        
        media_type = media_type_map.get(extension, 'application/octet-stream')
        
        return FileResponse(
            path=str(cert_path),
            filename=filename,
            media_type=media_type,
            headers={
                "Cache-Control": "max-age=3600"  # Cache for 1 hour
            }
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error serving certification {filename}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while serving the certification file"
        )


@router.get("/static/health")
async def static_health():
    """Health check endpoint for static files service"""
    return {"status": "healthy", "service": "static_files"}