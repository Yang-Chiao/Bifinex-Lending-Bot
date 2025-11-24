# 資料庫設計

本文檔說明資料庫設計和使用指南。

## 表結構

### users 表

| 欄位 | 類型 | 說明 |
|-----|------|------|
| id | VARCHAR | UUID (主鍵) |
| email | VARCHAR | Email (唯一索引) |
| password_hash | VARCHAR | 密碼雜湊 |
| role | ENUM | 角色 (admin/user) |
| is_active | BOOLEAN | 是否啟用 |
| bitfinex_api_key | VARCHAR | Bitfinex API Key (加密) |
| bitfinex_api_secret | VARCHAR | Bitfinex API Secret (加密) |
| created_at | TIMESTAMP | 創建時間 |
| updated_at | TIMESTAMP | 更新時間 |

### strategies 表

| 欄位 | 類型 | 說明 |
|-----|------|------|
| id | VARCHAR | UUID (主鍵) |
| user_id | VARCHAR | 用戶 ID (外鍵) |
| strategy_type | ENUM | 策略類型 |
| params | TEXT | 策略參數 (JSON) |
| is_active | BOOLEAN | 是否啟用 |
| created_at | TIMESTAMP | 創建時間 |
| updated_at | TIMESTAMP | 更新時間 |

### offers 表

| 欄位 | 類型 | 說明 |
|-----|------|------|
| id | VARCHAR | UUID (主鍵) |
| user_id | VARCHAR | 用戶 ID (外鍵) |
| strategy_id | VARCHAR | 策略 ID (外鍵，可選) |
| currency | VARCHAR | 貨幣 |
| amount | NUMERIC(20,8) | 金額 |
| rate | NUMERIC(10,6) | 利率 |
| period | NUMERIC(10,2) | 期限（天數） |
| is_active | BOOLEAN | 是否啟用 |
| expires_at | TIMESTAMP | 過期時間 |
| created_at | TIMESTAMP | 創建時間 |
| updated_at | TIMESTAMP | 更新時間 |

### loans 表

| 欄位 | 類型 | 說明 |
|-----|------|------|
| id | VARCHAR | UUID (主鍵) |
| user_id | VARCHAR | 用戶 ID (外鍵) |
| offer_id | VARCHAR | 報價 ID (外鍵，可選) |
| currency | VARCHAR | 貨幣 |
| amount | NUMERIC(20,8) | 金額 |
| rate | NUMERIC(10,6) | 利率 |
| period | NUMERIC(10,2) | 期限（天數） |
| status | ENUM | 狀態 (active/closed/cancelled) |
| started_at | TIMESTAMP | 開始時間 |
| closed_at | TIMESTAMP | 結束時間 |
| created_at | TIMESTAMP | 創建時間 |
| updated_at | TIMESTAMP | 更新時間 |

## SQLAlchemy ORM 使用指南

### 定義模型

```python
from app.models.base import BaseModel
from sqlalchemy import Column, String, Boolean

class User(BaseModel):
    __tablename__ = "users"
    
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
```

### 關聯（Relationship）

```python
from sqlalchemy.orm import relationship

class User(BaseModel):
    # ...
    strategies = relationship("Strategy", back_populates="user")

class Strategy(BaseModel):
    # ...
    user_id = Column(String, ForeignKey("users.id"))
    user = relationship("User", back_populates="strategies")
```

## 資料庫遷移流程（Alembic）

### 創建遷移

```bash
# 自動生成遷移腳本
alembic revision --autogenerate -m "Add new column"

# 手動創建遷移腳本
alembic revision -m "Add new column"
```

### 執行遷移

```bash
# 升級到最新版本
alembic upgrade head

# 升級到特定版本
alembic upgrade <revision_id>

# 降級一個版本
alembic downgrade -1

# 降級到特定版本
alembic downgrade <revision_id>
```

### 查看遷移歷史

```bash
# 查看當前版本
alembic current

# 查看遷移歷史
alembic history
```

## 常見查詢範例（CRUD）

### Create（創建）

```python
from app.models.user import User

# 創建用戶
user = User(
    email="user@example.com",
    password_hash=hashed_password
)
db.add(user)
db.commit()
db.refresh(user)
```

### Read（讀取）

```python
# 獲取單個用戶
user = db.query(User).filter(User.email == email).first()

# 獲取所有用戶
users = db.query(User).all()

# 獲取用戶的策略
strategies = db.query(Strategy).filter(Strategy.user_id == user.id).all()
```

### Update（更新）

```python
# 更新用戶
user = db.query(User).filter(User.id == user_id).first()
user.is_active = False
db.commit()
```

### Delete（刪除）

```python
# 刪除用戶（會級聯刪除相關的策略、報價等）
user = db.query(User).filter(User.id == user_id).first()
db.delete(user)
db.commit()
```

## 欄位命名規範

### 資料庫層（snake_case）

- 表名：複數形式，snake_case（如 `users`, `strategies`）
- 欄位名：snake_case（如 `created_at`, `is_active`）

### API 層（camelCase）

- 響應欄位：camelCase（如 `createdAt`, `isActive`）
- 使用 Pydantic alias 自動轉換

**範例：**
```python
class UserResponse(BaseModel):
    createdAt: datetime = Field(..., alias="created_at")
    isActive: bool = Field(..., alias="is_active")
    
    class Config:
        from_attributes = True
        populate_by_name = True
```

## 索引設計

### 單列索引

```python
email = Column(String, unique=True, index=True, nullable=False)
```

### 複合索引

```python
from sqlalchemy import Index

Index('idx_user_strategy', 'user_id', 'strategy_type')
```

## 事務處理

```python
try:
    # 開始事務
    user = User(...)
    db.add(user)
    
    strategy = Strategy(...)
    db.add(strategy)
    
    # 提交事務
    db.commit()
except Exception as e:
    # 回滾事務
    db.rollback()
    raise
```

## 查詢優化

### 使用 join 減少查詢次數

```python
# ❌ 多次查詢
user = db.query(User).filter(User.id == user_id).first()
strategies = db.query(Strategy).filter(Strategy.user_id == user_id).all()

# ✅ 使用 join
user = db.query(User).options(
    joinedload(User.strategies)
).filter(User.id == user_id).first()
```

### 使用 select_related（避免 N+1 問題）

```python
from sqlalchemy.orm import selectinload

users = db.query(User).options(
    selectinload(User.strategies)
).all()
```

## 參考資源

- [SQLAlchemy 文檔](https://docs.sqlalchemy.org/)
- [Alembic 文檔](https://alembic.sqlalchemy.org/)
- [類型對照](./TYPE_MAPPING.md)

