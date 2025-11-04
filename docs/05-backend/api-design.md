# API 設計文檔

## 🌐 API 基礎資訊

```
Base URL: https://api.yourdomain.com/api
Version: v1
Protocol: HTTPS
Auth: Bearer Token (JWT)
Content-Type: application/json
```

---

## 🔐 認證 API

### POST /auth/login
登入獲取 JWT Token

**Request:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response 200:**
```json
{
  "user": {
    "id": 1,
    "email": "user@example.com",
    "role": "user"
  },
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response 401:**
```json
{
  "detail": "Incorrect email or password"
}
```

---

### POST /auth/register
用戶註冊

**Request:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response 201:**
```json
{
  "user": {
    "id": 1,
    "email": "user@example.com",
    "role": "user"
  },
  "message": "User created successfully"
}
```

---

### GET /auth/me
獲取當前用戶資訊

**Headers:**
```
Authorization: Bearer <token>
```

**Response 200:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "role": "user",
  "created_at": "2025-01-01T00:00:00Z"
}
```

---

## 📊 儀表板 API

### GET /dashboard/stats
獲取儀表板統計數據

**Headers:**
```
Authorization: Bearer <token>
```

**Response 200:**
```json
{
  "total_balance": 1000.50,
  "available_balance": 500.25,
  "in_use_balance": 500.25,
  "today_earnings": 2.35,
  "total_earnings": 150.80,
  "usage_rate": 0.50,
  "apr": 0.08,
  "active_offers_count": 3,
  "active_loans_count": 2
}
```

---

### GET /dashboard/earnings
獲取收益趨勢數據

**Query Parameters:**
```
?period=7d  # 7d, 30d, 90d
```

**Response 200:**
```json
{
  "period": "7d",
  "data": [
    {
      "date": "2025-01-01",
      "earnings": 2.35,
      "cumulative": 150.80
    },
    {
      "date": "2025-01-02",
      "earnings": 2.40,
      "cumulative": 153.20
    }
  ]
}
```

---

## 💰 掛單 API

### GET /offers
獲取掛單列表

**Query Parameters:**
```
?status=active     # active, cancelled, executed
?page=1
?limit=20
```

**Response 200:**
```json
{
  "total": 50,
  "page": 1,
  "limit": 20,
  "data": [
    {
      "id": 1,
      "bitfinex_offer_id": 123456789,
      "amount": 100.00,
      "rate": 0.0001,
      "rate_daily_percent": 0.01,
      "duration": 2,
      "status": "active",
      "created_at": "2025-01-01T10:00:00Z",
      "updated_at": "2025-01-01T10:00:00Z"
    }
  ]
}
```

---

### POST /offers/cancel
取消掛單

**Request:**
```json
{
  "offer_id": 1
}
```

**Response 200:**
```json
{
  "message": "Offer cancelled successfully",
  "offer_id": 1
}
```

---

## 📜 放貸歷史 API

### GET /loans
獲取放貸歷史

**Query Parameters:**
```
?status=active      # active, completed
?start_date=2025-01-01
?end_date=2025-01-31
?page=1
?limit=20
```

**Response 200:**
```json
{
  "total": 100,
  "page": 1,
  "limit": 20,
  "data": [
    {
      "id": 1,
      "offer_id": 1,
      "amount": 100.00,
      "rate": 0.0001,
      "rate_daily_percent": 0.01,
      "duration": 2,
      "start_date": "2025-01-01T10:00:00Z",
      "end_date": "2025-01-03T10:00:00Z",
      "earnings": 0.20,
      "status": "completed"
    }
  ]
}
```

---

### GET /loans/summary
獲取放貸摘要統計

**Query Parameters:**
```
?period=30d  # 7d, 30d, 90d, all
```

**Response 200:**
```json
{
  "period": "30d",
  "total_loans": 45,
  "total_amount": 4500.00,
  "total_earnings": 45.50,
  "average_rate": 0.00012,
  "average_duration": 2.5
}
```

---

## 🎯 策略 API

### GET /strategy
獲取當前策略

**Response 200:**
```json
{
  "id": 1,
  "user_id": 1,
  "strategy_type": "market_follow",
  "is_active": true,
  "params": {
    "min_rate": 0.0001,
    "max_amount_per_offer": 500,
    "duration_preference": 2,
    "market_follow_percentage": 0.95
  },
  "updated_at": "2025-01-01T10:00:00Z"
}
```

---

### PUT /strategy
更新策略

