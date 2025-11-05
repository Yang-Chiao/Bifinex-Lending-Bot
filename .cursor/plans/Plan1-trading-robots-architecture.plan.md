# Plan 1: 核心基礎設施

## 🎯 目標
建立整個專案的基礎架構，讓團隊可以開始並行開發。

## 📅 時程
**Week 1** - 預計 1-2 天完成

## 🏗️ 交付物

### 1. Monorepo 結構
```
TradingRobots/
├── apps/                      # 應用層（後續建立）
├── packages/                  # 共用包
│   ├── config/               # ✅ 本次建立
│   └── types/                # ✅ 本次建立
├── docs/                     # 現有文檔
├── pnpm-workspace.yaml       # ✅ 本次建立
├── package.json              # ✅ 本次建立
├── .gitignore                # ✅ 本次建立
└── README.md                 # ✅ 本次更新
```

---

## 📦 實作內容

### Task 1.1: Monorepo 初始化

**1.1.1 根目錄配置**

`package.json`:
```json
{
  "name": "trading-robots",
  "version": "1.0.0",
  "private": true,
  "type": "module",
  "scripts": {
    "dev:backend": "cd apps/backend && python main.py",
    "dev:backstage": "pnpm --filter backstage dev",
    "dev:website": "pnpm --filter website dev",
    "build:all": "pnpm -r build",
    "clean": "pnpm -r clean && rm -rf node_modules"
  },
  "devDependencies": {
    "concurrently": "^8.2.2"
  }
}
```

`pnpm-workspace.yaml`:
```yaml
packages:
  - 'apps/*'
  - 'packages/*'
```

`.gitignore`:
```
# Dependencies
node_modules/
pnpm-lock.yaml

# Build outputs
dist/
build/
*.tsbuildinfo

# Environment
.env
.env.local

# Python
__pycache__/
*.py[cod]
.venv/
venv/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/
```

**1.1.2 更新根目錄 README**

添加：
- 專案結構說明
- 快速開始指南
- 各子專案連結
- Monorepo 使用說明

---

### Task 1.2: packages/config（共用配置包）

**目錄結構**:
```
packages/config/
├── src/
│   ├── typescript/
│   │   ├── base.json           # 基礎 TS 配置
│   │   ├── node.json           # Node.js 環境
│   │   └── react.json          # React 環境
│   ├── tailwind/
│   │   ├── base.config.js      # 基礎 Tailwind 配置
│   │   └── theme.js            # 共用主題（顏色、字體）
│   ├── eslint/
│   │   ├── base.js             # 基礎 ESLint 規則
│   │   ├── react.js            # React 專用
│   │   └── typescript.js       # TypeScript 規則
│   └── prettier/
│       └── index.js            # Prettier 配置
├── package.json
└── README.md
```

**1.2.1 TypeScript 配置**

`src/typescript/base.json`:
```json
{
  "$schema": "https://json.schemastore.org/tsconfig",
  "compilerOptions": {
    "target": "ES2020",
    "module": "ESNext",
    "lib": ["ES2020"],
    "moduleResolution": "bundler",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true
  }
}
```

`src/typescript/react.json`:
```json
{
  "extends": "./base.json",
  "compilerOptions": {
    "jsx": "react-jsx",
    "lib": ["ES2020", "DOM", "DOM.Iterable"]
  }
}
```

**1.2.2 Tailwind 配置**

`src/tailwind/theme.js`:
```javascript
// 共用主題配置
export const theme = {
  colors: {
    primary: {
      50: '#f0f9ff',
      100: '#e0f2fe',
      500: '#0ea5e9',
      600: '#0284c7',
      700: '#0369a1',
    },
    success: {
      500: '#22c55e',
      600: '#16a34a',
    },
    danger: {
      500: '#ef4444',
      600: '#dc2626',
    },
    warning: {
      500: '#f59e0b',
      600: '#d97706',
    },
  },
  fontFamily: {
    sans: ['Inter', 'sans-serif'],
    mono: ['Fira Code', 'monospace'],
  },
}
```

`src/tailwind/base.config.js`:
```javascript
import { theme } from './theme.js'

export default {
  content: [], // 各專案自行配置
  theme: {
    extend: theme,
  },
  plugins: [],
}
```

**1.2.3 ESLint 配置**

`src/eslint/base.js`:
```javascript
export default {
  env: {
    es2020: true,
    node: true,
  },
  extends: ['eslint:recommended'],
  parserOptions: {
    ecmaVersion: 2020,
    sourceType: 'module',
  },
  rules: {
    'no-console': 'warn',
    'no-unused-vars': ['error', { argsIgnorePattern: '^_' }],
  },
}
```

**1.2.4 package.json**

