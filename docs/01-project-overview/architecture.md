# 系統架構

## 🏗️ 整體架構

```
┌─────────────────────────────────────────────────────────────┐
│                         用戶層                                │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  Web Browser │  │ Telegram Bot │  │    Mobile    │      │
│  │  (React)     │  │              │  │   (Future)   │      │
│  └──────┬───────┘  └──────┬───────┘  └──────────────┘      │
└─────────┼──────────────────┼──────────────────────────────────┘
          │                  │
          │ HTTPS/WS         │ HTTPS
          │                  │
┌─────────▼──────────────────▼──────────────────────────────────┐
│                      應用層（API Gateway）                      │
│  ┌──────────────────────────────────────────────────────┐    │
│  │             FastAPI Backend                          │    │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐          │    │
│  │  │  Auth    │  │Dashboard │  │  Admin   │          │    │
│  │  │ Service  │  │  API     │  │   API    │          │    │
│  │  └──────────┘  └──────────┘  └──────────┘          │    │
│  └──────────────────────┬─────────────────────────────┘    │
└─────────────────────────┼──────────────────────────────────┘
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
┌───────▼────────┐ ┌──────▼──────┐ ┌───────▼────────┐
│ Trading Bot    │ │ Notification │ │   Database     │
│   Service      │ │   Service    │ │  PostgreSQL    │
│                │ │              │ │                │
│ ┌────────────┐ │ │ ┌──────────┐ │ │ ┌────────────┐ │
│ │Strategy    │ │ │ │Telegram  │ │ │ │   users    │ │
│ │Engine      │ │ │ │  Bot     │ │ │ │ strategies │ │
│ └────────────┘ │ │ └──────────┘ │ │ │   offers   │ │
│ ┌────────────┐ │ │ ┌──────────┐ │ │ │   loans    │ │
│ │Market      │ │ │ │  Email   │ │ │ │   logs     │ │
│ │Monitor     │ │ │ │(Future)  │ │ │ └────────────┘ │
│ └────────────┘ │ │ └──────────┘ │ └────────────────┘
└────────┬───────┘ └───────────────┘
         │
         │ HTTPS
         │
┌────────▼────────────────────────────────────┐
│         外部服務（External APIs）            │
│  ┌──────────────┐  ┌──────────────┐        │
│  │  Bitfinex    │  │  Telegram    │        │
│  │     API      │  │     API      │        │
│  └──────────────┘  └──────────────┘        │
└─────────────────────────────────────────────┘
```

---

## 🎨 架構設計原則

### 1. 前後端分離
- **前端**：React SPA，獨立部署
- **後端**：RESTful API，無狀態設計
- **優勢**：開發並行、技術解耦、易於擴展

### 2. 服務分層
```
前端層（Presentation）
    ↓
API 層（Application）
    ↓
業務邏輯層（Business Logic）
    ↓
數據訪問層（Data Access）
    ↓
數據庫層（Database）
```

### 3. 關注點分離
- **機器人服務**：獨立進程，專注交易邏輯
- **API 服務**：處理 HTTP 請求，數據查詢
- **通知服務**：異步推送，不阻塞主流程

---

## 🔧 核心組件

### 1. 前端（Frontend）

#### 技術棧
```typescript
- React 18
- TypeScript
- Vite
- TailwindCSS
- shadcn/ui
- React Query
- Zustand
- React Router
```

#### 目錄結構
```
frontend/
├── src/
│   ├── components/       # 可重用組件
│   │   ├── ui/          # shadcn/ui 組件
│   │   ├── charts/      # 圖表組件
│   │   └── forms/       # 表單組件
│   ├── pages/           # 頁面組件
│   │   ├── Dashboard/
│   │   ├── History/
│   │   ├── Strategy/
│   │   └── Admin/
│   ├── hooks/           # 自定義 Hooks
│   ├── services/        # API 服務
│   ├── stores/          # Zustand 狀態
│   ├── types/           # TypeScript 類型
│   └── utils/           # 工具函數
├── public/
└── package.json
```

---

### 2. 後端（Backend）

