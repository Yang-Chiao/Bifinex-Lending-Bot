from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime, timedelta
from app.core.database import get_db
from app.api.dependencies import get_current_user, get_bitfinex_client
from app.models.user import User
from app.schemas.dashboard import (
    AccountBalance,
    EarningsInfo,
    LoanStatus,
    LoanDetail,
    UserAccountInfo
)
from app.services.bitfinex_client import BitfinexClient

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/balance", response_model=AccountBalance)
async def get_account_balance(
    client: BitfinexClient = Depends(get_bitfinex_client)
):
    """
    獲取帳戶餘額
    - 返回所有錢包的餘額資訊
    - 包括 exchange, margin, funding 錢包
    """
    try:
        summary = client.get_account_summary()
        return AccountBalance(
            total_balance=summary.get("total_balance", {}),
            funding_balance=summary.get("funding_balance", {}),
            wallets=summary.get("wallets", [])
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"獲取餘額失敗: {str(e)}")


@router.get("/earnings", response_model=EarningsInfo)
async def get_earnings(
    currency: str = "USD",
    client: BitfinexClient = Depends(get_bitfinex_client)
):
    """
    獲取收益資訊
    - 總收益
    - 今日收益
    - 本月收益
    - 各筆借款的收益明細
    """
    try:
        # 獲取資金交易歷史
        trades = client.get_funding_trades(currency)
        
        now = datetime.now()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        total_earnings = 0.0
        today_earnings = 0.0
        monthly_earnings = 0.0
        earnings_by_loan = []
        
        for trade in trades:
            if isinstance(trade, list) and len(trade) >= 8:
                # Bitfinex funding trade 格式:
                # [ID, CURRENCY, MTS_CREATE, OFFER_ID, AMOUNT, RATE, PERIOD, MTS_FUNDING]
                trade_id = trade[0]
                amount = trade[4] if len(trade) > 4 else 0
                rate = trade[5] if len(trade) > 5 else 0
                period = trade[6] if len(trade) > 6 else 0
                created_at_ms = trade[7] if len(trade) > 7 else 0
                
                # 計算收益（簡化計算，實際可能需要更複雜的邏輯）
                if amount > 0:  # 出借金額
                    earnings = amount * rate * period / 365.0 / 100.0
                    total_earnings += earnings
                    
                    # 轉換時間戳
                    trade_time = datetime.fromtimestamp(created_at_ms / 1000)
                    
                    if trade_time >= today_start:
                        today_earnings += earnings
                    
                    if trade_time >= month_start:
                        monthly_earnings += earnings
                    
                    earnings_by_loan.append({
                        "trade_id": trade_id,
                        "amount": amount,
                        "rate": rate,
                        "period": period,
                        "earnings": earnings,
                        "created_at": trade_time.isoformat()
                    })
        
        return EarningsInfo(
            total_earnings=total_earnings,
            today_earnings=today_earnings,
            monthly_earnings=monthly_earnings,
            currency=currency,
            earnings_by_loan=earnings_by_loan
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"獲取收益失敗: {str(e)}")


@router.get("/loans", response_model=LoanStatus)
async def get_loans(
    currency: str = "USD",
    client: BitfinexClient = Depends(get_bitfinex_client)
):
    """
    獲取借款狀況
    - 活躍借款數量
    - 總借款金額
    - 平均利率
    - 借款明細列表
    """
    try:
        loans_data = client.get_loans(currency)
        
        active_loans = []
        total_amount = 0.0
        total_rate = 0.0
        total_earnings = 0.0
        
        for loan in loans_data:
            if loan.get("status") == "ACTIVE" or loan.get("amount", 0) > 0:
                active_loans.append(loan)
                total_amount += loan.get("amount", 0)
                total_rate += loan.get("rate", 0)
                
                # 簡單計算收益
                amount = loan.get("amount", 0)
                rate = loan.get("rate", 0)
                period = loan.get("period", 0)
                if amount > 0 and rate > 0 and period > 0:
                    earnings = amount * rate * period / 365.0 / 100.0
                    loan["earnings"] = earnings
                    total_earnings += earnings
        
        avg_rate = total_rate / len(active_loans) if active_loans else 0.0
        
        # 轉換為 LoanDetail 模型
        loan_details = []
        for loan in active_loans:
            created_at_ms = loan.get("created_at", 0)
            created_at = datetime.fromtimestamp(created_at_ms / 1000) if created_at_ms > 0 else datetime.now()
            
            loan_details.append(LoanDetail(
                id=loan.get("id"),
                symbol=loan.get("symbol", ""),
                side=loan.get("side", ""),
                created_at=created_at,
                amount=loan.get("amount", 0),
                rate=loan.get("rate", 0),
                period=loan.get("period", 0),
                status=loan.get("status"),
                earnings=loan.get("earnings")
            ))
        
        return LoanStatus(
            total_loans=len(loans_data),
            active_loans=len(active_loans),
            total_amount=total_amount,
            average_rate=avg_rate,
            total_earnings=total_earnings,
            loans=loan_details
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"獲取借款狀況失敗: {str(e)}")


@router.get("/account-info", response_model=UserAccountInfo)
async def get_account_info(
    currency: str = "USD",
    current_user: User = Depends(get_current_user),
    client: BitfinexClient = Depends(get_bitfinex_client)
):
    """
    獲取完整的帳戶資訊
    - 包含餘額、收益、借款狀況
    - 一次性返回所有資訊，減少 API 調用
    """
    try:
        # 獲取所有資訊
        balance_data = await get_account_balance(client)
        earnings_data = await get_earnings(currency, client)
        loans_data = await get_loans(currency, client)
        
        return UserAccountInfo(
            user_id=current_user.id,
            email=current_user.email,
            balance=balance_data,
            earnings=earnings_data,
            loan_status=loans_data,
            last_updated=datetime.now()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"獲取帳戶資訊失敗: {str(e)}")


@router.get("/user-info")
async def get_user_info(
    client: BitfinexClient = Depends(get_bitfinex_client)
):
    """
    獲取 Bitfinex 用戶基本資訊
    - 使用 Bitfinex API Key 獲取用戶資料
    """
    try:
        user_info = client.get_user_info()
        return user_info
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"獲取用戶資訊失敗: {str(e)}")
