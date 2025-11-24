"""
Offer Model

📚 學習重點：
1. 理解外鍵（ForeignKey）的使用
2. 理解 Decimal 類型用於金額
3. 理解關聯關係

📖 參考文檔：
- docs/DATABASE.md
- @trading-robots/types (TypeScript 類型定義)

✅ 完整範例：models/user.py
"""

from sqlalchemy import Column, String, Boolean, ForeignKey, Numeric, DateTime
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class Offer(BaseModel):
    """
    放貸報價實體
    
    對應 TypeScript: Offer
    
    🔗 對應類型：@trading-robots/types/entities/offer.ts
    """
    __tablename__ = "offers"
    
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    strategy_id = Column(String, ForeignKey("strategies.id"), nullable=True, index=True)
    
    currency = Column(String, nullable=False)
    amount = Column(Numeric(20, 8), nullable=False)
    rate = Column(Numeric(10, 6), nullable=False)
    period = Column(Numeric(10, 2), nullable=False)  # 天數
    
    is_active = Column(Boolean, default=True, nullable=False)
    expires_at = Column(DateTime, nullable=True)
    
    # 關聯
    user = relationship("User", back_populates="offers")
    strategy = relationship("Strategy", back_populates="offers")

