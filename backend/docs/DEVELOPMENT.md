# 新手開發指南

本文檔為新手開發者提供 Step-by-Step 的開發指南。

## 如何添加新 API 端點

### Step 1: 定義 Model（models/）

在 `app/models/` 中定義資料庫模型：

```python
# app/models/strategy.py
from app.models.base import BaseModel
from sqlalchemy import Column, String, ForeignKey

class Strategy(BaseModel):
    __tablename__ = "strategies"
    
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    strategy_type = Column(String, nullable=False)
    # ...
```

### Step 2: 創建 Schema（schemas/）

在 `app/schemas/` 中定義請求/響應 Schema：

```python
# app/schemas/strategy.py
from pydantic import BaseModel, Field
from datetime import datetime

class StrategyCreate(BaseModel):
    strategy_type: str
    # ...

class StrategyResponse(BaseModel):
    id: str
    userId: str = Field(..., alias="user_id")
    createdAt: datetime = Field(..., alias="created_at")
    # ...
    
    class Config:
        from_attributes = True
        populate_by_name = True
```

**💡 重要：**
- 使用 `alias` 支援 camelCase（對應前端）
- 添加 `🔗 對應 TypeScript` 註解

### Step 3: 實作 Service（services/）

在 `app/services/` 中實作業務邏輯：

```python
# app/services/strategy.py
from sqlalchemy.orm import Session
from app.models.strategy import Strategy

def create_strategy(db: Session, user_id: str, strategy_data: dict) -> Strategy:
    strategy = Strategy(
        user_id=user_id,
        **strategy_data
    )
    db.add(strategy)
    db.commit()
    db.refresh(strategy)
    return strategy
```

### Step 4: 添加 API（api/）

在 `app/api/` 中添加路由：

```python
# app/api/strategies.py
from fastapi import APIRouter, Depends
from app.schemas.common import ApiResponse, success_response
from app.schemas.strategy import StrategyCreate, StrategyResponse
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter()

@router.post("/strategies", response_model=ApiResponse[StrategyResponse])
def create_strategy(
    request: StrategyCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    strategy = strategy_service.create_strategy(
        db, current_user.id, request.dict()
    )
    return success_response(
        data=StrategyResponse.model_validate(strategy),
        message="Strategy created successfully"
    )
```

**💡 重要：**
- 使用 `ApiResponse<T>` 包裝響應
- 使用 `success_response()` 或 `error_response()` 便捷函數

### Step 5: 註冊路由（main.py）

在 `app/main.py` 中註冊路由：

```python
from app.api import strategies

app.include_router(strategies.router, prefix="/api", tags=["Strategies"])
```

### Step 6: 寫測試（tests/）

在 `tests/` 中撰寫測試：

```python
# tests/test_strategies.py
def test_create_strategy(client: TestClient):
    # 先登入獲取 token
    login_response = client.post("/api/auth/login", json={...})
    token = login_response.json()["data"]["accessToken"]
    
    # 創建策略
    response = client.post(
        "/api/strategies",
        json={"strategy_type": "market_follow"},
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "data" in data
```

### Step 7: 運行驗證

```bash
# 運行測試
pytest tests/test_strategies.py

# 啟動服務器測試
uvicorn app.main:app --reload
```

## 如何寫測試

### 使用 pytest

```python
import pytest
from fastapi.testclient import TestClient

def test_example(client: TestClient):
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["success"] is True
```

### 測試認證 API

```python
def test_login(client: TestClient):
    # 先註冊
    client.post("/api/auth/register", json={...})
    
    # 登入
    response = client.post("/api/auth/login", json={...})
    assert response.status_code == 200
    assert "accessToken" in response.json()["data"]
```

### 測試需要認證的 API

```python
def test_get_strategies(client: TestClient):
    # 登入獲取 token
    login_response = client.post("/api/auth/login", json={...})
    token = login_response.json()["data"]["accessToken"]
    
    # 使用 token 訪問 API
    response = client.get(
        "/api/strategies",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
```

## 常見問題排查

### 問題 1: 模組導入錯誤

**錯誤訊息：**
```
ModuleNotFoundError: No module named 'app'
```

**解決方案：**
1. 確認在專案根目錄運行
2. 確認虛擬環境已啟動
3. 檢查 `PYTHONPATH` 環境變數

### 問題 2: 資料庫連接失敗

**錯誤訊息：**
```
sqlalchemy.exc.OperationalError: could not connect to server
```

**解決方案：**
1. 確認 PostgreSQL 服務正在運行
2. 檢查 `.env` 中的 `DATABASE_URL`
3. 確認資料庫已創建

### 問題 3: 類型驗證錯誤

**錯誤訊息：**
```
pydantic.ValidationError: 1 validation error for LoginRequest
```

**解決方案：**
1. 檢查請求資料格式
2. 確認 Schema 定義正確
3. 查看詳細錯誤訊息

## Debug 技巧

### 使用 print 調試

```python
@router.post("/login")
def login(request: LoginRequest):
    print(f"Request: {request.dict()}")  # 調試用
    # ...
```

### 使用 FastAPI 的依賴注入調試

```python
from fastapi import Request

@router.post("/login")
def login(request: Request):
    print(f"Headers: {request.headers}")
    print(f"Body: {await request.body()}")
```

### 使用資料庫查詢調試

```python
# 在 Python shell 中
from app.core.database import SessionLocal
from app.models.user import User

db = SessionLocal()
users = db.query(User).all()
print(users)
```

## Git 工作流程

### 1. 創建分支

```bash
git checkout -b feature/add-strategy-api
```

### 2. 開發和提交

```bash
# 添加檔案
git add .

# 提交（使用清晰的訊息）
git commit -m "feat: add strategy API endpoints"

# 推送
git push origin feature/add-strategy-api
```

### 3. 創建 Pull Request

在 GitHub/GitLab 上創建 PR，等待 Code Review。

### 提交訊息規範

- `feat:` 新功能
- `fix:` 修復 bug
- `docs:` 文檔更新
- `refactor:` 重構
- `test:` 測試相關

## 類型一致性檢查清單

添加新 API 時，確保：

1. ✅ Schema 使用 camelCase（透過 alias）
2. ✅ 所有 API 使用 `ApiResponse<T>` 包裝
3. ✅ 添加 `🔗 對應 TypeScript` 註解
4. ✅ 撰寫測試驗證響應格式
5. ✅ 更新 `TYPE_MAPPING.md`（如需要）

## 參考資源

- [FastAPI 教程](https://fastapi.tiangolo.com/tutorial/)
- [Pydantic 文檔](https://docs.pydantic.dev/)
- [類型對照](./TYPE_MAPPING.md)
- [API 設計規範](./API_DESIGN.md)

