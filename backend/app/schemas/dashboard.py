"""
Dashboard Schemas

從舊專案移植並調整為目前結構使用：
- 提供帳戶餘額、收益、借款狀況與完整帳戶資訊的資料模型
"""

from pydantic import BaseModel
from typing import Dict, List, Optional, Any
from datetime import datetime


class AccountBalance(BaseModel):
    """帳戶餘額"""
    total_balance: Dict[str, float]
    funding_balance: Dict[str, float]
    wallets: List[Dict[str, Any]]


class LoanDetail(BaseModel):
    """借款明細"""
    id: int
    symbol: str
    side: str
    created_at: datetime
    amount: float
    rate: float
    period: int
    status: Optional[str] = None
    earnings: Optional[float] = None


class LoanStatus(BaseModel):
    """借款狀況"""
    total_loans: int
    active_loans: int
    total_amount: float
    average_rate: float
    total_earnings: float
    loans: List[LoanDetail]


class EarningsInfo(BaseModel):
    """收益資訊"""
    total_earnings: float
    today_earnings: float
    monthly_earnings: float
    currency: str = "USD"
    earnings_by_loan: List[Dict[str, Any]]


class UserAccountInfo(BaseModel):
    """用戶帳戶完整資訊"""
    user_id: str
    email: str
    balance: AccountBalance
    earnings: EarningsInfo
    loan_status: LoanStatus
    last_updated: datetime


