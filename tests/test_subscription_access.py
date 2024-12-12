import pytest
from fastapi.testclient import TestClient
from fastapi import HTTPException
from unittest.mock import patch

def get_auth_headers(client: TestClient, username: str):
    response = client.post("/api/v2/auth/token", data={
        "username": username,
        "password": "password"
    })
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_free_user_v1_access(client: TestClient):
    # First register a free user
    register_response = client.post("/api/v2/auth/register", json={
        "email": "freeuser@example.com",
        "username": "freeuser",
        "password": "password123"
    })
    assert register_response.status_code == 200
    
    # Get auth token
    token_response = client.post("/api/v2/auth/token", data={
        "username": "freeuser",
        "password": "password123"
    })
    assert token_response.status_code == 200
    token = token_response.json()["access_token"]
    
    # Test V1 API access
    headers = {"Authorization": f"Bearer {token}"}
    task_data = {"title": "Test Task", "description": "Test Description"}
    response = client.post("/api/v1/tasks/", json=task_data, headers=headers)
    assert response.status_code == 200

