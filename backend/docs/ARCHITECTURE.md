# 架構說明

本文檔說明 Backend 的整體架構設計。

## 分層架構

```
┌─────────────────────────────────────┐
│         API Layer (api/)           │  ← FastAPI 路由層
│   - 處理 HTTP 請求/響應             │
│   - 參數驗證                        │
│   - 統一響應格式                    │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│      Service Layer (services/)      │  ← 業務邏輯層
│   - 業務邏輯實作                    │
│   - 資料處理                        │
│   - 外部 API 調用                   │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│       Model Layer (models/)         │  ← SQLAlchemy ORM
│   - 資料庫模型定義                  │
│   - 關聯關係                        │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│         Database                    │  ← PostgreSQL
└─────────────────────────────────────┘
```

## 各層職責

### API Layer (`app/api/`)

**職責：**
- 處理 HTTP 請求
- 參數驗證（透過 Pydantic Schema）
- 調用 Service 層
- 返回統一響應格式 (`ApiResponse<T>`)

**範例：**
```python
@router.post("/login", response_model=ApiResponse[LoginResponse])
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = auth_service.authenticate_user(db, request.email, request.password)
    # ...
    return success_response(data=login_response)
```

### Schema Layer (`app/schemas/`)

**職責：**
- 定義 API 請求/響應的資料結構
- 資料驗證規則
- 類型對照（TypeScript ↔ Python）

**範例：**
```python
class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)
```

### Service Layer (`app/services/`)

**職責：**
- 實作業務邏輯
- 與 Model 層互動
- 處理錯誤和異常

**範例：**
```python
def authenticate_user(db: Session, email: str, password: str) -> User:
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password_hash):
        return None
    return user
```

### Model Layer (`app/models/`)

**職責：**
- 定義資料庫表結構
- 定義關聯關係
- 提供 ORM 查詢介面

**範例：**
```python
class User(BaseModel):
    __tablename__ = "users"
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
```

## 資料流向

### 請求流程

```
1. HTTP Request
   ↓
2. API Router (api/auth.py)
   ↓
3. Schema Validation (schemas/auth.py)
   ↓
4. Service Layer (services/auth.py)
   ↓
5. Model Layer (models/user.py)
   ↓
6. Database
```

### 響應流程

```
1. Database
   ↓
2. Model Layer (ORM Object)
   ↓
3. Service Layer (Business Logic)
   ↓
4. Schema Layer (Pydantic Model)
   ↓
5. API Response (ApiResponse<T>)
   ↓
6. HTTP Response
```

## 依賴注入（Depends）

FastAPI 使用依賴注入來管理共用資源：

```python
# 資料庫 session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 當前用戶
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    # ...
    return user

# 使用
@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    return current_user
```

## 錯誤處理機制

### 統一錯誤響應

所有錯誤都使用 `ApiResponse` 包裝：

```python
# 成功響應
return success_response(data=user_data, message="Success")

# 錯誤響應
return error_response(
    code="INVALID_CREDENTIALS",
    message="Email or password is incorrect"
)
```

### HTTP 異常

對於需要特定 HTTP 狀態碼的情況：

```python
raise HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials"
)
```

## 目錄結構

```
backend/
├── app/
│   ├── api/              # API 路由層
│   │   ├── auth.py       # Auth API
│   │   ├── deps.py       # 共用依賴
│   │   └── ...
│   ├── core/             # 核心基礎設施
│   │   ├── config.py     # 配置
│   │   ├── database.py   # 資料庫連接
│   │   └── security.py   # 安全相關
│   ├── models/           # ORM 模型
│   │   ├── base.py       # Base Model
│   │   ├── user.py       # User Model
│   │   └── ...
│   ├── schemas/          # Pydantic Schemas
│   │   ├── common.py     # 統一響應格式
│   │   ├── auth.py       # Auth Schemas
│   │   └── ...
│   └── services/         # 業務邏輯層
│       ├── auth.py       # Auth Service
│       └── ...
├── tests/                # 測試
├── alembic/              # 資料庫遷移
└── docs/                 # 文檔
```

## 設計原則

1. **單一職責**：每個層級只負責自己的職責
2. **依賴注入**：使用 FastAPI 的 Depends 管理依賴
3. **統一響應格式**：所有 API 使用 `ApiResponse<T>`
4. **類型安全**：使用 Pydantic 進行類型驗證
5. **文檔優先**：每個函數都有清晰的文檔字串

## 參考資源

- [FastAPI 官方文檔](https://fastapi.tiangolo.com/)
- [SQLAlchemy 文檔](https://docs.sqlalchemy.org/)
- [Pydantic 文檔](https://docs.pydantic.dev/)

