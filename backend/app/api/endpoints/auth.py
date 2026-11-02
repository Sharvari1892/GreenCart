from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user
from app.core.security import verify_password, get_password_hash, create_access_token
from app.schemas.auth import UserCreate, UserLogin, UserResponse, Token, RefreshRequest
from app.models.user import User
from app.models.refresh_token import RefreshToken
from app.core.config import settings
import secrets
from datetime import datetime, timedelta, timezone

router = APIRouter()

def create_refresh_token_record(db: Session, user_id: int) -> str:
    token_val = secrets.token_urlsafe(32)
    expires = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    db_token = RefreshToken(token=token_val, user_id=user_id, expires_at=expires)
    db.add(db_token)
    db.commit()
    return token_val

@router.post("/register", response_model=UserResponse)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_in.email).first()
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    user = User(
        name=user_in.name,
        email=user_in.email,
        password_hash=get_password_hash(user_in.password),
        role="user"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.post("/login", response_model=Token)
def login(user_in: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_in.email).first()
    if not user or not verify_password(user_in.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    
    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token_record(db, user.id)
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "refresh_token": refresh_token
    }

@router.post("/refresh", response_model=Token)
def refresh_token(req: RefreshRequest, db: Session = Depends(get_db)):
    token_record = db.query(RefreshToken).filter(RefreshToken.token == req.refresh_token).first()
    if not token_record or token_record.revoked or token_record.expires_at.timestamp() < datetime.now(timezone.utc).timestamp():
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")
    
    # Revoke old token
    token_record.revoked = True
    db.commit()
    
    user = db.query(User).filter(User.id == token_record.user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
        
    access_token = create_access_token(user.id)
    new_refresh_token = create_refresh_token_record(db, user.id)
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "refresh_token": new_refresh_token
    }

@router.post("/logout")
def logout(req: RefreshRequest, db: Session = Depends(get_db)):
    token_record = db.query(RefreshToken).filter(RefreshToken.token == req.refresh_token).first()
    if token_record:
        token_record.revoked = True
        db.commit()
    return {"msg": "Successfully logged out"}

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
