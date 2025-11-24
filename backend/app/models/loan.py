"""
Loan Model

📚 學習重點：
1. 理解狀態機（Status）的設計
2. 理解時間戳欄位的使用

📖 參考文檔：
- docs/DATABASE.md
- @trading-robots/types (TypeScript 類型定義)

✅ 完整範例：models/user.py
"""

from sqlalchemy import Column, String, Boolean, ForeignKey, Numeric, DateTime, Enum
from sqlalchemy.orm import relationship
import enum
from app.models.base import BaseModel

class LoanStatus(str, enum.Enum):
    """
    借款狀態
    
    對應 TypeScript: LoanStatus
    """
    ACTIVE = "active"
    CLOSED = "closed"
    CANCELLED = "cancelled"

class Loan(BaseModel):
    """
    借款實體
    
    對應 TypeScript: Loan
    
    🔗 對應類型：@trading-robots/types/entities/loan.ts
    """
    __tablename__ = "loans"
    
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    offer_id = Column(String, ForeignKey("offers.id"), nullable=True)
    
    currency = Column(String, nullable=False)
    amount = Column(Numeric(20, 8), nullable=False)
    rate = Column(Numeric(10, 6), nullable=False)
    period = Column(Numeric(10, 2), nullable=False)
    
    status = Column(Enum(LoanStatus), default=LoanStatus.ACTIVE, nullable=False)
    
    started_at = Column(DateTime, nullable=True)
    closed_at = Column(DateTime, nullable=True)
    
    # 關聯
    user = relationship("User", back_populates="loans")

