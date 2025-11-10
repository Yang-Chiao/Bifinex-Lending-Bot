# 🚀 快速開始指南

本指南將幫助你快速設置並開始使用 Bitfinex Lending Bot API。

## 📋 前置需求

- Python 3.9+
- PostgreSQL 12+
- Bitfinex 帳戶和 API Key（需要讀取權限）

## 🛠️ 設置步驟

### 1. 安裝依賴

```bash
cd backend
pip install -r requirements.txt
```

### 2. 設置環境變數

創建 `.env` 文件：

```bash
cp .env.example .env
```

編輯 `.env` 文件：

```env
# 資料庫配置
DATABASE_URL=postgresql://user:password@localhost/bitfinex_lending

# JWT 配置（生產環境請使用強密鑰）
SECRET_KEY=your-secret-key-change-in-production-min-32-chars

# 生成加密 Key
python scripts/generate_encryption_key.py
# 複製輸出的 key 到下面
ENCRYPTION_KEY=<生成的加密key>

# Bitfinex API（使用默認值即可）
BITFINEX_API_URL=https://api.bitfinex.com/v2
```

### 3. 初始化資料庫

```bash
# 創建 PostgreSQL 資料庫
createdb bitfinex_lending

# 初始化 Alembic（首次運行）
alembic init alembic

# 創建遷移文件
alembic revision --autogenerate -m "Initial migration"

# 執行遷移
alembic upgrade head
```

**注意：** 如果已經有 `alembic` 目錄，跳過 `alembic init` 步驟。

### 4. 創建測試用戶

在 Python shell 中運行：

```python
from app.core.database import SessionLocal
from app.models.user import User
from app.core.security import get_password_hash, encrypt_api_key

db = SessionLocal()

# 創建用戶
user = User(
    email="test@example.com",
    password_hash=get_password_hash("password123"),
    api_key_encrypted=encrypt_api_key("your_bitfinex_api_key"),
    api_secret_encrypted=encrypt_api_key("your_bitfinex_api_secret")
)

db.add(user)
db.commit()
db.close()
```

### 5. 啟動服務

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

服務將在 `http://localhost:8000` 啟動。

## 🧪 測試 API

### 方法 1: 使用 Swagger UI

訪問 `http://localhost:8000/docs` 查看交互式 API 文檔。

### 方法 2: 使用 curl

```bash
# 1. 登入獲取 Token
TOKEN=$(curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "email=test@example.com&password=password123" \
  | python -m json.tool | grep access_token | cut -d'"' -f4)

# 2. 獲取帳戶餘額
curl -X GET "http://localhost:8000/api/v1/dashboard/balance" \
  -H "Authorization: Bearer $TOKEN" \
  | python -m json.tool

# 3. 獲取借款狀況
curl -X GET "http://localhost:8000/api/v1/dashboard/loans?currency=USD" \
  -H "Authorization: Bearer $TOKEN" \
  | python -m json.tool
```

### 方法 3: 使用 Python

```python
import requests

BASE_URL = "http://localhost:8000/api/v1"

# 登入
response = requests.post(
    f"{BASE_URL}/auth/login",
    data={"email": "test@example.com", "password": "password123"}
)
token = response.json()["access_token"]

# 設置認證頭
headers = {"Authorization": f"Bearer {token}"}

# 獲取餘額
response = requests.get(f"{BASE_URL}/dashboard/balance", headers=headers)
print("帳戶餘額:", response.json())

# 獲取收益
response = requests.get(f"{BASE_URL}/dashboard/earnings?currency=USD", headers=headers)
print("收益資訊:", response.json())

# 獲取借款狀況
response = requests.get(f"{BASE_URL}/dashboard/loans?currency=USD", headers=headers)
print("借款狀況:", response.json())
```

## 📡 可用的 API 端點

### 認證
- `POST /api/v1/auth/login` - 用戶登入
- `GET /api/v1/auth/me` - 獲取當前用戶資訊

### Dashboard
- `GET /api/v1/dashboard/balance` - 獲取帳戶餘額
- `GET /api/v1/dashboard/earnings` - 獲取收益資訊
- `GET /api/v1/dashboard/loans` - 獲取借款狀況
- `GET /api/v1/dashboard/account-info` - 獲取完整帳戶資訊
- `GET /api/v1/dashboard/user-info` - 獲取 Bitfinex 用戶資訊

詳細文檔請參考 [API_GUIDE.md](./API_GUIDE.md)

## ⚠️ 常見問題

### 1. 資料庫連接錯誤

確保 PostgreSQL 服務正在運行：

```bash
# Linux/Mac
sudo systemctl status postgresql

# Windows
# 檢查服務是否運行
```

### 2. Bitfinex API 認證失敗

- 確認 API Key 和 Secret 正確
- 確認 API Key 有讀取權限
- 檢查 Bitfinex 帳戶是否正常

### 3. 加密 Key 錯誤

確保 `ENCRYPTION_KEY` 是使用 `scripts/generate_encryption_key.py` 生成的。
如果已創建用戶但更換了加密 Key，需要重新設置用戶的 API 憑證。

### 4. 模組導入錯誤

確保你在 `backend` 目錄下運行，並且已安裝所有依賴：

```bash
cd backend
pip install -r requirements.txt
```

## 📚 下一步

- 查看 [API_GUIDE.md](./API_GUIDE.md) 了解詳細的 API 使用說明
- 查看 [README.md](./README.md) 了解項目架構
- 開始開發前端應用

## 🆘 需要幫助？

如果遇到問題，請檢查：
1. 日誌輸出（終端）
2. FastAPI 文檔：`http://localhost:8000/docs`
3. 確保所有環境變數都已正確設置
