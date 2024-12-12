from __future__ import annotations
from datetime import datetime
from typing import List, Optional
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, Table, Boolean
from sqlalchemy.orm import Mapped, relationship, backref
from sqlalchemy.sql import func

from app.core.database import Base
from app.models.user_model import User

note_collaborators = Table(
    "note_collaborators",
    Base.metadata,
    Column("note_id", Integer, ForeignKey("notes.id")),
    Column("user_id", Integer, ForeignKey("users.id")),
)

class Note(Base):
    __tablename__ = "notes"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    title: Mapped[str] = Column(String, index=True)
    content: Mapped[str] = Column(Text)
    is_encrypted: Mapped[bool] = Column(Boolean, default=False)
    parent_id: Mapped[Optional[int]] = Column(Integer, ForeignKey("notes.id"), nullable=True)
    owner_id: Mapped[int] = Column(Integer, ForeignKey("users.id"))
    created_at: Mapped[datetime] = Column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = Column(DateTime(timezone=True), onupdate=func.now())

    owner: Mapped[User] = relationship("User", back_populates="notes")
    collaborators: Mapped[List[User]] = relationship(
        "User", 
        secondary=note_collaborators,
        backref="shared_notes"
    )
    children: Mapped[List[Note]] = relationship(
        "Note",
        backref=backref("parent", remote_side=[id]),
        cascade="all, delete-orphan"
    ) 