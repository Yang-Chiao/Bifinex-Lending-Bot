"""
共用依賴

提供 API 路由常用的依賴注入函數
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.database import get_db
from app.core.security import decrypt_api_key
from app.models.user import User
from app.services.bitfinex_client import BitfinexClient

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """獲取當前登入用戶"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token = credentials.credentials
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        token_type: str = payload.get("type")

        if user_id is None or token_type != "access":
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception
    return user


def get_bitfinex_client(current_user: User = Depends(get_current_user)) -> BitfinexClient:
    """
    取得 Bitfinex 客戶端

    - 從目前登入用戶讀取加密後的 API Key / Secret
    - 解密後建立 BitfinexClient 實例
    """
    if not current_user.bitfinex_api_key or not current_user.bitfinex_api_secret:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用戶尚未設置 Bitfinex API 憑證",
        )

    try:
        api_key = decrypt_api_key(current_user.bitfinex_api_key)
        api_secret = decrypt_api_key(current_user.bitfinex_api_secret)
        return BitfinexClient(api_key, api_secret)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"無法初始化 Bitfinex 客戶端: {str(e)}",
        )

