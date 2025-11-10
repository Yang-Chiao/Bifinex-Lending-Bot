# API 使用指南

## 📡 API 端點說明

### 認證端點

#### 1. 用戶登入
```http
POST /api/v1/auth/login
Content-Type: application/x-www-form-urlencoded

email=user@example.com&password=your_password
```

**響應:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

---

### Dashboard 端點

所有 Dashboard API 都需要在請求頭中包含 Bearer Token：

```
Authorization: Bearer <your_access_token>
```

#### 1. 獲取帳戶餘額
```http
GET /api/v1/dashboard/balance
Authorization: Bearer <token>
```

**響應:**
```json
{
  "total_balance": {
    "USD": 1000.5,
    "BTC": 0.001
  },
  "funding_balance": {
    "USD": 500.0
  },
  "wallets": [
    ["exchange", "USD", 500.5],
    ["funding", "USD", 500.0]
  ]
}
```

#### 2. 獲取收益資訊
```http
GET /api/v1/dashboard/earnings?currency=USD
Authorization: Bearer <token>
```

**響應:**
```json
{
  "total_earnings": 125.50,
  "today_earnings": 5.25,
  "monthly_earnings": 85.30,
  "currency": "USD",
  "earnings_by_loan": [
    {
      "trade_id": 123456,
      "amount": 1000.0,
      "rate": 0.05,
      "period": 30,
      "earnings": 4.11,
      "created_at": "2024-01-15T10:30:00"
    }
  ]
}
```

#### 3. 獲取借款狀況
```http
GET /api/v1/dashboard/loans?currency=USD
Authorization: Bearer <token>
```

**響應:**
```json
{
  "total_loans": 10,
  "active_loans": 5,
  "total_amount": 5000.0,
  "average_rate": 0.045,
  "total_earnings": 225.0,
  "loans": [
    {
      "id": 789012,
      "symbol": "fUSD",
      "side": "lend",
      "created_at": "2024-01-15T10:00:00",
      "amount": 1000.0,
      "rate": 0.05,
      "period": 30,
      "status": "ACTIVE",
      "earnings": 4.11
    }
  ]
}
```

#### 4. 獲取完整帳戶資訊
```http
GET /api/v1/dashboard/account-info?currency=USD
Authorization: Bearer <token>
```

**響應:**
包含所有上述資訊的完整物件。

#### 5. 獲取 Bitfinex 用戶資訊
```http
GET /api/v1/dashboard/user-info
Authorization: Bearer <token>
```

**響應:**
Bitfinex API 返回的原始用戶資訊。

---

## 🔐 認證流程

1. **登入獲取 Token**
   ```bash
   curl -X POST "http://localhost:8000/api/v1/auth/login" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "email=user@example.com&password=password123"
   ```

2. **使用 Token 訪問 API**
   ```bash
   curl -X GET "http://localhost:8000/api/v1/dashboard/balance" \
     -H "Authorization: Bearer <your_token>"
   ```

---

## 📝 注意事項

1. Token 有效期為 24 小時
2. 所有 Dashboard API 都需要用戶已設置 Bitfinex API Key 和 Secret
3. 如果 API Key 未設置，會返回 400 錯誤
4. 確保 Bitfinex API Key 有足夠的權限（需要讀取權限）

---

## 🧪 測試 API

### 使用 curl

```bash
# 1. 登入
TOKEN=$(curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "email=user@example.com&password=password123" \
  | jq -r '.access_token')

# 2. 獲取餘額
curl -X GET "http://localhost:8000/api/v1/dashboard/balance" \
  -H "Authorization: Bearer $TOKEN"
```

### 使用 Python requests

```python
import requests

BASE_URL = "http://localhost:8000/api/v1"

# 1. 登入
response = requests.post(
    f"{BASE_URL}/auth/login",
    data={"email": "user@example.com", "password": "password123"}
)
token = response.json()["access_token"]

# 2. 獲取餘額
headers = {"Authorization": f"Bearer {token}"}
response = requests.get(f"{BASE_URL}/dashboard/balance", headers=headers)
print(response.json())
```

---

## 📚 查看完整文檔

訪問 `http://localhost:8000/docs` 查看交互式 API 文檔（Swagger UI）。
