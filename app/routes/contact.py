# Contact form endpoints
from fastapi import APIRouter, HTTPException, Request, status
from fastapi.responses import JSONResponse
from app.models import ContactFormRequest, ContactFormResponse, ContactDocument
from app.services.db import insert_contact
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/contact", response_model=ContactFormResponse)
async def submit_contact_form(
    contact_request: ContactFormRequest,
    request: Request
):
    """
    Submit a contact form
    
    - **name**: Contact's name (required)
    - **email**: Contact's email address (required)
    - **subject**: Email subject (required)
    - **message**: Email message (required)
    """
    try:
        # Get client information for logging
        client_ip = request.client.host if request.client else "unknown"
        user_agent = request.headers.get("user-agent", "unknown")
        
        # Create contact document
        contact_doc = ContactDocument(
            name=contact_request.name,
            email=contact_request.email,
            subject=contact_request.subject,
            message=contact_request.message,
            created_at=datetime.utcnow(),
            ip_address=client_ip,
            user_agent=user_agent
        )
        
        # Convert to dict for MongoDB insertion
        contact_dict = contact_doc.dict()
        
        # Insert into database
        contact_id = await insert_contact(contact_dict)
        
        logger.info(f"Contact form submitted successfully. ID: {contact_id}, Email: {contact_request.email}")
        
        return ContactFormResponse(
            success=True,
            message="Contact form submitted successfully. Thank you for reaching out!",
            id=contact_id
        )
        
    except Exception as e:
        logger.error(f"Error processing contact form: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while processing your request. Please try again later."
        )


@router.get("/contact/health")
async def contact_health():
    """Health check endpoint for contact service"""
    return {"status": "healthy", "service": "contact"}


# Optional: Admin endpoint to get contacts (add authentication in production)
@router.get("/contact/admin/all")
async def get_all_contacts_admin(skip: int = 0, limit: int = 50):
    """
    Admin endpoint to get all contacts
    Note: In production, this should be protected with authentication
    """
    try:
        from app.services.db import get_all_contacts
        contacts = await get_all_contacts(skip=skip, limit=limit)
        
        # Convert ObjectId to string for JSON serialization
        for contact in contacts:
            contact["_id"] = str(contact["_id"])
            
        return {
            "contacts": contacts,
            "total": len(contacts),
            "skip": skip,
            "limit": limit
        }
        
    except Exception as e:
        logger.error(f"Error getting contacts: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving contacts."
        )