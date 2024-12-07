import pytest
from fastapi.testclient import TestClient

def test_create_task(client: TestClient):
    task_data = {
        "title": "Test Task",
        "description": "Test Description",
        "completed": False
    }
    
    response = client.post("/api/v1/tasks/", json=task_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == task_data["title"]
    assert data["description"] == task_data["description"]
    assert data["completed"] == task_data["completed"]
    assert "id" in data
    assert "created_at" in data

def test_read_tasks(client: TestClient):
    # Create test tasks
    task_data = [
        {"title": "Task 1", "description": "Description 1"},
        {"title": "Task 2", "description": "Description 2"}
    ]
    
    for task in task_data:
        client.post("/api/v1/tasks/", json=task)
    
    response = client.get("/api/v1/tasks/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["title"] == "Task 1"
    assert data[1]["title"] == "Task 2"

def test_read_task(client: TestClient):
    # Create a test task
    task_data = {"title": "Single Task", "description": "Test Description"}
    create_response = client.post("/api/v1/tasks/", json=task_data)
    task_id = create_response.json()["id"]
    
    response = client.get(f"/api/v1/tasks/{task_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == task_data["title"]
    assert data["description"] == task_data["description"]

def test_read_nonexistent_task(client: TestClient):
    response = client.get("/api/v1/tasks/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"

def test_update_task(client: TestClient):
    # Create a test task
    task_data = {"title": "Original Title", "description": "Original Description"}
    create_response = client.post("/api/v1/tasks/", json=task_data)
    task_id = create_response.json()["id"]
    
    # Update the task
    update_data = {"title": "Updated Title", "description": "Updated Description", "completed": True}
    response = client.put(f"/api/v1/tasks/{task_id}", json=update_data)
    
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == update_data["title"]
    assert data["description"] == update_data["description"]
    assert data["completed"] == update_data["completed"]

def test_update_nonexistent_task(client: TestClient):
    update_data = {"title": "Updated Title", "description": "Updated Description"}
    response = client.put("/api/v1/tasks/999", json=update_data)
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"

def test_delete_task(client: TestClient):
    # Create a test task
    task_data = {"title": "Task to Delete", "description": "Will be deleted"}
    create_response = client.post("/api/v1/tasks/", json=task_data)
    task_id = create_response.json()["id"]
    
    # Delete the task
    response = client.delete(f"/api/v1/tasks/{task_id}")
    assert response.status_code == 200
    
    # Verify task is deleted
    get_response = client.get(f"/api/v1/tasks/{task_id}")
    assert get_response.status_code == 404

def test_delete_nonexistent_task(client: TestClient):
    response = client.delete("/api/v1/tasks/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"

def test_create_task_invalid_data(client: TestClient):
    task_data = {
        "description": "Missing title field"
    }
    response = client.post("/api/v1/tasks/", json=task_data)
    assert response.status_code == 422

def test_pagination(client: TestClient):
    # Create 15 test tasks
    for i in range(15):
        task_data = {"title": f"Task {i}", "description": f"Description {i}"}
        client.post("/api/v1/tasks/", json=task_data)
    
    # Test default pagination (limit=100)
    response = client.get("/api/v1/tasks/")
    assert response.status_code == 200
    assert len(response.json()) == 15
    
    # Test custom pagination
    response = client.get("/api/v1/tasks/?skip=5&limit=5")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 5
    assert data[0]["title"] == "Task 5" 