"""
Auth Schemas

🔗 對應 TypeScript 類型：@trading-robots/types/api/auth.ts
"""

from pydantic import BaseModel, EmailStr, Field, field_validator
from app.schemas.user import UserResponse

class LoginRequest(BaseModel):
    """
    登入請求
    
    對應 TypeScript: LoginRequest
    """
    email: EmailStr = Field(..., description="Email")
    password: str = Field(..., min_length=6, description="密碼")
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "SecurePass123!"
            }
        }

class LoginResponse(BaseModel):
    """
    登入響應
    
    對應 TypeScript: LoginResponse
    
    💡 注意：
    - 使用 camelCase 欄位名稱匹配前端
    - 包含 refreshToken（與 Plan 1 一致）
    """
    accessToken: str = Field(..., description="存取 Token")
    refreshToken: str = Field(..., description="刷新 Token")
    user: UserResponse = Field(..., description="用戶資訊")
    
    class Config:
        json_schema_extra = {
            "example": {
                "accessToken": "eyJhbGciOiJIUzI1NiIs...",
                "refreshToken": "eyJhbGciOiJIUzI1NiIs...",
                "user": {
                    "id": "123",
                    "email": "user@example.com",
                    "role": "user",
                    "createdAt": "2024-01-01T00:00:00",
                    "updatedAt": "2024-01-01T00:00:00",
                    "isActive": True
                }
            }
        }

class RegisterRequest(BaseModel):
    """
    註冊請求
    
    對應 TypeScript: RegisterRequest
    
    💡 包含 confirmPassword 欄位（與 Plan 1 一致）
    """
    email: EmailStr = Field(..., description="Email")
    password: str = Field(..., min_length=8, description="密碼（至少8字元）")
    confirmPassword: str = Field(..., description="確認密碼")
    
    @field_validator('confirmPassword')
    @classmethod
    def passwords_match(cls, v, info):
        """驗證兩次密碼是否一致"""
        if 'password' in info.data and v != info.data['password']:
            raise ValueError('passwords do not match')
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "SecurePass123!",
                "confirmPassword": "SecurePass123!"
            }
        }

