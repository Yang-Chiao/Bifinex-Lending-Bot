"""
統一 API 響應格式

🔗 對應 TypeScript 類型：@trading-robots/types/common/response.ts

這個模組確保前後端 API 響應格式完全一致。
"""

from typing import Generic, TypeVar, Optional
from pydantic import BaseModel, Field

T = TypeVar('T')

class ApiError(BaseModel):
    """
    API 錯誤格式
    
    對應 TypeScript: ApiError
    """
    code: str = Field(..., description="錯誤代碼")
    message: str = Field(..., description="錯誤訊息")
    details: Optional[dict] = Field(None, description="錯誤詳情")
    
    class Config:
        json_schema_extra = {
            "example": {
                "code": "INVALID_CREDENTIALS",
                "message": "Email or password is incorrect",
                "details": {"field": "email"}
            }
        }

class ApiResponse(BaseModel, Generic[T]):
    """
    統一 API 響應格式
    
    對應 TypeScript: ApiResponse<T>
    
    使用範例：
    >>> ApiResponse[UserResponse](
    ...     success=True,
    ...     data=user_data,
    ...     message="User created successfully"
    ... )
    """
    success: bool = Field(..., description="請求是否成功")
    data: Optional[T] = Field(None, description="響應數據")
    error: Optional[ApiError] = Field(None, description="錯誤資訊")
    message: Optional[str] = Field(None, description="附加訊息")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "data": {"id": "123", "email": "user@example.com"},
                "message": "Operation successful"
            }
        }

# 便捷函數
def success_response(data: T = None, message: str = None) -> ApiResponse[T]:
    """創建成功響應"""
    return ApiResponse(success=True, data=data, message=message)

def error_response(code: str, message: str, details: dict = None) -> ApiResponse:
    """創建錯誤響應"""
    return ApiResponse(
        success=False,
        error=ApiError(code=code, message=message, details=details)
    )

