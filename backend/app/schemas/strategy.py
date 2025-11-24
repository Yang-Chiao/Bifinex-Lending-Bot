"""
策略相關的 Pydantic Schemas

📚 學習重點：
1. 理解 Schema 的作用（資料驗證、API 文檔生成）
2. 學會使用 Field() 設定驗證規則
3. 理解請求/響應分離設計

📖 參考文檔：
- docs/API_DESIGN.md
- docs/DATABASE.md
- @trading-robots/types (TypeScript 類型定義)

✅ 完整範例：schemas/user.py, schemas/auth.py
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime

# TODO: 實作策略基礎 Schema
class StrategyBase(BaseModel):
    """
    策略的共用欄位
    
    欄位說明：
    - strategy_type: str - 策略類型（market_follow, ladder, fixed_rate）
    - params: dict - 策略參數（根據 strategy_type 不同而不同）
    - is_active: bool - 是否啟用
    
    💡 提示：
    1. 使用 Field() 設定預設值和驗證規則
    2. params 欄位可以用 Dict[str, Any] 類型
    3. 參考 docs/DATABASE.md 的 strategies 表定義
    
    🔗 對應類型：@trading-robots/types/entities/strategy.ts
    """
    # TODO: 在這裡添加欄位定義
    # strategy_type: str = Field(...)
    # params: Dict[str, Any] = Field(...)
    # is_active: bool = Field(default=True)
    pass

# TODO: 實作創建策略的請求 Schema
class StrategyCreate(StrategyBase):
    """
    創建策略的請求資料
    
    💡 提示：
    - 繼承自 StrategyBase
    - 所有必要欄位都不能為空
    - 可以添加額外的驗證邏輯
    
    📝 範例（參考 schemas/auth.py 的 RegisterRequest）
    """
    pass

# TODO: 實作更新策略的請求 Schema
class StrategyUpdate(BaseModel):
    """
    更新策略的請求資料
    
    💡 提示：
    - 更新時所有欄位都是可選的（partial update）
    - 使用 Optional[] 包裹每個欄位
    
    ❓ 思考：為什麼不繼承 StrategyBase？
    答：因為更新時不需要所有欄位都提供
    """
    pass

# TODO: 實作策略響應 Schema
class Strategy(StrategyBase):
    """
    API 回傳的策略資料
    
    💡 提示：
    - 繼承自 StrategyBase
    - 添加自動生成的欄位：id, user_id, created_at, updated_at
    - 設定 Config.from_attributes = True（從 ORM 模型轉換）
    - 使用 alias 支援 camelCase（如 userId, createdAt）
    
    📝 範例（參考 schemas/user.py 的 UserResponse）
    """
    # TODO: 添加額外欄位
    # id: str
    # userId: str = Field(..., alias="user_id")
    # createdAt: datetime = Field(..., alias="created_at")
    # updatedAt: datetime = Field(..., alias="updated_at")
    
    # class Config:
    #     from_attributes = True
    #     populate_by_name = True
    pass

