import pytest
from fastapi.testclient import TestClient

def test_create_note(authorized_client: TestClient):
    note_data = {
        "title": "Test Note",
        "content": "Test Content",
        "is_encrypted": False
    }
    response = authorized_client.post("/api/v2/notes/", json=note_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == note_data["title"]
    return data

def test_read_notes(authorized_client: TestClient):
    # Create test note first
    note_data = test_create_note(authorized_client)
    
    response = authorized_client.get("/api/v2/notes/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1

def test_read_note(authorized_client: TestClient):
    # Create test note first
    note_data = test_create_note(authorized_client)
    
    response = authorized_client.get(f"/api/v2/notes/{note_data['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == note_data["title"]

def test_update_note(authorized_client: TestClient):
    # Create test note first
    note_data = test_create_note(authorized_client)
    
    update_data = {
        "title": "Updated Note",
        "content": "Updated Content",
        "is_encrypted": False
    }
    response = authorized_client.put(
        f"/api/v2/notes/{note_data['id']}", 
        json=update_data
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == update_data["title"]

def test_delete_note(authorized_client: TestClient):
    # Create test note first
    note_data = test_create_note(authorized_client)
    
    response = authorized_client.delete(f"/api/v2/notes/{note_data['id']}")
    assert response.status_code == 200 