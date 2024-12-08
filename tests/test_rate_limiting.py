import pytest
from fastapi.testclient import TestClient
import time

def get_auth_headers(client: TestClient, username: str):
    response = client.post("/api/v2/auth/token", data={
        "username": username,
        "password": "password"
    })
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

#def test_rate_limiting(client: TestClient, premium_user):
#    headers = get_auth_headers(client, premium_user.username)
#    
#    # Make requests up to the limit (60 requests per minute)
#    for _ in range(61):  # One more than the limit
#        response = client.get("/api/v2/tasks/", headers=headers)
#        if _ < 60:
#            assert response.status_code == 200
#        else:
#            assert response.status_code == 429
#            assert response.json()["detail"] == "Rate limit exceeded"

def test_rate_limit_reset(client: TestClient, premium_user):
    headers = get_auth_headers(client, premium_user.username)
    
    # Make some requests
    for _ in range(30):
        response = client.get("/api/v2/tasks/", headers=headers)
        assert response.status_code == 200
    
    # Wait for rate limit window to reset
    time.sleep(60)
    
    # Should be able to make requests again
    response = client.get("/api/v2/tasks/", headers=headers)
    assert response.status_code == 200 