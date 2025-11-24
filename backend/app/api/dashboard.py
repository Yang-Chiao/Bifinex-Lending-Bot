"""
Dashboard API Routes

使用目前登入用戶的 Bitfinex API Key 呼叫 Bitfinex API，提供：
- 帳戶餘額
- 收益資訊
- 借款狀況與明細
- 完整帳戶資訊
- Bitfinex 用戶基本資訊
"""

from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.deps import get_current_user, get_bitfinex_client
from app.models.user import User
from app.schemas.common import ApiResponse, success_response, error_response
from app.schemas.dashboard import (
    AccountBalance,
    EarningsInfo,
    LoanStatus,
    LoanDetail,
    UserAccountInfo,
)
from app.services.bitfinex_client import BitfinexClient

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/balance", response_model=ApiResponse[AccountBalance])
async def get_account_balance(
    client: BitfinexClient = Depends(get_bitfinex_client),
) -> ApiResponse[AccountBalance]:
    """
    獲取帳戶餘額

    - 返回所有錢包的餘額資訊
    - 包括 exchange、margin、funding 錢包
    """
    try:
        summary = client.get_account_summary()
        balance = AccountBalance(
            total_balance=summary.get("total_balance", {}),
            funding_balance=summary.get("funding_balance", {}),
            wallets=summary.get("wallets", []),
        )
        return success_response(data=balance, message="取得帳戶餘額成功")
    except Exception as e:
        return error_response(
            code="BITFINEX_BALANCE_FAILED",
            message=f"獲取餘額失敗: {str(e)}",
        )


@router.get("/earnings", response_model=ApiResponse[EarningsInfo])
async def get_earnings(
    currency: str = "USD",
    client: BitfinexClient = Depends(get_bitfinex_client),
) -> ApiResponse[EarningsInfo]:
    """
    獲取收益資訊

    - 總收益
    - 今日收益
    - 本月收益
    - 各筆借款的收益明細
    """
    try:
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

                if amount > 0:
                    earnings = amount * rate * period / 365.0 / 100.0
                    total_earnings += earnings

                    trade_time = datetime.fromtimestamp(created_at_ms / 1000) if created_at_ms else now

                    if trade_time >= today_start:
                        today_earnings += earnings

                    if trade_time >= month_start:
                        monthly_earnings += earnings

                    earnings_by_loan.append(
                        {
                            "trade_id": trade_id,
                            "amount": amount,
                            "rate": rate,
                            "period": period,
                            "earnings": earnings,
                            "created_at": trade_time.isoformat(),
                        }
                    )

        earnings_info = EarningsInfo(
            total_earnings=total_earnings,
            today_earnings=today_earnings,
            monthly_earnings=monthly_earnings,
            currency=currency,
            earnings_by_loan=earnings_by_loan,
        )
        return success_response(data=earnings_info, message="取得收益資訊成功")
    except Exception as e:
        return error_response(
            code="BITFINEX_EARNINGS_FAILED",
            message=f"獲取收益失敗: {str(e)}",
        )


@router.get("/loans", response_model=ApiResponse[LoanStatus])
async def get_loans(
    currency: str = "USD",
    client: BitfinexClient = Depends(get_bitfinex_client),
) -> ApiResponse[LoanStatus]:
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

                amount = loan.get("amount", 0)
                rate = loan.get("rate", 0)
                period = loan.get("period", 0)
                if amount > 0 and rate > 0 and period > 0:
                    earnings = amount * rate * period / 365.0 / 100.0
                    loan["earnings"] = earnings
                    total_earnings += earnings

        avg_rate = total_rate / len(active_loans) if active_loans else 0.0

        loan_details = []
        for loan in active_loans:
            created_at_ms = loan.get("created_at", 0)
            created_at = (
                datetime.fromtimestamp(created_at_ms / 1000)
                if created_at_ms
                else datetime.now()
            )

            loan_details.append(
                LoanDetail(
                    id=loan.get("id"),
                    symbol=loan.get("symbol", ""),
                    side=loan.get("side", ""),
                    created_at=created_at,
                    amount=loan.get("amount", 0),
                    rate=loan.get("rate", 0),
                    period=loan.get("period", 0),
                    status=loan.get("status"),
                    earnings=loan.get("earnings"),
                )
            )

        status_data = LoanStatus(
            total_loans=len(loans_data),
            active_loans=len(active_loans),
            total_amount=total_amount,
            average_rate=avg_rate,
            total_earnings=total_earnings,
            loans=loan_details,
        )
        return success_response(data=status_data, message="取得借款狀況成功")
    except Exception as e:
        return error_response(
            code="BITFINEX_LOANS_FAILED",
            message=f"獲取借款狀況失敗: {str(e)}",
        )


@router.get("/account-info", response_model=ApiResponse[UserAccountInfo])
async def get_account_info(
    currency: str = "USD",
    current_user: User = Depends(get_current_user),
    client: BitfinexClient = Depends(get_bitfinex_client),
) -> ApiResponse[UserAccountInfo]:
    """
    獲取完整的帳戶資訊

    - 包含餘額、收益、借款狀況
    - 一次性返回所有資訊，減少 API 呼叫
    """
    try:
        balance_resp = await get_account_balance(client)
        earnings_resp = await get_earnings(currency, client)
        loans_resp = await get_loans(currency, client)

        if not balance_resp.success or not earnings_resp.success or not loans_resp.success:
            # 任何一個子呼叫失敗時回傳錯誤
            return error_response(
                code="ACCOUNT_INFO_FAILED",
                message="無法取得完整帳戶資訊",
            )

        account_info = UserAccountInfo(
            user_id=str(current_user.id),
            email=current_user.email,
            balance=balance_resp.data,  # type: ignore[arg-type]
            earnings=earnings_resp.data,  # type: ignore[arg-type]
            loan_status=loans_resp.data,  # type: ignore[arg-type]
            last_updated=datetime.now(),
        )
        return success_response(data=account_info, message="取得帳戶完整資訊成功")
    except Exception as e:
        return error_response(
            code="ACCOUNT_INFO_FAILED",
            message=f"獲取帳戶資訊失敗: {str(e)}",
        )


@router.get("/user-info", response_model=ApiResponse[dict])
async def get_user_info(
    client: BitfinexClient = Depends(get_bitfinex_client),
) -> ApiResponse[dict]:
    """
    獲取 Bitfinex 用戶基本資訊

    - 使用 Bitfinex API Key 直接回傳 Bitfinex API 的原始用戶資料
    """
    try:
        user_info = client.get_user_info()
        return success_response(data=user_info, message="取得 Bitfinex 用戶資訊成功")
    except Exception as e:
        return error_response(
            code="BITFINEX_USER_INFO_FAILED",
            message=f"獲取用戶資訊失敗: {str(e)}",
        )


