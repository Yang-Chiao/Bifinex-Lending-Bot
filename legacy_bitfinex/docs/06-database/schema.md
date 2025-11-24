# 資料庫結構設計

## 🗄️ 資料表總覽

```
users (用戶表)
strategies (策略表)
offers (掛單記錄表)
loans (放貸記錄表)
daily_stats (每日統計表)
logs (系統日誌表)
notifications (通知記錄表)
```

---

## 📋 資料表詳細設計

### 1. users (用戶表)

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) DEFAULT 'user',  -- 'admin' or 'user'
    
    -- Bitfinex API 憑證（加密）
    api_key_encrypted TEXT,
    api_secret_encrypted TEXT,
    
    -- 設定
    telegram_chat_id VARCHAR(50),
    
    -- 狀態
    is_active BOOLEAN DEFAULT true,
    
    -- 時間戳
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);
```

**欄位說明**：
- `api_key_encrypted`, `api_secret_encrypted`：使用 Fernet 加密
- `telegram_chat_id`：用於通知推送
- `is_active`：軟刪除標記

---

### 2. strategies (策略表)

```sql
CREATE TABLE strategies (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    
    -- 策略類型
    strategy_type VARCHAR(50) NOT NULL,  -- 'market_follow', 'ladder', 'composite'
    
    -- 策略參數（JSON）
    params JSONB NOT NULL,
    
    -- 狀態
    is_active BOOLEAN DEFAULT true,
    
    -- 時間戳
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT unique_user_strategy UNIQUE(user_id)
);

CREATE INDEX idx_strategies_user ON strategies(user_id);
CREATE INDEX idx_strategies_type ON strategies(strategy_type);
```

**params JSONB 範例**：

```json
{
  "min_rate": 0.0001,
  "max_amount_per_offer": 500,
  "duration_preference": 2,
  "market_follow_percentage": 0.95
}
```

---

### 3. offers (掛單記錄表)

```sql
CREATE TABLE offers (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    
    -- Bitfinex 訂單 ID
    bitfinex_offer_id BIGINT UNIQUE,
    
    -- 訂單參數
    currency VARCHAR(10) DEFAULT 'USD',
    amount DECIMAL(15, 2) NOT NULL,
    rate DECIMAL(15, 8) NOT NULL,       -- 每日利率（小數）
    duration INTEGER NOT NULL,           -- 天數
    
    -- 狀態
    status VARCHAR(20) NOT NULL,         -- 'pending', 'active', 'executed', 'cancelled'
    
    -- 時間戳
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    executed_at TIMESTAMP,
    cancelled_at TIMESTAMP
);

CREATE INDEX idx_offers_user ON offers(user_id);
CREATE INDEX idx_offers_status ON offers(status);
CREATE INDEX idx_offers_created ON offers(created_at);
CREATE INDEX idx_offers_bitfinex ON offers(bitfinex_offer_id);
```

**狀態流轉**：
```
pending → active → executed
         ↓
      cancelled
```

---

### 4. loans (放貸記錄表)

```sql
CREATE TABLE loans (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    offer_id INTEGER REFERENCES offers(id) ON DELETE SET NULL,
    
    -- Bitfinex 放貸 ID
    bitfinex_loan_id BIGINT UNIQUE,
    
    -- 放貸參數
    currency VARCHAR(10) DEFAULT 'USD',
    amount DECIMAL(15, 2) NOT NULL,
    rate DECIMAL(15, 8) NOT NULL,
    duration INTEGER NOT NULL,
    
    -- 收益
    earnings DECIMAL(15, 4) DEFAULT 0,
    
    -- 日期
    start_date TIMESTAMP NOT NULL,
    end_date TIMESTAMP NOT NULL,
    
    -- 狀態
    status VARCHAR(20) NOT NULL,  -- 'active', 'completed', 'early_return'
    
    -- 時間戳
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP
);

CREATE INDEX idx_loans_user ON loans(user_id);
CREATE INDEX idx_loans_status ON loans(status);
CREATE INDEX idx_loans_dates ON loans(start_date, end_date);
CREATE INDEX idx_loans_bitfinex ON loans(bitfinex_loan_id);
```

---

### 5. daily_stats (每日統計表)

```sql
CREATE TABLE daily_stats (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    
    -- 日期
    date DATE NOT NULL,
    
    -- 資金數據
    total_balance DECIMAL(15, 2) DEFAULT 0,
    available_balance DECIMAL(15, 2) DEFAULT 0,
    in_use_balance DECIMAL(15, 2) DEFAULT 0,
    
    -- 收益數據
    daily_earnings DECIMAL(15, 4) DEFAULT 0,
    cumulative_earnings DECIMAL(15, 4) DEFAULT 0,
    
    -- 利率數據
    average_rate DECIMAL(15, 8),
    
    -- 統計數據
    offers_count INTEGER DEFAULT 0,
    loans_count INTEGER DEFAULT 0,
    
    -- 時間戳
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT unique_user_date UNIQUE(user_id, date)
);

