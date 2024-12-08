from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import create_access_token, verify_password, get_current_user
from app.crud import user_crud
from app.schemas.user_schema import Token, User, UserCreate
from app.core.config import settings

router = APIRouter()

@router.post("/register", response_model=User)
def register(user: UserCreate, db: Session = Depends(get_db)) -> Any:
    if user_crud.get_user_by_email(db, email=user.email):
        raise HTTPException(
            status_code=400,
            detail="A user with this email already exists."
        )
    if user_crud.get_user_by_username(db, username=user.username):
        raise HTTPException(
            status_code=400,
            detail="A user with this username already exists."
        )
    return user_crud.create_user(db, user)

@router.post("/token", response_model=Token)
def login(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    user = user_crud.get_user_by_username(db, username=form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=User)
def read_current_user(current_user: User = Depends(get_current_user)) -> Any:
    return current_user 