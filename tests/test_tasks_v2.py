import pytest
from datetime import datetime, timedelta
from fastapi.testclient import TestClient

def get_auth_headers(client: TestClient, username: str):
    response = client.post("/api/v2/auth/token", data={
        "username": username,
        "password": "password"
    })
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.mark.parametrize("user_fixture", ["premium_user", "admin_user"])
def test_create_task_with_premium_features(client: TestClient, request, user_fixture):
    user = request.getfixturevalue(user_fixture)
    headers = get_auth_headers(client, user.username)
    
    task_data = {
        "title": "Premium Task",
        "description": "Test Description",
        "priority": "high",
        "due_date": (datetime.now() + timedelta(days=1)).isoformat(),
        "reminder_date": datetime.now().isoformat(),
        "recurrence_type": "daily",
        "recurrence_interval": 1
    }
    
    response = client.post("/api/v2/tasks/", json=task_data, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["priority"] == "high"
    assert "due_date" in data
    assert "next_occurrence" in data

def test_admin_access_all_tasks(client: TestClient, admin_user, premium_user):
    headers = get_auth_headers(client, "adminuser")
    
    # Create tasks for premium user
    premium_headers = get_auth_headers(client, "premiumuser")
    task_data = {"title": "Premium User Task", "description": "Test"}
    client.post("/api/v2/tasks/", json=task_data, headers=premium_headers)
    
    # Admin should see all tasks
    response = client.get("/api/v2/tasks/", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0 