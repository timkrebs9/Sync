from typing import Optional
from sqlalchemy.orm import Session
from app.models.user_model import User, UserPreferences, SubscriptionTier
from app.schemas.user_schema import UserCreate
from app.core.security import get_password_hash
from datetime import datetime

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()

def get_user_by_username(db: Session, username: str) -> Optional[User]:
    return db.query(User).filter(User.username == username).first()

def create_user(db: Session, user: UserCreate) -> User:
    db_user = User(
        email=user.email,
        username=user.username,
        hashed_password=get_password_hash(user.password),
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    if user.preferences:
        db_preferences = UserPreferences(
            user_id=db_user.id,
            **user.preferences.dict()
        )
        db.add(db_preferences)
        db.commit()
        db.refresh(db_user)

    return db_user

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()

async def update_subscription_status(
    db: Session, 
    user_id: int, 
    subscription_tier: SubscriptionTier,
    stripe_subscription_id: str = None,
    subscription_end_date: datetime = None
):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.subscription = subscription_tier
        if stripe_subscription_id:
            user.stripe_subscription_id = stripe_subscription_id
        if subscription_end_date:
            user.subscription_end_date = subscription_end_date
        db.commit()
        db.refresh(user)
    return user 