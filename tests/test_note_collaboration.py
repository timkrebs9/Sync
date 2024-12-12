import pytest
from fastapi.testclient import TestClient
from fastapi.websockets import WebSocket
import asyncio

async def test_note_collaboration(authorized_client: TestClient):
    # Create a test note
    note_data = {
        "title": "Collaborative Note",
        "content": "Initial content",
        "is_encrypted": False
    }
    response = authorized_client.post("/api/v2/notes/", json=note_data)
    note = response.json()
    
    # Test sharing the note
    share_response = authorized_client.post(
        f"/api/v2/notes/{note['id']}/share",
        json={"user_email": "collaborator@example.com"}
    )
    assert share_response.status_code == 200
    
    # Test WebSocket connection
    async with authorized_client.websocket_connect(
        f"/api/v2/notes/ws/{note['id']}?token={token}"
    ) as websocket:
        await websocket.send_json({
            "type": "content_update",
            "content": "Updated content"
        })
        data = await websocket.receive_json()
        assert data["type"] == "content_update"
        assert data["content"] == "Updated content" 