#### 技術棧
```python
- FastAPI
- SQLAlchemy
- Pydantic
- APScheduler
- python-jose (JWT)
- passlib (密碼加密)
- cryptography (API Key 加密)
```

#### 目錄結構
```
backend/
├── app/
│   ├── api/             # API 路由
│   │   ├── auth.py
│   │   ├── dashboard.py
│   │   ├── offers.py
│   │   ├── loans.py
│   │   └── admin.py
│   ├── bot/             # 機器人邏輯
│   │   ├── strategies/  # 策略實現
│   │   ├── market.py    # 市場數據
│   │   └── executor.py  # 執行器
│   ├── core/            # 核心配置
│   │   ├── config.py
│   │   ├── security.py
│   │   └── database.py
│   ├── models/          # 資料庫模型
│   ├── schemas/         # Pydantic 模型
│   ├── services/        # 業務邏輯
│   └── utils/           # 工具函數
├── tests/
├── alembic/             # 資料庫遷移
├── requirements.txt
└── main.py
```

---

### 3. 交易機器人（Trading Bot）

#### 核心流程
```python
while True:
    # 1. 獲取市場數據
    market_rate = fetch_market_rate()
    
    # 2. 獲取用戶策略
    for user in active_users:
        strategy = get_user_strategy(user)
        
        # 3. 計算掛單參數
        offer_params = strategy.calculate(market_rate)
        
        # 4. 執行掛單
        if should_place_offer(offer_params):
            place_offer(user, offer_params)
        
        # 5. 管理現有訂單
        manage_existing_offers(user)
    
    # 6. 記錄日誌
    log_execution()
    
    # 7. 等待下一輪
    sleep(300)  # 5 分鐘
```

#### 策略模式
```python
class Strategy(ABC):
    @abstractmethod
    def calculate(self, market_rate: float) -> OfferParams:
        pass

class MarketFollowStrategy(Strategy):
    def calculate(self, market_rate: float) -> OfferParams:
        return OfferParams(
            rate=market_rate * 0.95,
            amount=available_balance,
            duration=2  # days
        )

class LadderStrategy(Strategy):
    def calculate(self, market_rate: float) -> list[OfferParams]:
        # 階梯式邏輯
        pass
```

---

### 4. 資料庫（Database）

#### 資料表設計
```sql
users (用戶)
├── id (PK)
├── email
├── password_hash
├── role (admin/user)
├── api_key_encrypted
├── api_secret_encrypted
└── created_at

strategies (策略)
├── id (PK)
├── user_id (FK)
├── strategy_type
├── params (JSONB)
├── is_active
└── updated_at

offers (掛單)
├── id (PK)
├── user_id (FK)
├── bitfinex_offer_id
├── amount
├── rate
├── duration
├── status
├── created_at
└── updated_at

loans (成交記錄)
├── id (PK)
├── user_id (FK)
├── offer_id (FK)
├── amount
├── rate
├── start_date
├── end_date
├── earnings
└── status

logs (系統日誌)
├── id (PK)
├── level
├── message
├── user_id (FK)
└── timestamp
```

---

## 🔄 數據流

### 1. 用戶登入流程
```
User → Frontend → POST /api/auth/login
                    ↓
                FastAPI Auth Service
                    ↓
                Verify Password
                    ↓
                Generate JWT Token
                    ↓
                Frontend (Store Token)
                    ↓
                Redirect to Dashboard
```

### 2. 儀表板數據流
```
Frontend → GET /api/dashboard/stats (with JWT)
              ↓
          FastAPI Verify JWT
              ↓
          Query Database
              ↓
          Aggregate Data
              ↓
          Return JSON
              ↓
          Frontend Render Charts
```

### 3. 機器人執行流程
```
Scheduler Trigger (Every 5 min)
    ↓
Bot Service Start
    ↓
For Each User:
    ├── Fetch Bitfinex Market Data
    ├── Get User Strategy from DB
    ├── Calculate Offer Parameters
    ├── Place/Cancel Offers via Bitfinex API
    ├── Update Database
    └── Send Notification (if needed)
    ↓
Sleep Until Next Execution
```