**Request:**
```json
{
  "strategy_type": "ladder",
  "params": {
    "min_rate": 0.00008,
    "layers": [
      {
        "percentage": 0.3,
        "rate_offset": -0.00005
      },
      {
        "percentage": 0.4,
        "rate_offset": 0
      },
      {
        "percentage": 0.3,
        "rate_offset": 0.00005
      }
    ],
    "duration_preference": 7
  }
}
```

**Response 200:**
```json
{
  "message": "Strategy updated successfully",
  "strategy": {
    "id": 1,
    "strategy_type": "ladder",
    "params": { ... }
  }
}
```

---

## 🤖 機器人控制 API

### POST /bot/start
啟動機器人

**Response 200:**
```json
{
  "message": "Bot started successfully",
  "status": "running"
}
```

---

### POST /bot/stop
停止機器人

**Response 200:**
```json
{
  "message": "Bot stopped successfully",
  "status": "stopped"
}
```

---

### GET /bot/status
獲取機器人狀態

**Response 200:**
```json
{
  "status": "running",
  "last_execution": "2025-01-01T10:00:00Z",
  "next_execution": "2025-01-01T10:05:00Z",
  "errors_count": 0
}
```

---

## 👥 管理員 API

### GET /admin/users
獲取所有用戶（僅管理員）

**Query Parameters:**
```
?role=user  # admin, user, all
?page=1
?limit=20
```

**Response 200:**
```json
{
  "total": 5,
  "data": [
    {
      "id": 1,
      "email": "user@example.com",
      "role": "user",
      "is_active": true,
      "created_at": "2025-01-01T00:00:00Z",
      "last_login": "2025-01-05T10:00:00Z"
    }
  ]
}
```

---

### GET /admin/system/stats
獲取系統統計（僅管理員）

**Response 200:**
```json
{
  "total_users": 5,
  "active_bots": 4,
  "total_balance": 5000.00,
  "total_earnings_today": 10.50,
  "total_offers": 15,
  "total_loans": 30,
  "system_uptime": "15d 3h 25m"
}
```

---

### PUT /admin/users/:id
更新用戶資訊（僅管理員）

**Request:**
```json
{
  "is_active": true,
  "role": "user"
}
```

**Response 200:**
```json
{
  "message": "User updated successfully",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "role": "user",
    "is_active": true
  }
}
```

---

## ⚙️ 設定 API

### GET /settings
獲取用戶設定

**Response 200:**
```json
{
  "telegram_chat_id": "123456789",
  "notifications": {
    "trade_executed": true,
    "daily_report": true,
    "error_alerts": true
  }
}
```

---

### PUT /settings
更新用戶設定

**Request:**
```json
{
  "telegram_chat_id": "123456789",
  "notifications": {
    "trade_executed": true,
    "daily_report": false,
    "error_alerts": true
  }
}
```

**Response 200:**
```json
{
  "message": "Settings updated successfully"
}
```

---

## 📊 市場數據 API

### GET /market/rates
獲取當前市場利率

**Response 200:**
```json
{
  "currency": "USD",
  "data": {
    "average_rate": 0.00012,
    "min_rate": 0.00008,
    "max_rate": 0.00020,
    "volume": 1000000.00,
    "timestamp": "2025-01-01T10:00:00Z"
  }
}
```

---

## 🚨 錯誤處理

### 統一錯誤格式

```json
{
  "detail": "Error message",
  "code": "ERROR_CODE",
  "timestamp": "2025-01-01T10:00:00Z"
}
```

### 常見錯誤碼

| HTTP Status | Code | Description |
|-------------|------|-------------|
| 400 | INVALID_INPUT | 輸入參數錯誤 |
| 401 | UNAUTHORIZED | 未授權 |
| 403 | FORBIDDEN | 權限不足 |
| 404 | NOT_FOUND | 資源不存在 |
| 409 | CONFLICT | 資源衝突 |
| 429 | TOO_MANY_REQUESTS | 請求過於頻繁 |
| 500 | INTERNAL_ERROR | 伺服器錯誤 |
| 503 | SERVICE_UNAVAILABLE | 服務暫時不可用 |

---

## 🔒 安全性

### Rate Limiting
```
- 登入：5 次/分鐘
- API 查詢：100 次/分鐘
- 交易操作：10 次/分鐘
```

### CORS 設定
```python
allow_origins = ["https://yourdomain.com"]
allow_credentials = True
allow_methods = ["GET", "POST", "PUT", "DELETE"]
allow_headers = ["*"]
```

---

## 📝 API 版本控制

```
/api/v1/...  # 當前版本
/api/v2/...  # 未來版本
```

---

下一步：閱讀 [資料庫設計](../06-database/schema.md) 了解數據結構。

