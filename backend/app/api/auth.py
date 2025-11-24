"""
Auth API Routes

所有 API 都使用統一響應格式 ApiResponse

🔗 對應前端 API：參考 docs/05-backend/api-design.md
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.auth import LoginRequest, LoginResponse, RegisterRequest
from app.schemas.user import UserResponse
from app.schemas.common import ApiResponse, success_response, error_response
from app.services import auth as auth_service

router = APIRouter()

@router.post("/register", response_model=ApiResponse[UserResponse])
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    """
    註冊新用戶
    
    對應 TypeScript API：POST /api/auth/register
    請求：RegisterRequest（包含 confirmPassword）
    響應：ApiResponse<User>
    """
    try:
        user = auth_service.create_user(db, request.email, request.password)
        return success_response(
            data=UserResponse.model_validate(user),
            message="User created successfully"
        )
    except HTTPException as e:
        return error_response(
            code="REGISTRATION_FAILED",
            message=e.detail
        )

@router.post("/login", response_model=ApiResponse[LoginResponse])
def login(request: LoginRequest, db: Session = Depends(get_db)):
    """
    用戶登入
    
    對應 TypeScript API：POST /api/auth/login
    請求：LoginRequest
    響應：ApiResponse<LoginResponse>（包含 accessToken 和 refreshToken）
    """
    user = auth_service.authenticate_user(db, request.email, request.password)
    if not user:
        return error_response(
            code="INVALID_CREDENTIALS",
            message="Incorrect email or password"
        )
    
    # 創建 Tokens
    tokens = auth_service.create_tokens(str(user.id))
    
    # 構建響應
    login_response = LoginResponse(
        accessToken=tokens["access_token"],
        refreshToken=tokens["refresh_token"],
        user=UserResponse.model_validate(user)
    )
    
    return success_response(
        data=login_response,
        message="Login successful"
    )

@router.post("/refresh", response_model=ApiResponse[dict])
def refresh_token(
    refresh_token: str,
    db: Session = Depends(get_db)
):
    """
    刷新 Access Token
    
    對應 TypeScript API：POST /api/auth/refresh
    """
    # TODO: 實作 refresh token 邏輯
    # 1. 驗證 refresh token
    # 2. 檢查用戶是否存在且活躍
    # 3. 生成新的 access token
    pass
