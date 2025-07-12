import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_contact_form_valid():
    """Test valid contact form submission"""
    contact_data = {
        "name": "John Doe",
        "email": "john@example.com",
        "subject": "Test Subject",
        "message": "This is a test message"
    }
    
    response = client.post("/api/v1/contact", json=contact_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["success"] is True
    assert "id" in data
    assert data["message"] == "Contact form submitted successfully. Thank you for reaching out!"


def test_contact_form_invalid_email():
    """Test contact form with invalid email"""
    contact_data = {
        "name": "John Doe",
        "email": "invalid-email",
        "subject": "Test Subject",
        "message": "This is a test message"
    }
    
    response = client.post("/api/v1/contact", json=contact_data)
    assert response.status_code == 422  # Validation error


def test_contact_form_missing_fields():
    """Test contact form with missing required fields"""
    contact_data = {
        "name": "John Doe",
        "email": "john@example.com"
        # Missing subject and message
    }
    
    response = client.post("/api/v1/contact", json=contact_data)
    assert response.status_code == 422  # Validation error


def test_contact_form_empty_fields():
    """Test contact form with empty fields"""
    contact_data = {
        "name": "",
        "email": "john@example.com",
        "subject": "",
        "message": ""
    }
    
    response = client.post("/api/v1/contact", json=contact_data)
    assert response.status_code == 422  # Validation error


def test_contact_form_html_sanitization():
    """Test HTML tag sanitization in contact form"""
    contact_data = {
        "name": "<script>alert('xss')</script>John Doe",
        "email": "john@example.com",
        "subject": "<b>Test</b> Subject",
        "message": "<p>This is a test message</p>"
    }
    
    response = client.post("/api/v1/contact", json=contact_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["success"] is True


def test_contact_health():
    """Test contact service health check"""
    response = client.get("/api/v1/contact/health")
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "contact"


def test_contact_admin_endpoint():
    """Test admin endpoint for getting contacts"""
    response = client.get("/api/v1/contact/admin/all")
    assert response.status_code == 200
    
    data = response.json()
    assert "contacts" in data
    assert "total" in data
    assert isinstance(data["contacts"], list)