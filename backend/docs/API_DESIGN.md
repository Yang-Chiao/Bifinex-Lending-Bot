# API 設計規範

本文檔說明 Backend API 的設計規範和最佳實踐。

## RESTful API 最佳實踐

### URL 設計

- 使用名詞，不使用動詞
- 使用複數形式
- 使用小寫字母和連字號

**範例：**
```
✅ GET /api/strategies
✅ POST /api/strategies
✅ GET /api/strategies/{id}
✅ PUT /api/strategies/{id}
✅ DELETE /api/strategies/{id}

❌ GET /api/getStrategies
❌ POST /api/createStrategy
```

### HTTP 方法

| 方法 | 用途 | 範例 |
|-----|------|------|
| GET | 獲取資源 | `GET /api/strategies` |
| POST | 創建資源 | `POST /api/strategies` |
| PUT | 完整更新資源 | `PUT /api/strategies/{id}` |
| PATCH | 部分更新資源 | `PATCH /api/strategies/{id}` |
| DELETE | 刪除資源 | `DELETE /api/strategies/{id}` |

## HTTP 狀態碼使用規範

| 狀態碼 | 用途 | 範例 |
|--------|------|------|
| 200 | 成功 | GET, PUT, PATCH 成功 |
| 201 | 創建成功 | POST 創建資源成功 |
| 400 | 請求錯誤 | 參數驗證失敗 |
| 401 | 未授權 | Token 無效或過期 |
| 403 | 禁止訪問 | 權限不足 |
| 404 | 資源不存在 | 找不到指定的資源 |
| 500 | 伺服器錯誤 | 內部錯誤 |

## 統一響應格式

### 成功響應

所有 API 都使用 `ApiResponse<T>` 包裝：

```json
{
  "success": true,
  "data": {
    "id": "123",
    "email": "user@example.com"
  },
  "message": "Operation successful"
}
```

### 錯誤響應

```json
{
  "success": false,
  "error": {
    "code": "INVALID_CREDENTIALS",
    "message": "Email or password is incorrect",
    "details": {
      "field": "email"
    }
  }
}
```

### 實作方式

```python
from app.schemas.common import ApiResponse, success_response, error_response

@router.post("/login", response_model=ApiResponse[LoginResponse])
def login(request: LoginRequest):
    # 成功
    return success_response(
        data=login_data,
        message="Login successful"
    )
    
    # 錯誤
    return error_response(
        code="INVALID_CREDENTIALS",
        message="Email or password is incorrect"
    )
```

## 分頁、排序、篩選規範

### 分頁

```python
@router.get("/strategies")
def get_strategies(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    offset = (page - 1) * page_size
    strategies = db.query(Strategy).offset(offset).limit(page_size).all()
    total = db.query(Strategy).count()
    
    return success_response(data={
        "items": strategies,
        "total": total,
        "page": page,
        "page_size": page_size
    })
```

### 排序

```python
@router.get("/strategies")
def get_strategies(
    sort_by: str = Query("created_at"),
    order: str = Query("desc"),  # asc or desc
    db: Session = Depends(get_db)
):
    order_func = desc if order == "desc" else asc
    strategies = db.query(Strategy).order_by(order_func(getattr(Strategy, sort_by))).all()
    return success_response(data=strategies)
```

### 篩選

```python
@router.get("/strategies")
def get_strategies(
    is_active: Optional[bool] = None,
    strategy_type: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Strategy)
    
    if is_active is not None:
        query = query.filter(Strategy.is_active == is_active)
    if strategy_type:
        query = query.filter(Strategy.strategy_type == strategy_type)
    
    strategies = query.all()
    return success_response(data=strategies)
```

## API 端點命名規則

### 資源端點

```
GET    /api/strategies          # 獲取列表
POST   /api/strategies          # 創建
GET    /api/strategies/{id}     # 獲取單個
PUT    /api/strategies/{id}     # 完整更新
PATCH  /api/strategies/{id}     # 部分更新
DELETE /api/strategies/{id}     # 刪除
```

### 動作端點

對於非 CRUD 操作，使用動詞：

```
POST /api/strategies/{id}/activate
POST /api/strategies/{id}/deactivate
POST /api/auth/login
POST /api/auth/register
POST /api/auth/refresh
```

## 請求/響應範例

### 註冊用戶

**請求：**
```http
POST /api/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePass123!",
  "confirmPassword": "SecurePass123!"
}
```

**響應：**
```json
{
  "success": true,
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "role": "user",
    "createdAt": "2024-01-01T00:00:00",
    "updatedAt": "2024-01-01T00:00:00",
    "isActive": true
  },
  "message": "User created successfully"
}
```

### 登入

**請求：**
```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePass123!"
}
```

**響應：**
```json
{
  "success": true,
  "data": {
    "accessToken": "eyJhbGciOiJIUzI1NiIs...",
    "refreshToken": "eyJhbGciOiJIUzI1NiIs...",
    "user": {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "email": "user@example.com",
      "role": "user",
      "createdAt": "2024-01-01T00:00:00",
      "updatedAt": "2024-01-01T00:00:00",
      "isActive": true
    }
  },
  "message": "Login successful"
}
```

## 認證和授權

### Bearer Token

所有需要認證的 API 都需要在 Header 中攜帶 Token：

```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

### 實作方式

```python
from app.api.deps import get_current_user

@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    return success_response(data=current_user)
```

## 錯誤處理

### 驗證錯誤

當請求參數不符合 Schema 定義時，FastAPI 會自動返回 422：

```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

### 業務邏輯錯誤

使用 `error_response` 返回：

```python
if not user:
    return error_response(
        code="INVALID_CREDENTIALS",
        message="Email or password is incorrect"
    )
```

## 版本控制

目前使用 `/api` 作為 API 前綴。未來如果需要版本控制：

```
/api/v1/strategies
/api/v2/strategies
```

## 參考資源

- [RESTful API 設計指南](https://restfulapi.net/)
- [FastAPI 文檔](https://fastapi.tiangolo.com/)
- [統一響應格式](./TYPE_MAPPING.md)

