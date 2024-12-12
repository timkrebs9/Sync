from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.crud import note_crud, user_crud
from app.models.user_model import User
from app.schemas.note_schema import Note, NoteCreate
from app.core.websocket_manager import manager
from app.services.encryption_service import encryption_service

router = APIRouter()

@router.post("/", response_model=Note)
def create_note(
    note: NoteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return note_crud.create_note(db=db, note=note, current_user=current_user)

@router.get("/", response_model=List[Note])
def read_notes(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    notes = note_crud.get_notes(db, current_user, skip=skip, limit=limit)
    return notes

@router.get("/{note_id}", response_model=Note)
def read_note(
    note_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    note = note_crud.get_note(db, note_id=note_id, current_user=current_user)
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

@router.put("/{note_id}", response_model=Note)
def update_note(
    note_id: int,
    note: NoteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    updated_note = note_crud.update_note(
        db, note_id=note_id, note_update=note, current_user=current_user
    )
    if updated_note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return updated_note

@router.delete("/{note_id}", response_model=Note)
def delete_note(
    note_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    note = note_crud.delete_note(db, note_id=note_id, current_user=current_user)
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

@router.post("/{note_id}/share")
def share_note(
    note_id: int,
    user_email: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    note = note_crud.get_note(db, note_id=note_id, current_user=current_user)
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    
    shared_user = user_crud.get_user_by_email(db, email=user_email)
    if shared_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return note_crud.add_collaborator(db, note, shared_user)

@router.websocket("/ws/{note_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    note_id: int,
    token: str,
    db: Session = Depends(get_db)
):
    try:
        # Verify token and get user
        user = get_current_user(token)
        await manager.connect(websocket, note_id, str(user.id))
        
        try:
            while True:
                data = await websocket.receive_json()
                # Handle different types of updates
                if data["type"] == "content_update":
                    await note_crud.update_note_content(
                        db, note_id, data["content"], user
                    )
                    await manager.broadcast_update(
                        note_id, 
                        {"type": "content_update", "content": data["content"]},
                        str(user.id)
                    )
        except WebSocketDisconnect:
            manager.disconnect(note_id, str(user.id))
    except Exception as e:
        await websocket.close() 