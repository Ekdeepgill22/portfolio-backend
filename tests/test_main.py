import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root_endpoint():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    
    data = response.json()
    assert data["message"] == "Portfolio Backend API"
    assert data["version"] == "1.0.0"
    assert "endpoints" in data


def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "healthy"
    assert "environment" in data
    assert "database" in data


def test_api_v1_root():
    """Test API v1 root endpoint"""
    response = client.get("/api/v1/")
    assert response.status_code == 200
    
    data = response.json()
    assert data["message"] == "Portfolio Backend API v1"
    assert "endpoints" in data
    assert "contact" in data["endpoints"]
    assert "resume" in data["endpoints"]
    assert "certifications" in data["endpoints"]


def test_cors_headers():
    """Test CORS headers are present"""
    response = client.options("/api/v1/contact")
    assert response.status_code == 200
    
    # FastAPI automatically handles CORS preflight requests
    assert "access-control-allow-origin" in response.headers or response.status_code == 200


def test_nonexistent_endpoint():
    """Test accessing non-existent endpoint"""
    response = client.get("/api/v1/nonexistent")
    assert response.status_code == 404