"""
AI Workforce Platform — Health & Gateway Readiness Tests
"""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root_discovery():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["service"] == "AI Workforce Platform — Core API Gateway"
    assert data["version"] == "1.0.0"
    assert data["docs"] == "/docs"


def test_liveness_health():
    response = client.get("/v1/healthz")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "HEALTHY"
    assert data["services"]["api"] == "UP"


def test_readiness_probe():
    response = client.get("/v1/healthz/ready")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "READY"


def test_openapi_spec_availability():
    response = client.get("/v1/openapi.json")
    assert response.status_code == 200
    data = response.json()
    assert "openapi" in data
    assert data["info"]["version"] == "1.0.0"
