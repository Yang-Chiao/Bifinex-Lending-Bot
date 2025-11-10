from pydantic import BaseModel
from typing import Dict, List, Optional, Any
from datetime import datetime


class BalanceInfo(BaseModel):
    """餘額資訊"""
    currency: str
    amount: float
    wallet_type: str  # exchange, margin, funding


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
    user_id: int
    email: str
    balance: AccountBalance
    earnings: EarningsInfo
    loan_status: LoanStatus
    last_updated: datetime
