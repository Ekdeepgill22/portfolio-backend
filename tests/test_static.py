import pytest
from fastapi.testclient import TestClient
from app.main import app
import os
from pathlib import Path

client = TestClient(app)

def test_static_health():
    """Test static files service health check"""
    response = client.get("/api/v1/static/health")
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "static_files"


def test_certifications_list():
    """Test certifications listing endpoint"""
    response = client.get("/api/v1/certifications")
    
    # Should return 200 even if directory doesn't exist (will return 404)
    # or if it exists (will return certification list)
    assert response.status_code in [200, 404]
    
    if response.status_code == 200:
        data = response.json()
        assert "certifications" in data
        assert "total" in data
        assert isinstance(data["certifications"], list)


def test_resume_download():
    """Test resume download endpoint"""
    response = client.get("/api/v1/resume")
    
    # Should return 404 if file doesn't exist, 200 if it does
    assert response.status_code in [200, 404]
    
    if response.status_code == 200:
        assert response.headers["content-type"] == "application/pdf"
        assert "attachment" in response.headers["content-disposition"]


def test_resume_direct_link():
    """Test direct resume link"""
    response = client.get("/api/v1/static/resume/resume.pdf")
    
    # Should return 404 if file doesn't exist, 200 if it does
    assert response.status_code in [200, 404]
    
    if response.status_code == 200:
        assert response.headers["content-type"] == "application/pdf"


def test_certification_serve():
    """Test serving a specific certification"""
    response = client.get("/api/v1/static/certifications/nonexistent.png")
    assert response.status_code == 404


def test_certification_serve_invalid_path():
    """Test serving certification with invalid path"""
    response = client.get("/api/v1/static/certifications/../../../etc/passwd")
    assert response.status_code == 404