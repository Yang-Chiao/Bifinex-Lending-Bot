"""
Strategy Model

📚 學習重點：
1. 理解 SQLAlchemy ORM 模型定義
2. 理解關聯（Relationship）的使用
3. 理解 Enum 類型的使用

📖 參考文檔：
- docs/DATABASE.md
- docs/ARCHITECTURE.md
- @trading-robots/types (TypeScript 類型定義)

✅ 完整範例：models/user.py
"""

from sqlalchemy import Column, String, Boolean, Enum, Text, ForeignKey
from sqlalchemy.orm import relationship
import enum
import json
from app.models.base import BaseModel

class StrategyType(str, enum.Enum):
    """
    策略類型
    
    對應 TypeScript: StrategyType
    """
    MARKET_FOLLOW = "market_follow"
    LADDER = "ladder"
    FIXED_RATE = "fixed_rate"

class Strategy(BaseModel):
    """
    策略實體
    
    對應 TypeScript: Strategy
    
    💡 提示：
    1. 繼承自 BaseModel（獲得 id, created_at, updated_at）
    2. 使用 relationship 定義與 User 的關聯
    3. params 欄位存儲 JSON 字串（根據 strategy_type 不同而不同）
    
    🔗 對應類型：@trading-robots/types/entities/strategy.ts
    """
    __tablename__ = "strategies"
    
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    strategy_type = Column(Enum(StrategyType), nullable=False)
    params = Column(Text, nullable=False)  # JSON 字串
    is_active = Column(Boolean, default=True, nullable=False)
    
    # 關聯
    user = relationship("User", back_populates="strategies")
    offers = relationship("Offer", back_populates="strategy", cascade="all, delete-orphan")

