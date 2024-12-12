from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

class NoteBase(BaseModel):
    title: str
    content: str
    is_encrypted: bool = False
    parent_id: Optional[int] = None

class NoteCreate(NoteBase):
    pass

class Note(NoteBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: Optional[datetime]
    collaborator_ids: List[int] = []

    class Config:
        from_attributes = True 