---

## 🔐 安全架構

### 1. 認證流程
```
1. 用戶輸入帳密 → Frontend
2. POST /api/auth/login → Backend
3. 驗證帳密 (bcrypt)
4. 生成 JWT Token (24hr 有效期)
5. Frontend 存儲 Token (localStorage)
6. 每次請求帶 Authorization Header
7. Backend 驗證 Token
```

### 2. API Key 加密
```python
from cryptography.fernet import Fernet

# 使用環境變數的 Secret Key
cipher = Fernet(SECRET_KEY)

# 加密
encrypted_key = cipher.encrypt(api_key.encode())

# 解密（使用時）
api_key = cipher.decrypt(encrypted_key).decode()
```

### 3. 權限控制
```python
@router.get("/admin/users")
async def get_users(
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(403, "Admin only")
    # ...
```

---

## 📡 通信協議

### 1. HTTP RESTful API
- **前端 ↔ 後端**：標準 REST API
- **Content-Type**：application/json
- **認證**：Bearer Token (JWT)

### 2. WebSocket（選用）
- **用途**：即時數據推送
- **協議**：ws:// 或 wss://
- **場景**：Dashboard 即時更新

### 3. Telegram Bot API
- **用途**：通知推送
- **方式**：HTTPS POST
- **格式**：Markdown

---

## 🚀 部署架構

### MVP 階段（單機）
```
┌─────────────────────────────────────┐
│      VPS / EC2 (Ubuntu 22.04)       │
│                                     │
│  ┌─────────────────────────────┐   │
│  │   Nginx (Reverse Proxy)     │   │
│  │   ├── Frontend (Static)     │   │
│  │   └── Backend API Proxy     │   │
│  └─────────────────────────────┘   │
│                                     │
│  ┌─────────────────────────────┐   │
│  │   FastAPI (uvicorn)         │   │
│  │   Port: 8000                │   │
│  └─────────────────────────────┘   │
│                                     │
│  ┌─────────────────────────────┐   │
│  │   Trading Bot (systemd)     │   │
│  │   Background Process        │   │
│  └─────────────────────────────┘   │
│                                     │
│  ┌─────────────────────────────┐   │
│  │   PostgreSQL                │   │
│  │   Port: 5432                │   │
│  └─────────────────────────────┘   │
└─────────────────────────────────────┘
```

### 生產階段（分離）
```
┌──────────────┐   ┌──────────────┐
│   CDN/       │   │   API        │
│   Vercel     │   │   Cloud Run  │
│  (Frontend)  │   │  (Backend)   │
└──────────────┘   └──────┬───────┘
                          │
        ┌─────────────────┼─────────────┐
        │                 │             │
┌───────▼─────┐  ┌────────▼──────┐  ┌──▼──────┐
│  Bot EC2    │  │  RDS/Cloud    │  │  Redis  │
│  (Systemd)  │  │  PostgreSQL   │  │ (Cache) │
└─────────────┘  └───────────────┘  └─────────┘
```

---

## 📊 監控架構（未來）

```
Application Logs → Loguru → File
                              ↓
                    Logstash (Optional)
                              ↓
                    Elasticsearch
                              ↓
                    Kibana Dashboard

Metrics → Prometheus → Grafana

Health Check → Uptime Robot → Telegram Alert
```

---

## 🔧 技術決策

### 為什麼選 FastAPI？
- ✅ 高性能（異步支援）
- ✅ 自動生成 API 文檔
- ✅ 類型檢查（Pydantic）
- ✅ 現代化、社群活躍

### 為什麼選 React？
- ✅ 生態系豐富
- ✅ TypeScript 支援好
- ✅ shadcn/ui 組件精美
- ✅ 開發效率高

### 為什麼選 PostgreSQL？
- ✅ 可靠性高
- ✅ JSONB 支援（策略參數）
- ✅ 併發處理好
- ✅ 易於擴展

---

下一步：閱讀 [技術棧](../02-tech-stack/) 了解詳細的技術選型。

