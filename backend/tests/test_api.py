"""
Tests for API endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)


class TestHealthEndpoint:
    """Tests for /health endpoint."""

    def test_health_returns_200(self, client):
        """Health endpoint should return 200 OK."""
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_returns_healthy_status(self, client):
        """Health endpoint should return healthy status."""
        response = client.get("/health")
        assert response.json() == {"status": "healthy"}


class TestStatusEndpoint:
    """Tests for /api/v1/status endpoint."""

    def test_status_returns_200(self, client):
        """Status endpoint should return 200 OK."""
        response = client.get("/api/v1/status")
        assert response.status_code == 200

    def test_status_contains_app_name(self, client):
        """Status should contain app name."""
        response = client.get("/api/v1/status")
        data = response.json()
        assert "app" in data
        assert data["app"] == "AI SDLC Co-Pilot"

    def test_status_contains_version(self, client):
        """Status should contain version."""
        response = client.get("/api/v1/status")
        data = response.json()
        assert "version" in data
        assert data["version"] == "0.1.0"


class TestRootEndpoint:
    """Tests for / root endpoint."""

    def test_root_returns_200(self, client):
        """Root endpoint should return 200 OK."""
        response = client.get("/")
        assert response.status_code == 200

    def test_root_contains_welcome_message(self, client):
        """Root should contain welcome message."""
        response = client.get("/")
        data = response.json()
        assert "message" in data
        assert "Welcome" in data["message"]
