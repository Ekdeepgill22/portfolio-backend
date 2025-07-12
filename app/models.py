# Pydantic models with validation
from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from datetime import datetime
import re


class ContactFormRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Contact name")
    email: EmailStr = Field(..., description="Contact email address")
    subject: str = Field(..., min_length=1, max_length=200, description="Email subject")
    message: str = Field(..., min_length=1, max_length=2000, description="Email message")
    
    @validator('name')
    def validate_name(cls, v):
        # Remove any potential HTML tags and extra whitespace
        v = re.sub(r'<[^>]+>', '', v).strip()
        if not v:
            raise ValueError('Name cannot be empty')
        return v
    
    @validator('subject')
    def validate_subject(cls, v):
        # Remove any potential HTML tags and extra whitespace
        v = re.sub(r'<[^>]+>', '', v).strip()
        if not v:
            raise ValueError('Subject cannot be empty')
        return v
    
    @validator('message')
    def validate_message(cls, v):
        # Remove any potential HTML tags and extra whitespace
        v = re.sub(r'<[^>]+>', '', v).strip()
        if not v:
            raise ValueError('Message cannot be empty')
        return v


class ContactFormResponse(BaseModel):
    success: bool
    message: str
    id: Optional[str] = None


class ContactDocument(BaseModel):
    name: str
    email: str
    subject: str
    message: str
    created_at: datetime
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    
    class Config:
        # Allow datetime fields to be serialized
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }