import pytest
from fastapi.testclient import TestClient

def test_user_registration(client: TestClient):
    response = client.post("/api/v2/auth/register", json={
        "email": "test@example.com",
        "username": "testuser",
        "password": "testpass123"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["subscription"] == "free"

def test_user_login(client: TestClient):
    # First create a test user
    client.post("/api/v2/auth/register", json={
        "email": "logintest@example.com",
        "username": "logintest",
        "password": "password123"
    })
    
    response = client.post("/api/v2/auth/token", data={
        "username": "logintest",
        "password": "password123"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_invalid_login(client: TestClient):
    response = client.post("/api/v2/auth/token", data={
        "username": "wronguser",
        "password": "wrongpass"
    })
    assert response.status_code == 401