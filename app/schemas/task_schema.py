from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from app.models.task_model import Priority, RecurrenceType


class TagBase(BaseModel):
    name: str


class TagCreate(TagBase):
    pass


class Tag(TagBase):
    id: int

    class Config:
        from_attributes = True


class CategoryBase(BaseModel):
    name: str


class CategoryCreate(CategoryBase):
    pass


class Category(CategoryBase):
    id: int

    class Config:
        from_attributes = True


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False
    priority: Priority = Priority.MEDIUM
    due_date: Optional[datetime] = None
    reminder_date: Optional[datetime] = None
    recurrence_type: Optional[RecurrenceType] = None
    recurrence_interval: Optional[int] = None


class TaskCreate(TaskBase):
    category_id: Optional[int] = None
    tag_ids: Optional[List[int]] = None


class Task(TaskBase):
    id: int
    category: Optional[Category] = None
    tags: List[Tag] = []
    next_occurrence: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
