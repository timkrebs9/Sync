import pytest
from datetime import datetime, timedelta
from fastapi.testclient import TestClient
from app.models.task_model import Priority, RecurrenceType

def test_create_task(authorized_client: TestClient):
    task_data = {
        "title": "Test Task",
        "description": "Test Description",
        "completed": False,
        "priority": "medium"
    }
    response = authorized_client.post("/api/v1/tasks/", json=task_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == task_data["title"]
    return data

def test_read_tasks(authorized_client: TestClient):
    # Create test task first
    task_data = test_create_task(authorized_client)
    
    response = authorized_client.get("/api/v1/tasks/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1

def test_read_task(authorized_client: TestClient):
    # Create test task first
    task_data = test_create_task(authorized_client)
    
    response = authorized_client.get(f"/api/v1/tasks/{task_data['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == task_data["title"]

def test_read_nonexistent_task(authorized_client: TestClient):
    response = authorized_client.get("/api/v1/tasks/999999")
    assert response.status_code == 404

def test_update_task(authorized_client: TestClient):
    # Create test task first
    task_data = test_create_task(authorized_client)
    
    update_data = {
        "title": "Updated Task",
        "description": "Updated Description"
    }
    response = authorized_client.put(f"/api/v1/tasks/{task_data['id']}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == update_data["title"]

def test_delete_task(authorized_client: TestClient):
    # Create test task first
    task_data = test_create_task(authorized_client)
    
    response = authorized_client.delete(f"/api/v1/tasks/{task_data['id']}")
    assert response.status_code == 200

def test_create_task_invalid_data(authorized_client: TestClient):
    task_data = {
        "title": "",  # Invalid empty title
        "description": "Test Description"
    }
    response = authorized_client.post("/api/v1/tasks/", json=task_data)
    assert response.status_code == 422

# Continue updating other tests similarly...
