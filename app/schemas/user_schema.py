from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime
from app.models.user_model import UserRole, SubscriptionTier

class UserPreferencesBase(BaseModel):
    theme: str = "light"
    notifications_enabled: bool = True
    default_reminder_time: int = 30
    timezone: str = "UTC"

class UserPreferencesCreate(UserPreferencesBase):
    pass

class UserPreferences(UserPreferencesBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    email: EmailStr
    username: str
    role: UserRole = UserRole.USER
    subscription: SubscriptionTier = SubscriptionTier.FREE

class UserCreate(UserBase):
    password: str
    preferences: Optional[UserPreferencesCreate] = None

class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime]
    preferences: Optional[UserPreferences] = None

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None 