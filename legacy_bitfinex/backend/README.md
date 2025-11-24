# Bitfinex Lending Bot - Backend API

## 🚀 快速開始

### 1. 安裝依賴

```bash
pip install -r requirements.txt
```

### 2. 設置環境變數

複製 `.env.example` 並創建 `.env` 文件：

```bash
cp .env.example .env
```

編輯 `.env` 文件，填入你的配置。

**重要：生成加密 Key**

```python
from cryptography.fernet import Fernet
key = Fernet.generate_key()
print(key.decode())  # 複製這個值到 ENCRYPTION_KEY
```

### 3. 初始化資料庫

```bash
# 創建資料庫遷移（首次）
alembic init alembic

# 創建遷移文件
alembic revision --autogenerate -m "Initial migration"

# 執行遷移
alembic upgrade head
```

### 4. 運行服務

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API 文檔將在 `http://localhost:8000/docs` 可用。

## 📡 API 端點

### 認證

- `POST /api/v1/auth/login` - 用戶登入

### Dashboard

- `GET /api/v1/dashboard/balance` - 獲取帳戶餘額
- `GET /api/v1/dashboard/earnings` - 獲取收益資訊
- `GET /api/v1/dashboard/loans` - 獲取借款狀況
- `GET /api/v1/dashboard/account-info` - 獲取完整帳戶資訊
- `GET /api/v1/dashboard/user-info` - 獲取 Bitfinex 用戶資訊

## 🔐 認證

所有 Dashboard API 都需要 Bearer Token 認證：

```
Authorization: Bearer <your_jwt_token>
```

## 📝 注意事項

1. 確保 PostgreSQL 資料庫已安裝並運行
2. 確保 Bitfinex API Key 和 Secret 已正確設置
3. ENCRYPTION_KEY 必須是 32 bytes base64 編碼的字串
