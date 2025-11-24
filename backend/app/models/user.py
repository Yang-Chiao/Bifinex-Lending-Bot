"""
User Model

🔗 對應 TypeScript 類型：@trading-robots/types/entities/user.ts
"""

from sqlalchemy import Column, String, Boolean, Enum
from sqlalchemy.orm import relationship
import enum
from app.models.base import BaseModel

class UserRole(str, enum.Enum):
    """
    用戶角色
    
    對應 TypeScript: UserRole = 'admin' | 'user'
    """
    ADMIN = "admin"
    USER = "user"

class User(BaseModel):
    """
    用戶實體
    
    對應 TypeScript: User interface
    
    欄位對照：
    - id: string (繼承自 BaseModel)
    - email: string
    - role: UserRole
    - created_at: string (繼承自 BaseModel，對應 createdAt)
    - updated_at: string (繼承自 BaseModel，對應 updatedAt)
    - is_active: boolean (對應 isActive)
    """
    __tablename__ = "users"
    
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.USER, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Bitfinex API (加密存儲)
    bitfinex_api_key = Column(String, nullable=True)
    bitfinex_api_secret = Column(String, nullable=True)
    
    # 關聯
    strategies = relationship("Strategy", back_populates="user", cascade="all, delete-orphan")
    offers = relationship("Offer", back_populates="user", cascade="all, delete-orphan")
    loans = relationship("Loan", back_populates="user", cascade="all, delete-orphan")
