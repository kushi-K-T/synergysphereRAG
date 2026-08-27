import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data

def test_zero_fallback_on_local_failure():
    with patch("app.local_ai.local_llm.local_llm.execute", side_effect=RuntimeError("Ollama down")):
        response = client.post("/query", json={"query": "Show my private project data."})
        assert response.status_code == 503
        assert "Zero-fallback enforced" in response.json()["detail"]
