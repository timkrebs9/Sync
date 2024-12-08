from __future__ import annotations

import enum
from datetime import datetime
from typing import List

from sqlalchemy import Boolean, Column, DateTime, Enum, ForeignKey, Integer, String, Table
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.sql import func

from app.core.database import Base
from app.models.user_model import User

__all__ = ["Priority", "RecurrenceType", "Tag", "Category", "Task"]


class Priority(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class RecurrenceType(str, enum.Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"


task_tags = Table(
    "task_tags",
    Base.metadata,
    Column("task_id", Integer, ForeignKey("tasks.id")),
    Column("tag_id", Integer, ForeignKey("tags.id")),
)


class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    name: Mapped[str] = Column(String, unique=True, index=True)
    tasks: Mapped[List[Task]] = relationship("Task", secondary=task_tags, back_populates="tags")


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    name: Mapped[str] = Column(String, unique=True, index=True)
    tasks: Mapped[List[Task]] = relationship("Task", back_populates="category")


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    title: Mapped[str] = Column(String, index=True)
    description: Mapped[str | None] = Column(String, nullable=True)
    completed: Mapped[bool] = Column(Boolean, default=False)
    priority: Mapped[Priority] = Column(Enum(Priority), default=Priority.MEDIUM)
    due_date: Mapped[datetime | None] = Column(DateTime(timezone=True), nullable=True)
    reminder_date: Mapped[datetime | None] = Column(DateTime(timezone=True), nullable=True)
    category_id: Mapped[int | None] = Column(Integer, ForeignKey("categories.id"), nullable=True)
    recurrence_type: Mapped[RecurrenceType | None] = Column(Enum(RecurrenceType), nullable=True)
    recurrence_interval: Mapped[int | None] = Column(Integer, nullable=True)
    next_occurrence: Mapped[datetime | None] = Column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = Column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime | None] = Column(DateTime(timezone=True), onupdate=func.now())
    user_id: Mapped[int] = Column(Integer, ForeignKey("users.id"))

    category: Mapped[Category | None] = relationship("Category", back_populates="tasks")
    tags: Mapped[List[Tag]] = relationship("Tag", secondary=task_tags, back_populates="tasks")
    user: Mapped[User] = relationship("User", back_populates="tasks")
