"""
Auth Service

業務邏輯：用戶認證、註冊、Token 管理
"""

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.user import User
from app.core.security import verify_password, get_password_hash, create_access_token
from datetime import timedelta
from app.core.config import settings

def authenticate_user(db: Session, email: str, password: str) -> User:
    """
    驗證用戶
    
    Args:
        db: 資料庫 session
        email: Email
        password: 明文密碼
        
    Returns:
        User 物件或 None
    """
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    if not user.is_active:
        return None
    return user

def create_user(db: Session, email: str, password: str) -> User:
    """
    創建用戶
    
    Args:
        db: 資料庫 session
        email: Email
        password: 明文密碼
        
    Returns:
        User 物件
        
    Raises:
        HTTPException: Email 已註冊
    """
    # 檢查是否已存在
    if db.query(User).filter(User.email == email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # 創建用戶
    db_user = User(
        email=email,
        password_hash=get_password_hash(password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_tokens(user_id: str) -> dict:
    """
    創建 Access Token 和 Refresh Token
    
    Args:
        user_id: 用戶 ID
        
    Returns:
        包含 access_token 和 refresh_token 的字典
    """
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user_id, "type": "access"},
        expires_delta=access_token_expires
    )
    
    refresh_token_expires = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    refresh_token = create_access_token(
        data={"sub": user_id, "type": "refresh"},
        expires_delta=refresh_token_expires
    )
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }

