"""
Loans API Routes

📚 學習重點：
參考 api/strategies.py 的註解說明

✅ 完整範例：api/auth.py
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.common import ApiResponse

router = APIRouter()

# TODO: 實作借款相關的 API 端點
pass

