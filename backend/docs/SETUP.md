# 環境設置指南

本文檔說明如何設置 Backend 開發環境。

## 前置需求

- Python 3.9+
- PostgreSQL 12+
- Git

## 步驟 1: Python 虛擬環境設置

### 使用 venv（推薦）

```bash
# 創建虛擬環境
python -m venv venv

# 啟動虛擬環境
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### 使用 pyenv（可選）

```bash
# 安裝 Python 3.11
pyenv install 3.11.0
pyenv local 3.11.0
```

## 步驟 2: PostgreSQL 安裝和資料庫創建

### Windows

1. 下載並安裝 [PostgreSQL](https://www.postgresql.org/download/windows/)
2. 記住設定的密碼

### Linux (Ubuntu/Debian)

```bash
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib
```

### Mac

```bash
brew install postgresql
brew services start postgresql
```

### 創建資料庫

```bash
# 登入 PostgreSQL
psql -U postgres

# 創建資料庫
CREATE DATABASE trading_robots;

# 退出
\q
```

## 步驟 3: 安裝依賴

```bash
# 安裝生產依賴
pip install -r requirements.txt

# 安裝開發依賴
pip install -r requirements-dev.txt
```

## 步驟 4: 環境變數配置

### 複製環境變數範本

```bash
cp .env.example .env
```

### 編輯 .env 檔案

```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/trading_robots

# Security
SECRET_KEY=your-secret-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Encryption (for API keys)
ENCRYPTION_KEY=your-fernet-key-here

# Bitfinex (測試用)
BITFINEX_API_URL=https://api.bitfinex.com/v2

# CORS
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000

# App
DEBUG=True
```

### 生成 Fernet Key

```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

將生成的 key 填入 `ENCRYPTION_KEY`。

### 生成 SECRET_KEY

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

將生成的 key 填入 `SECRET_KEY`。

## 步驟 5: 資料庫遷移

### 初始化 Alembic（如果尚未初始化）

```bash
alembic init alembic
```

### 創建初始遷移

```bash
alembic revision --autogenerate -m "Initial migration"
```

### 執行遷移

```bash
alembic upgrade head
```

### 或使用腳本初始化（開發用）

```bash
python scripts/init_db.py
```

## 步驟 6: 創建管理員用戶（可選）

```bash
python scripts/create_admin.py admin@example.com admin123
```

## 步驟 7: 啟動開發服務器

```bash
# 方式 1: 使用 uvicorn
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 方式 2: 使用 Python
python -m app.main

# 方式 3: 使用 FastAPI CLI
fastapi dev app/main.py
```

服務器啟動後，訪問：
- API 文檔：http://localhost:8000/docs
- 健康檢查：http://localhost:8000/api/health

## 驗證設置

### 測試健康檢查端點

```bash
curl http://localhost:8000/api/health
```

預期響應：
```json
{
  "success": true,
  "data": {"status": "healthy"},
  "message": "Service is running"
}
```

### 運行測試

```bash
pytest
```

## 常見問題

### 問題 1: PostgreSQL 連接失敗

**解決方案：**
1. 確認 PostgreSQL 服務正在運行
2. 檢查 `DATABASE_URL` 是否正確
3. 確認用戶權限

### 問題 2: 模組導入錯誤

**解決方案：**
1. 確認虛擬環境已啟動
2. 確認在正確的目錄下運行
3. 檢查 `PYTHONPATH` 環境變數

### 問題 3: Alembic 遷移失敗

**解決方案：**
1. 確認資料庫已創建
2. 檢查 `DATABASE_URL` 配置
3. 查看 `alembic/env.py` 中的導入路徑

## 下一步

- 閱讀 [ARCHITECTURE.md](./ARCHITECTURE.md) 了解架構
- 閱讀 [DEVELOPMENT.md](./DEVELOPMENT.md) 開始開發
- 閱讀 [TYPE_MAPPING.md](./TYPE_MAPPING.md) 了解類型對照

