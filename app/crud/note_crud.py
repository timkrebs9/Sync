from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.note_model import Note
from app.models.user_model import User, UserRole
from app.schemas.note_schema import NoteCreate
from app.core.permissions import is_task_owner
from app.services.encryption_service import encryption_service
from sqlalchemy.sql import func

def create_note(db: Session, note: NoteCreate, current_user: User) -> Note:
    db_note = Note(
        **note.model_dump(),
        owner_id=current_user.id
    )
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

def get_notes(
    db: Session, 
    current_user: User, 
    skip: int = 0, 
    limit: int = 100
) -> List[Note]:
    if current_user.role == UserRole.ADMIN:
        return db.query(Note).offset(skip).limit(limit).all()
    return (
        db.query(Note)
        .filter(
            (Note.owner_id == current_user.id) | 
            (Note.collaborators.any(id=current_user.id))
        )
        .offset(skip)
        .limit(limit)
        .all()
    )

def get_note(db: Session, note_id: int, current_user: User) -> Optional[Note]:
    note = db.query(Note).filter(Note.id == note_id).first()
    if note and (
        is_task_owner(current_user, note.owner_id) or 
        current_user in note.collaborators
    ):
        return note
    return None

def update_note(
    db: Session, 
    note_id: int, 
    note_update: NoteCreate, 
    current_user: User
) -> Optional[Note]:
    db_note = get_note(db, note_id=note_id, current_user=current_user)
    if db_note is None:
        return None

    for key, value in note_update.model_dump().items():
        setattr(db_note, key, value)

    db.commit()
    db.refresh(db_note)
    return db_note

def delete_note(db: Session, note_id: int, current_user: User) -> Optional[Note]:
    db_note = get_note(db, note_id=note_id, current_user=current_user)
    if db_note is None:
        return None

    db.delete(db_note)
    db.commit()
    return db_note 

async def update_note_content(
    db: Session, 
    note_id: int, 
    content: str, 
    current_user: User
) -> Optional[Note]:
    db_note = get_note(db, note_id=note_id, current_user=current_user)
    if db_note is None:
        return None

    if db_note.is_encrypted:
        content = encryption_service.encrypt_content(content)
    
    db_note.content = content
    db_note.updated_at = func.now()
    db.commit()
    db.refresh(db_note)
    return db_note

def add_collaborator(db: Session, note: Note, user: User) -> Note:
    if user not in note.collaborators:
        note.collaborators.append(user)
        db.commit()
        db.refresh(note)
    return note 