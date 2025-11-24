# Trading Robots Backend

Bitfinex 放貸機器人後端 API。

## 🏗️ 架構

本專案採用 FastAPI 分層架構：

- **API Layer** (`app/api/`) - 處理 HTTP 請求/響應
- **Schema Layer** (`app/schemas/`) - 資料驗證和類型定義
- **Service Layer** (`app/services/`) - 業務邏輯
- **Model Layer** (`app/models/`) - 資料庫模型（SQLAlchemy ORM）

## 📋 功能

- ✅ 用戶認證（註冊、登入、Token 刷新）
- ✅ 統一 API 響應格式 (`ApiResponse<T>`)
- ✅ 類型一致性（與前端 TypeScript 類型對應）
- ✅ 資料庫遷移（Alembic）
- ✅ 測試框架（pytest）

## 🚀 快速開始

### 1. 環境設置

```bash
# 創建虛擬環境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安裝依賴
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### 2. 配置環境變數

```bash
# 複製範本
cp .env.example .env

# 編輯 .env（填入資料庫 URL、SECRET_KEY 等）
```

詳細說明請參考 [docs/SETUP.md](./docs/SETUP.md)

### 3. 初始化資料庫

```bash
# 使用 Alembic 遷移
alembic upgrade head

# 或使用腳本（開發用）
python scripts/init_db.py
```

### 4. 啟動服務器

```bash
uvicorn app.main:app --reload
```

訪問 http://localhost:8000/docs 查看 API 文檔。

## 📚 文檔

- [環境設置指南](./docs/SETUP.md) - 完整的環境設置步驟
- [架構說明](./docs/ARCHITECTURE.md) - 系統架構和設計原則
- [API 設計規範](./docs/API_DESIGN.md) - API 設計最佳實踐
- [資料庫設計](./docs/DATABASE.md) - 資料庫結構和使用指南
- [類型對照表](./docs/TYPE_MAPPING.md) - TypeScript ↔ Python 類型對照
- [開發指南](./docs/DEVELOPMENT.md) - 新手開發指南
- [Code Review 檢查清單](./docs/CODE_REVIEW.md) - Code Review 規範

## 🧪 測試

```bash
# 運行所有測試
pytest

# 運行特定測試
pytest tests/test_auth.py

# 查看覆蓋率
pytest --cov=app
```

## 📁 專案結構

```
backend/
├── app/
│   ├── api/              # API 路由層
│   │   ├── auth.py      # Auth API
│   │   ├── deps.py      # 共用依賴
│   │   └── health.py    # 健康檢查
│   ├── core/            # 核心基礎設施
│   │   ├── config.py     # 配置
│   │   ├── database.py  # 資料庫連接
│   │   └── security.py  # 安全相關
│   ├── models/          # ORM 模型
│   │   ├── base.py      # Base Model
│   │   ├── user.py      # User Model
│   │   └── ...
│   ├── schemas/         # Pydantic Schemas
│   │   ├── common.py    # 統一響應格式
│   │   ├── auth.py      # Auth Schemas
│   │   └── ...
│   └── services/        # 業務邏輯層
│       ├── auth.py      # Auth Service
│       └── ...
├── tests/               # 測試
├── alembic/             # 資料庫遷移
├── docs/                # 文檔
└── scripts/             # 輔助腳本
```

## 🔑 關鍵特性

### 統一響應格式

所有 API 都使用 `ApiResponse<T>` 包裝：

```python
from app.schemas.common import success_response, error_response

# 成功響應
return success_response(data=user_data, message="Success")

# 錯誤響應
return error_response(code="ERROR_CODE", message="Error message")
```

### 類型一致性

- Schema 使用 camelCase（透過 alias）對應前端 TypeScript 類型
- 所有 Schema 都有 `🔗 對應 TypeScript` 註解
- 詳細對照請參考 [TYPE_MAPPING.md](./docs/TYPE_MAPPING.md)

### 認證機制

- JWT Token 認證
- Access Token + Refresh Token
- 使用 `get_current_user` 依賴注入獲取當前用戶

## 🛠️ 開發工具

- **FastAPI** - Web 框架
- **SQLAlchemy** - ORM
- **Alembic** - 資料庫遷移
- **Pydantic** - 資料驗證
- **pytest** - 測試框架

## 📝 開發規範

- 遵循 [API 設計規範](./docs/API_DESIGN.md)
- 遵循 [Code Review 檢查清單](./docs/CODE_REVIEW.md)
- 參考 [開發指南](./docs/DEVELOPMENT.md) 添加新功能

## 🤝 貢獻

1. 創建功能分支：`git checkout -b feature/your-feature`
2. 提交變更：`git commit -m "feat: add your feature"`
3. 推送分支：`git push origin feature/your-feature`
4. 創建 Pull Request

## 📄 授權

[授權資訊]
