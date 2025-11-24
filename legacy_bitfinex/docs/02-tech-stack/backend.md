# 後端技術棧

## 📦 核心技術

### FastAPI
```json
{
  "version": "^0.108.0",
  "用途": "Web 框架",
  "特性": ["異步", "自動文檔", "類型驗證"]
}
```

**選擇理由**：
- ✅ 高性能（與 Node.js 相當）
- ✅ 自動生成 OpenAPI 文檔
- ✅ Pydantic 整合（類型安全）
- ✅ 異步支援（async/await）
- ✅ 易於測試

**基礎範例**：
```python
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Bitfinex Lending Bot API",
    version="1.0.0",
    docs_url="/api/docs"
)

# CORS 設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
async def root():
    return {"message": "Hello World"}
```

---

### Python 3.10+
```json
{
  "version": ">=3.10",
  "用途": "程式語言",
  "新特性": ["類型提示增強", "Pattern Matching"]
}
```

**使用的新特性**：
```python
# 類型聯合
def get_user(user_id: int) -> User | None:
    pass

# Match-Case
match status:
    case "active":
        return process_active()
    case "inactive":
        return process_inactive()
```

---

## 🗄️ 資料庫

### SQLAlchemy
```json
{
  "version": "^2.0.0",
  "用途": "ORM",
  "模式": "異步"
}
```

**Model 範例**：
```python
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, default="user")
    api_key_encrypted = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 關聯
    strategies = relationship("Strategy", back_populates="user")
    offers = relationship("Offer", back_populates="user")
```

---

### Alembic
```json
{
  "version": "^1.13.0",
  "用途": "資料庫遷移"
}
```

**遷移範例**：
```python
# alembic/versions/xxx_create_users_table.py
def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('password_hash', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    op.drop_table('users')
```

---

### PostgreSQL
```json
{
  "version": ">=14.0",
  "用途": "關聯式資料庫"
}
```

**連線範例**：
```python
DATABASE_URL = "postgresql+asyncpg://user:pass@localhost/dbname"

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession)
```

---

## 🔐 安全性

### python-jose
```json
{
  "version": "^3.3.0",
  "用途": "JWT 處理"
}
```

**JWT 生成與驗證**：
```python
from jose import JWTError, jwt
from datetime import datetime, timedelta

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=24)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
```

---

### passlib
```json
{
  "version": "^1.7.4",
  "用途": "密碼加密"
}
```

**密碼處理**：
```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)
```

---

### cryptography
```json
{
  "version": "^41.0.0",
  "用途": "API Key 加密"
}
```

**對稱加密**：
```python
from cryptography.fernet import Fernet

# 生成 Key（只需一次，存在環境變數）
key = Fernet.generate_key()

cipher = Fernet(key)

# 加密
encrypted = cipher.encrypt(api_key.encode())

# 解密
decrypted = cipher.decrypt(encrypted).decode()
```

---

## 📅 任務排程

### APScheduler
```json
{
  "version": "^3.10.0",
  "用途": "定時任務"
}
```

**範例**：
```python
from apscheduler.schedulers.asyncio import AsyncIOScheduler

scheduler = AsyncIOScheduler()

# 每 5 分鐘執行
scheduler.add_job(
    run_trading_bot,
    'interval',
    minutes=5,
    id='trading_bot'
)

scheduler.start()
```

---

## 🔌 外部 API

### bitfinex-api-py
```json
{
  "version": "^3.0.0",
  "用途": "Bitfinex API 客戶端"
}
```

**使用範例**：
```python
from bitfinex import Client

client = Client(
    api_key="YOUR_KEY",
    api_secret="YOUR_SECRET"
)

# 獲取市場利率
funding_book = client.funding_book("fUSD")

# 提交放貸訂單
offer = client.submit_funding_offer(
    currency="USD",
    amount=100,
    rate=0.0001,  # 0.01% daily
    period=2  # days
)
```

---

### python-telegram-bot
```json
{
  "version": "^20.7.0",
  "用途": "Telegram Bot"
}
```