CREATE INDEX idx_daily_stats_user_date ON daily_stats(user_id, date DESC);
```

---

### 6. logs (系統日誌表)

```sql
CREATE TABLE logs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    
    -- 日誌級別
    level VARCHAR(20) NOT NULL,  -- 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'
    
    -- 日誌內容
    message TEXT NOT NULL,
    
    -- 額外數據
    extra_data JSONB,
    
    -- 來源
    source VARCHAR(100),  -- 'api', 'bot', 'system'
    
    -- 時間戳
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_logs_user ON logs(user_id);
CREATE INDEX idx_logs_level ON logs(level);
CREATE INDEX idx_logs_timestamp ON logs(timestamp DESC);
CREATE INDEX idx_logs_source ON logs(source);
```

---

### 7. notifications (通知記錄表)

```sql
CREATE TABLE notifications (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    
    -- 通知類型
    type VARCHAR(50) NOT NULL,  -- 'trade_executed', 'error', 'daily_report'
    
    -- 通知內容
    title VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    
    -- 狀態
    is_sent BOOLEAN DEFAULT false,
    sent_at TIMESTAMP,
    
    -- 時間戳
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_notifications_user ON notifications(user_id);
CREATE INDEX idx_notifications_type ON notifications(type);
CREATE INDEX idx_notifications_sent ON notifications(is_sent);
```

---

## 🔗 關聯關係圖

```
users
  │
  ├─1:1── strategies
  │
  ├─1:N── offers
  │         │
  │         └─1:1── loans
  │
  ├─1:N── daily_stats
  │
  ├─1:N── logs
  │
  └─1:N── notifications
```

---

## 📊 視圖（Views）

### view_user_dashboard

```sql
CREATE VIEW view_user_dashboard AS
SELECT 
    u.id AS user_id,
    u.email,
    
    -- 資金統計
    COALESCE(SUM(CASE WHEN l.status = 'active' THEN l.amount ELSE 0 END), 0) AS in_use_balance,
    COALESCE(SUM(CASE WHEN o.status = 'active' THEN o.amount ELSE 0 END), 0) AS pending_balance,
    
    -- 收益統計
    COALESCE(SUM(CASE WHEN DATE(l.start_date) = CURRENT_DATE THEN l.earnings ELSE 0 END), 0) AS today_earnings,
    COALESCE(SUM(l.earnings), 0) AS total_earnings,
    
    -- 掛單統計
    COUNT(DISTINCT CASE WHEN o.status = 'active' THEN o.id END) AS active_offers,
    COUNT(DISTINCT CASE WHEN l.status = 'active' THEN l.id END) AS active_loans
    
FROM users u
LEFT JOIN offers o ON u.id = o.user_id
LEFT JOIN loans l ON u.id = l.user_id
WHERE u.is_active = true
GROUP BY u.id, u.email;
```

---

### view_earnings_trend

```sql
CREATE VIEW view_earnings_trend AS
SELECT 
    user_id,
    date,
    daily_earnings,
    SUM(daily_earnings) OVER (
        PARTITION BY user_id 
        ORDER BY date
    ) AS cumulative_earnings
FROM daily_stats
ORDER BY user_id, date DESC;
```

---

## 🔄 觸發器（Triggers）

### 自動更新 updated_at

```sql
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_strategies_updated_at
    BEFORE UPDATE ON strategies
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_offers_updated_at
    BEFORE UPDATE ON offers
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
```

---

### 自動計算收益

```sql
CREATE OR REPLACE FUNCTION calculate_loan_earnings()
RETURNS TRIGGER AS $$
BEGIN
    NEW.earnings = NEW.amount * NEW.rate * NEW.duration;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER calculate_earnings_on_insert
    BEFORE INSERT ON loans
    FOR EACH ROW
    EXECUTE FUNCTION calculate_loan_earnings();
```

---

## 📈 性能優化

### 1. 索引策略

```sql
-- 複合索引（常用查詢）
CREATE INDEX idx_offers_user_status ON offers(user_id, status);
CREATE INDEX idx_loans_user_status ON loans(user_id, status);
CREATE INDEX idx_loans_user_dates ON loans(user_id, start_date, end_date);

-- 部分索引（只索引活躍數據）
CREATE INDEX idx_active_offers ON offers(user_id) WHERE status = 'active';
CREATE INDEX idx_active_loans ON loans(user_id) WHERE status = 'active';
```

---

### 2. 分區策略（未來擴展）

```sql
-- 按月分區 logs 表
CREATE TABLE logs (
    -- ... columns
) PARTITION BY RANGE (timestamp);

CREATE TABLE logs_2025_01 PARTITION OF logs
    FOR VALUES FROM ('2025-01-01') TO ('2025-02-01');
```

---

## 🔒 安全性

### 1. 行級安全（RLS）

```sql
-- 啟用 RLS
ALTER TABLE offers ENABLE ROW LEVEL SECURITY;
ALTER TABLE loans ENABLE ROW LEVEL SECURITY;

-- 用戶只能查看自己的數據
CREATE POLICY user_own_offers ON offers
    FOR ALL TO authenticated_user
    USING (user_id = current_user_id());
```

---

### 2. 敏感數據加密

- API Keys 使用應用層加密（Fernet）
- 密碼使用 bcrypt (cost 12+)
- 資料庫連線使用 SSL

---

## 💾 備份策略

### 1. 全量備份
```bash
# 每日凌晨 2 點
pg_dump -U user -d dbname > backup_$(date +%Y%m%d).sql
```

### 2. 增量備份
```sql
-- 啟用 WAL 歸檔
archive_mode = on
archive_command = 'cp %p /backup/wal/%f'
```

---

## 🔄 資料遷移

使用 Alembic 管理：

```bash
# 創建遷移
alembic revision -m "create users table"

# 執行遷移
alembic upgrade head

# 回滾
alembic downgrade -1
```

---

下一步：閱讀 [資料遷移](./migrations.md) 了解具體遷移腳本。