```json
{
  "name": "@trading-robots/config",
  "version": "1.0.0",
  "type": "module",
  "exports": {
    "./typescript/base": "./src/typescript/base.json",
    "./typescript/react": "./src/typescript/react.json",
    "./tailwind": "./src/tailwind/base.config.js",
    "./eslint/base": "./src/eslint/base.js"
  },
  "files": ["src"],
  "peerDependencies": {
    "tailwindcss": "^3.4.0",
    "typescript": "^5.0.0"
  }
}
```

---

### Task 1.3: packages/types（共用類型定義）

**目錄結構**:
```
packages/types/
├── src/
│   ├── api/                  # API 請求/響應類型
│   │   ├── auth.ts
│   │   ├── user.ts
│   │   ├── strategy.ts
│   │   ├── offer.ts
│   │   └── loan.ts
│   ├── entities/             # 實體類型
│   │   ├── user.ts
│   │   ├── strategy.ts
│   │   ├── offer.ts
│   │   └── loan.ts
│   ├── bitfinex/             # Bitfinex API 類型
│   │   ├── market.ts
│   │   ├── funding.ts
│   │   └── wallet.ts
│   ├── common/               # 通用類型
│   │   ├── pagination.ts
│   │   ├── response.ts
│   │   └── error.ts
│   └── index.ts              # 統一導出
├── package.json
├── tsconfig.json
└── README.md
```

**1.3.1 通用類型**

`src/common/response.ts`:
```typescript
/**
 * API 統一響應格式
 */
export interface ApiResponse<T = any> {
  success: boolean
  data?: T
  error?: ApiError
  message?: string
}

export interface ApiError {
  code: string
  message: string
  details?: Record<string, any>
}
```

`src/common/pagination.ts`:
```typescript
/**
 * 分頁請求參數
 */
export interface PaginationParams {
  page?: number
  limit?: number
  sortBy?: string
  sortOrder?: 'asc' | 'desc'
}

/**
 * 分頁響應數據
 */
export interface PaginatedResponse<T> {
  items: T[]
  total: number
  page: number
  limit: number
  totalPages: number
}
```

**1.3.2 用戶相關類型**

`src/entities/user.ts`:
```typescript
/**
 * 用戶實體
 */
export interface User {
  id: string
  email: string
  role: UserRole
  createdAt: string
  updatedAt: string
  isActive: boolean
}

export type UserRole = 'admin' | 'user'

export interface UserProfile extends User {
  hasBitfinexApiKey: boolean
  strategiesCount: number
  totalEarnings: number
}
```

`src/api/auth.ts`:
```typescript
import { User } from '../entities/user'

/**
 * 登入請求
 */
export interface LoginRequest {
  email: string
  password: string
}

/**
 * 登入響應
 */
export interface LoginResponse {
  accessToken: string
  refreshToken: string
  user: User
}

/**
 * 註冊請求
 */
export interface RegisterRequest {
  email: string
  password: string
  confirmPassword: string
}
```

**1.3.3 策略相關類型**

`src/entities/strategy.ts`:
```typescript
/**
 * 策略類型
 */
export type StrategyType = 'market_follow' | 'ladder' | 'fixed_rate'

/**
 * 策略實體
 */
export interface Strategy {
  id: string
  userId: string
  strategyType: StrategyType
  params: StrategyParams
  isActive: boolean
  createdAt: string
  updatedAt: string
}

/**
 * 策略參數（根據類型不同而不同）
 */
export type StrategyParams =
  | MarketFollowParams
  | LadderParams
  | FixedRateParams

export interface MarketFollowParams {
  rateMultiplier: number // 0.95 = 市場利率的 95%
  minRate: number
  maxRate: number
  duration: number // days
}

export interface LadderParams {
  levels: {
    amount: number
    rate: number
    duration: number
  }[]
}

export interface FixedRateParams {
  rate: number
  duration: number
}
```

`src/api/strategy.ts`:
```typescript
import { Strategy, StrategyParams, StrategyType } from '../entities/strategy'
import { PaginatedResponse } from '../common/pagination'

export interface CreateStrategyRequest {
  strategyType: StrategyType
  params: StrategyParams
  isActive?: boolean
}

export interface UpdateStrategyRequest {
  params?: StrategyParams
  isActive?: boolean
}

export type StrategyListResponse = PaginatedResponse<Strategy>
```

**1.3.4 Offer 和 Loan 類型**

`src/entities/offer.ts`:
```typescript
/**
 * 掛單狀態
 */
export type OfferStatus = 'active' | 'executed' | 'cancelled' | 'expired'

/**
 * 掛單實體
 */
export interface Offer {
  id: string
  userId: string
  bitfinexOfferId: number
  amount: number
  rate: number // 年化利率（小數，如 0.05 = 5%）
  duration: number // 天數
  status: OfferStatus
  createdAt: string
  updatedAt: string
}
```

