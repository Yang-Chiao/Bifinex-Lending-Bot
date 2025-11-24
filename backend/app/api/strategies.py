"""
Strategies API Routes

📚 學習重點：
1. 理解 API 路由的設計
2. 理解統一響應格式的使用
3. 理解依賴注入的使用

📖 參考文檔：
- docs/API_DESIGN.md
- docs/DEVELOPMENT.md

✅ 完整範例：api/auth.py
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.common import ApiResponse

router = APIRouter()

# TODO: 實作策略相關的 API 端點
# 參考 api/auth.py 的結構
# 包含：GET /strategies, POST /strategies, PUT /strategies/{id}, DELETE /strategies/{id}

@router.get("/strategies", response_model=ApiResponse[list])
def get_strategies(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    獲取當前用戶的所有策略
    
    對應 TypeScript API：GET /api/strategies
    """
    # TODO: 實作邏輯
    pass

