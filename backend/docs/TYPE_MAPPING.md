# TypeScript ↔ Python 類型對照表

## 概述

本文檔說明如何確保前後端 API 類型定義完全一致。

- **前端類型定義**：`packages/types/src/` (TypeScript)
- **後端類型定義**：`backend/app/schemas/` (Python/Pydantic)

## 命名規範

### 欄位命名
| 位置 | 命名風格 | 範例 |
|-----|---------|------|
| TypeScript | camelCase | `createdAt`, `isActive`, `accessToken` |
| Python Schema | camelCase (alias) | `createdAt` (alias for `created_at`) |
| Python Model | snake_case | `created_at`, `is_active` |
| Database | snake_case | `created_at`, `is_active` |

### 實作方式
```python
# Python Schema 使用 alias 支援 camelCase
class UserResponse(BaseModel):
    createdAt: datetime = Field(..., alias="created_at")
    isActive: bool = Field(..., alias="is_active")
    
    class Config:
        from_attributes = True
        populate_by_name = True  # 允許兩種命名
```

## 統一響應格式

### TypeScript (packages/types/src/common/response.ts)
```typescript
interface ApiResponse<T> {
  success: boolean
  data?: T
  error?: ApiError
  message?: string
}
```

### Python (app/schemas/common.py)
```python
class ApiResponse(BaseModel, Generic[T]):
    success: bool
    data: Optional[T] = None
    error: Optional[ApiError] = None
    message: Optional[str] = None
```

## Auth 類型對照

### LoginRequest
| TypeScript | Python | 說明 |
|-----------|--------|------|
| `email: string` | `email: EmailStr` | Email 格式驗證 |
| `password: string` | `password: str` | 密碼 |

### LoginResponse
| TypeScript | Python | 說明 |
|-----------|--------|------|
| `accessToken: string` | `accessToken: str` | Access Token (camelCase) |
| `refreshToken: string` | `refreshToken: str` | Refresh Token (camelCase) |
| `user: User` | `user: UserResponse` | 用戶資訊 |

### RegisterRequest
| TypeScript | Python | 說明 |
|-----------|--------|------|
| `email: string` | `email: EmailStr` | Email |
| `password: string` | `password: str` | 密碼 |
| `confirmPassword: string` | `confirmPassword: str` | 確認密碼 |

## User 類型對照

### User Entity
| TypeScript | Python Model | Python Schema | 說明 |
|-----------|-------------|---------------|------|
| `id: string` | `id: str` | `id: str` | UUID |
| `email: string` | `email: str` | `email: str` | Email |
| `role: UserRole` | `role: UserRole` | `role: str` | 角色 |
| `createdAt: string` | `created_at: DateTime` | `createdAt: datetime` | 創建時間 |
| `updatedAt: string` | `updated_at: DateTime` | `updatedAt: datetime` | 更新時間 |
| `isActive: boolean` | `is_active: bool` | `isActive: bool` | 是否啟用 |

### UserRole
| TypeScript | Python |
|-----------|--------|
| `type UserRole = 'admin' \| 'user'` | `class UserRole(str, Enum): ADMIN = "admin"; USER = "user"` |

## 開發流程

### 添加新 API 時的類型檢查清單

1. ✅ 檢查 TypeScript 類型定義 (`packages/types/src/`)
2. ✅ 創建對應的 Python Schema (`app/schemas/`)
3. ✅ 確保欄位名稱使用 camelCase（使用 alias）
4. ✅ 確保所有 API 使用 `ApiResponse` 包裝響應
5. ✅ 撰寫測試驗證響應格式
6. ✅ 在 Schema 中添加類型對照註解

### 範例：添加 Strategy API

**Step 1: 查看 TypeScript 類型**
```typescript
// packages/types/src/entities/strategy.ts
interface Strategy {
  id: string
  userId: string
  strategyType: StrategyType
  params: StrategyParams
  isActive: boolean
  createdAt: string
  updatedAt: string
}
```

**Step 2: 創建 Python Schema**
```python
# app/schemas/strategy.py
"""
Strategy Schemas

🔗 對應 TypeScript：@trading-robots/types/entities/strategy.ts
"""

class StrategyResponse(BaseModel):
    id: str
    userId: str = Field(..., alias="user_id")
    strategyType: str = Field(..., alias="strategy_type")
    params: Dict[str, Any]
    isActive: bool = Field(..., alias="is_active")
    createdAt: datetime = Field(..., alias="created_at")
    updatedAt: datetime = Field(..., alias="updated_at")
    
    class Config:
        from_attributes = True
        populate_by_name = True
```

**Step 3: 使用 ApiResponse**
```python
# app/api/strategies.py
@router.get("/{strategy_id}", response_model=ApiResponse[StrategyResponse])
def get_strategy(strategy_id: str):
    strategy = ...
    return success_response(
        data=StrategyResponse.model_validate(strategy)
    )
```

## 常見錯誤

### ❌ 錯誤：直接返回數據
```python
@router.post("/login")
def login(...):
    return {"access_token": token, "user": user}  # ❌ 沒有包裝
```

### ✅ 正確：使用 ApiResponse
```python
@router.post("/login", response_model=ApiResponse[LoginResponse])
def login(...):
    return success_response(data=login_data)  # ✅
```

### ❌ 錯誤：使用 snake_case
```python
class LoginResponse(BaseModel):
    access_token: str  # ❌ 前端期望 accessToken
    user: dict        # ❌ 前端期望結構化類型
```

### ✅ 正確：使用 camelCase
```python
class LoginResponse(BaseModel):
    accessToken: str  # ✅
    refreshToken: str  # ✅
    user: UserResponse  # ✅
```

## 參考資源

- TypeScript 類型定義：`packages/types/src/`
- Python Schema：`app/schemas/`
- API 設計文檔：`docs/API_DESIGN.md`
- 完整範例：`app/api/auth.py`

