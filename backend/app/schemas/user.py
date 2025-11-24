"""
User Schemas

🔗 對應 TypeScript 類型：@trading-robots/types/entities/user.ts
"""

from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    """用戶基礎 Schema"""
    email: EmailStr = Field(..., description="用戶 Email")

class UserResponse(BaseModel):
    """
    用戶響應 Schema
    
    對應 TypeScript: User
    
    💡 注意：使用 alias 支援前端的 camelCase 命名
    """
    id: str = Field(..., description="用戶 ID")
    email: str = Field(..., description="Email")
    role: str = Field(..., description="角色")
    createdAt: datetime = Field(..., alias="created_at", description="創建時間")
    updatedAt: datetime = Field(..., alias="updated_at", description="更新時間")
    isActive: bool = Field(..., alias="is_active", description="是否啟用")
    
    class Config:
        from_attributes = True
        populate_by_name = True  # 允許同時接受 snake_case 和 camelCase

class UserProfileResponse(UserResponse):
    """
    用戶詳情響應
    
    對應 TypeScript: UserProfile extends User
    """
    hasBitfinexApiKey: bool = Field(..., alias="has_bitfinex_api_key")
    strategiesCount: int = Field(default=0, alias="strategies_count")
    totalEarnings: float = Field(default=0.0, alias="total_earnings")