`src/entities/loan.ts`:
```typescript
/**
 * 成交記錄狀態
 */
export type LoanStatus = 'active' | 'completed' | 'cancelled'

/**
 * 成交記錄實體
 */
export interface Loan {
  id: string
  userId: string
  offerId: string
  bitfinexLoanId: number
  amount: number
  rate: number
  startDate: string
  endDate: string
  earnings: number
  status: LoanStatus
  createdAt: string
}
```

**1.3.5 Bitfinex API 類型**

`src/bitfinex/market.ts`:
```typescript
/**
 * Bitfinex 市場數據
 */
export interface BitfinexTicker {
  symbol: string
  frr: number // Flash Return Rate
  bid: number
  bidPeriod: number
  bidSize: number
  ask: number
  askPeriod: number
  askSize: number
}

export interface BitfinexFundingBook {
  rate: number
  period: number
  count: number
  amount: number
}
```

`src/bitfinex/funding.ts`:
```typescript
/**
 * Bitfinex 放貸操作
 */
export interface BitfinexOfferRequest {
  type: 'LIMIT' | 'FRRDELTAVAR'
  symbol: string
  amount: string
  rate: string
  period: number
}

export interface BitfinexOfferResponse {
  id: number
  symbol: string
  amount: string
  rate: string
  period: number
  status: string
  timestamp: number
}
```

**1.3.6 統一導出**

`src/index.ts`:
```typescript
// Common
export * from './common/response'
export * from './common/pagination'
export * from './common/error'

// Entities
export * from './entities/user'
export * from './entities/strategy'
export * from './entities/offer'
export * from './entities/loan'

// API
export * from './api/auth'
export * from './api/user'
export * from './api/strategy'
export * from './api/offer'
export * from './api/loan'

// Bitfinex
export * from './bitfinex/market'
export * from './bitfinex/funding'
export * from './bitfinex/wallet'
```

**1.3.7 package.json**

```json
{
  "name": "@trading-robots/types",
  "version": "1.0.0",
  "type": "module",
  "main": "./src/index.ts",
  "types": "./src/index.ts",
  "exports": {
    ".": "./src/index.ts"
  },
  "files": ["src"],
  "scripts": {
    "typecheck": "tsc --noEmit"
  },
  "devDependencies": {
    "typescript": "^5.3.3"
  }
}
```

`tsconfig.json`:
```json
{
  "extends": "@trading-robots/config/typescript/base",
  "compilerOptions": {
    "outDir": "./dist",
    "rootDir": "./src",
    "declaration": true
  },
  "include": ["src/**/*"]
}
```

---

## ✅ 驗收標準

### 功能驗收
- [ ] pnpm workspace 正常工作
- [ ] 可以在根目錄執行 `pnpm install`
- [ ] `packages/config` 可以被其他包引用
- [ ] `packages/types` TypeScript 檢查通過
- [ ] 所有類型定義完整且合理

### 文檔驗收
- [ ] 根目錄 README 包含完整啟動指南
- [ ] 每個 package 都有 README 說明用途和使用方法

### 代碼品質
- [ ] 所有 TypeScript 類型都有適當的 JSDoc 註解
- [ ] 命名清晰一致
- [ ] Git commit 訊息清楚

---

## 📚 文檔更新

更新根目錄 `README.md`：
- Monorepo 結構說明
- 安裝依賴指南（`pnpm install`）
- 各 package 用途說明
- 下一步計劃（Plan 2 和 Plan 3）

---

## 🔗 後續依賴

完成此計劃後，可以並行進行：
- **Plan 2: Backend 架構與文檔**（依賴 packages/types）
- **Plan 3: UI 組件庫**（依賴 packages/config 和 packages/types）

---

## ⏱️ 預計時間

- Task 1.1: 30 分鐘
- Task 1.2: 1 小時
- Task 1.3: 2 小時
- 文檔撰寫: 30 分鐘

**總計：約 4 小時**

---

## 📋 Todos（9個任務）

1. ✅ 初始化 Monorepo（package.json、workspace、gitignore）
2. ✅ 建立 packages/config TypeScript 配置
3. ✅ 建立 packages/config Tailwind 配置和主題
4. ✅ 建立 packages/config ESLint 和 Prettier 配置
5. ✅ 建立 packages/types 通用類型（response、pagination）
6. ✅ 建立 packages/types 實體類型（User、Strategy、Offer、Loan）
7. ✅ 建立 packages/types API 類型（請求/響應）
8. ✅ 建立 packages/types Bitfinex API 類型
9. ✅ 更新根目錄 README 和各 package README

---