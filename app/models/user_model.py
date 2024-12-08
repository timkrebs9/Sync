from __future__ import annotations
from typing import List
from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, Enum, String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.sql import func
import enum

from app.core.database import Base

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"

class SubscriptionTier(str, enum.Enum):
    FREE = "free"
    PREMIUM = "premium"

class UserPreferences(Base):
    __tablename__ = "user_preferences"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = Column(Integer, ForeignKey("users.id"), unique=True)
    theme: Mapped[str] = Column(String, default="light")
    notifications_enabled: Mapped[bool] = Column(Boolean, default=True)
    default_reminder_time: Mapped[int] = Column(Integer, default=30)  # minutes
    timezone: Mapped[str] = Column(String, default="UTC")

    user: Mapped[User] = relationship("User", back_populates="preferences")

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    email: Mapped[str] = Column(String, unique=True, index=True)
    username: Mapped[str] = Column(String, unique=True, index=True)
    hashed_password: Mapped[str] = Column(String)
    role: Mapped[UserRole] = Column(Enum(UserRole), default=UserRole.USER)
    subscription: Mapped[SubscriptionTier] = Column(
        Enum(SubscriptionTier), 
        default=SubscriptionTier.FREE
    )
    is_active: Mapped[bool] = Column(Boolean, default=True)
    created_at: Mapped[datetime] = Column(
        DateTime(timezone=True), 
        server_default=func.now()
    )
    updated_at: Mapped[datetime | None] = Column(
        DateTime(timezone=True), 
        onupdate=func.now()
    )

    preferences: Mapped[UserPreferences] = relationship("UserPreferences", back_populates="user", uselist=False)
    tasks: Mapped[List["Task"]] = relationship("Task", back_populates="user") 