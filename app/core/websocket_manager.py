from typing import Dict, Set
from fastapi import WebSocket
import json

class WebSocketManager:
    def __init__(self):
        self.active_connections: Dict[int, Dict[str, WebSocket]] = {}  # note_id -> {user_id: websocket}
        self.user_connections: Dict[str, Set[int]] = {}  # user_id -> set of note_ids

    async def connect(self, websocket: WebSocket, note_id: int, user_id: str):
        await websocket.accept()
        if note_id not in self.active_connections:
            self.active_connections[note_id] = {}
        self.active_connections[note_id][user_id] = websocket
        
        if user_id not in self.user_connections:
            self.user_connections[user_id] = set()
        self.user_connections[user_id].add(note_id)

    def disconnect(self, note_id: int, user_id: str):
        if note_id in self.active_connections:
            self.active_connections[note_id].pop(user_id, None)
        if user_id in self.user_connections:
            self.user_connections[user_id].remove(note_id)

    async def broadcast_update(self, note_id: int, data: dict, exclude_user: str = None):
        if note_id in self.active_connections:
            for user_id, connection in self.active_connections[note_id].items():
                if user_id != exclude_user:
                    await connection.send_json(data)

manager = WebSocketManager() 