**通知範例**：
```python
from telegram import Bot

bot = Bot(token="YOUR_BOT_TOKEN")

async def send_notification(chat_id: int, message: str):
    await bot.send_message(
        chat_id=chat_id,
        text=message,
        parse_mode='Markdown'
    )
```

---

## 🛠️ 輔助工具

### Pydantic
```json
{
  "version": "^2.5.0",
  "用途": "數據驗證"
}
```

**Schema 定義**：
```python
from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)

class StrategyUpdate(BaseModel):
    strategy_type: str
    min_rate: float = Field(ge=0, le=1)
    duration: int = Field(ge=2, le=30)
```

---

### Loguru
```json
{
  "version": "^0.7.0",
  "用途": "日誌系統"
}
```

**配置**：
```python
from loguru import logger

logger.add(
    "logs/app_{time}.log",
    rotation="1 day",
    retention="30 days",
    level="INFO"
)

logger.info("Bot started")
logger.error("API call failed", error=str(e))
```

---

### python-dotenv
```json
{
  "version": "^1.0.0",
  "用途": "環境變數管理"
}
```

**使用**：
```python
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY")
```

---

## 📦 完整 requirements.txt

```txt
# Web Framework
fastapi==0.108.0
uvicorn[standard]==0.25.0
python-multipart==0.0.6

# Database
sqlalchemy==2.0.23
alembic==1.13.0
asyncpg==0.29.0
psycopg2-binary==2.9.9

# Security
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
cryptography==41.0.7

# Task Scheduling
apscheduler==3.10.4

# External APIs
bitfinex-api-py==3.0.0
python-telegram-bot==20.7

# Utilities
pydantic==2.5.0
pydantic-settings==2.1.0
python-dotenv==1.0.0
loguru==0.7.2

# Development
pytest==7.4.3
pytest-asyncio==0.21.1
httpx==0.25.2
```

---

## 🏗️ 專案結構

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI 應用入口
│   │
│   ├── api/                 # API 路由
│   │   ├── __init__.py
│   │   ├── deps.py          # 依賴注入
│   │   ├── auth.py
│   │   ├── dashboard.py
│   │   ├── offers.py
│   │   ├── loans.py
│   │   └── admin.py
│   │
│   ├── bot/                 # 交易機器人
│   │   ├── __init__.py
│   │   ├── executor.py      # 執行器
│   │   ├── market.py        # 市場數據
│   │   └── strategies/
│   │       ├── base.py
│   │       ├── market_follow.py
│   │       └── ladder.py
│   │
│   ├── core/                # 核心配置
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── security.py
│   │   └── database.py
│   │
│   ├── models/              # SQLAlchemy Models
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── strategy.py
│   │   ├── offer.py
│   │   └── loan.py
│   │
│   ├── schemas/             # Pydantic Schemas
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── strategy.py
│   │   └── dashboard.py
│   │
│   ├── services/            # 業務邏輯
│   │   ├── __init__.py
│   │   ├── user_service.py
│   │   ├── bot_service.py
│   │   └── notification_service.py
│   │
│   └── utils/               # 工具函數
│       ├── __init__.py
│       └── helpers.py
│
├── alembic/                 # 資料庫遷移
│   ├── versions/
│   └── env.py
│
├── tests/                   # 測試
│   ├── test_api.py
│   └── test_bot.py
│
├── .env.example             # 環境變數範本
├── requirements.txt
├── alembic.ini
└── README.md
```

---

## ⚙️ 配置管理

```python
# app/core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str
    
    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_HOURS: int = 24
    ENCRYPTION_KEY: str
    
    # Bitfinex
    BITFINEX_API_KEY: str
    BITFINEX_API_SECRET: str
    
    # Telegram
    TELEGRAM_BOT_TOKEN: str
    
    # Bot
    BOT_INTERVAL_MINUTES: int = 5
    
    class Config:
        env_file = ".env"

settings = Settings()
```

---

## 🚀 啟動命令

```bash
# 開發環境
uvicorn app.main:app --reload --port 8000

# 生產環境
gunicorn app.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000
```

---

下一步：閱讀 [基礎設施](./infrastructure.md) 了解部署相關技術。

