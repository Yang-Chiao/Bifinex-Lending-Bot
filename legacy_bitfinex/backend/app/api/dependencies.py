from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import verify_token
from app.models.user import User
from app.core.security import decrypt_api_key
from app.services.bitfinex_client import BitfinexClient

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """獲取當前登入用戶"""
    token = credentials.credentials
    payload = verify_token(token)
    
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="無效的認證憑證",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    email: str = payload.get("sub")
    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="無效的認證憑證",
        )
    
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用戶不存在",
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="用戶帳戶已被停用",
        )
    
    return user


def get_bitfinex_client(current_user: User = Depends(get_current_user)) -> BitfinexClient:
    """獲取 Bitfinex 客戶端"""
    if not current_user.api_key_encrypted or not current_user.api_secret_encrypted:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用戶尚未設置 Bitfinex API 憑證"
        )
    
    try:
        api_key = decrypt_api_key(current_user.api_key_encrypted)
        api_secret = decrypt_api_key(current_user.api_secret_encrypted)
        return BitfinexClient(api_key, api_secret)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"無法初始化 Bitfinex 客戶端: {str(e)}"
        )
