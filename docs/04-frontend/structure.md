# 前端專案結構

## 📁 目錄架構

```
frontend/
├── public/                    # 靜態資源
│   ├── favicon.ico
│   └── logo.svg
│
├── src/
│   ├── assets/               # 圖片、字體等資源
│   │   ├── images/
│   │   └── fonts/
│   │
│   ├── components/           # 組件
│   │   ├── ui/              # shadcn/ui 基礎組件
│   │   │   ├── button.tsx
│   │   │   ├── card.tsx
│   │   │   ├── dialog.tsx
│   │   │   ├── input.tsx
│   │   │   ├── select.tsx
│   │   │   ├── table.tsx
│   │   │   └── ...
│   │   │
│   │   ├── charts/          # 圖表組件
│   │   │   ├── EarningsChart.tsx
│   │   │   ├── UsageChart.tsx
│   │   │   └── RateDistribution.tsx
│   │   │
│   │   ├── forms/           # 表單組件
│   │   │   ├── LoginForm.tsx
│   │   │   ├── StrategyForm.tsx
│   │   │   └── SettingsForm.tsx
│   │   │
│   │   ├── layout/          # 布局組件
│   │   │   ├── Header.tsx
│   │   │   ├── Sidebar.tsx
│   │   │   ├── Footer.tsx
│   │   │   └── MainLayout.tsx
│   │   │
│   │   └── widgets/         # 小部件
│   │       ├── StatCard.tsx
│   │       ├── OffersList.tsx
│   │       └── NotificationBell.tsx
│   │
│   ├── pages/               # 頁面組件
│   │   ├── Dashboard/
│   │   │   ├── index.tsx
│   │   │   └── components/
│   │   │       ├── StatsSection.tsx
│   │   │       ├── ChartsSection.tsx
│   │   │       └── ActiveOffers.tsx
│   │   │
│   │   ├── History/
│   │   │   ├── index.tsx
│   │   │   └── components/
│   │   │       ├── HistoryTable.tsx
│   │   │       └── Filters.tsx
│   │   │
│   │   ├── Strategy/
│   │   │   ├── index.tsx
│   │   │   └── components/
│   │   │       ├── StrategySelector.tsx
│   │   │       └── ParametersForm.tsx
│   │   │
│   │   ├── Settings/
│   │   │   ├── index.tsx
│   │   │   └── components/
│   │   │       ├── ProfileSettings.tsx
│   │   │       ├── APISettings.tsx
│   │   │       └── NotificationSettings.tsx
│   │   │
│   │   ├── Admin/
│   │   │   ├── Users/
│   │   │   │   └── index.tsx
│   │   │   └── System/
│   │   │       └── index.tsx
│   │   │
│   │   ├── Login/
│   │   │   └── index.tsx
│   │   │
│   │   └── Register/
│   │       └── index.tsx
│   │
│   ├── hooks/               # 自定義 Hooks
│   │   ├── useAuth.ts
│   │   ├── useDashboard.ts
│   │   ├── useOffers.ts
│   │   ├── useStrategy.ts
│   │   └── useWebSocket.ts
│   │
│   ├── services/            # API 服務
│   │   ├── api.ts          # Axios 實例
│   │   ├── auth.service.ts
│   │   ├── dashboard.service.ts
│   │   ├── offers.service.ts
│   │   ├── loans.service.ts
│   │   └── admin.service.ts
│   │
│   ├── stores/              # Zustand 狀態管理
│   │   ├── authStore.ts
│   │   ├── themeStore.ts
│   │   └── notificationStore.ts
│   │
│   ├── types/               # TypeScript 類型定義
│   │   ├── api.types.ts
│   │   ├── user.types.ts
│   │   ├── offer.types.ts
│   │   ├── loan.types.ts
│   │   └── strategy.types.ts
│   │
│   ├── utils/               # 工具函數
│   │   ├── formatters.ts   # 格式化函數
│   │   ├── validators.ts   # 驗證函數
│   │   ├── constants.ts    # 常量
│   │   └── helpers.ts      # 輔助函數
│   │
│   ├── lib/                 # 第三方庫配置
│   │   └── utils.ts        # cn() 等工具
│   │
│   ├── styles/              # 全域樣式
│   │   └── globals.css
│   │
│   ├── App.tsx              # 根組件
│   ├── main.tsx             # 入口文件
│   └── vite-env.d.ts        # Vite 類型定義
│
├── .env.example             # 環境變數範本
├── .env.development         # 開發環境
├── .env.production          # 生產環境
├── .eslintrc.cjs            # ESLint 配置
├── .prettierrc              # Prettier 配置
├── components.json          # shadcn/ui 配置
├── index.html
├── package.json
├── postcss.config.js
├── tailwind.config.js
├── tsconfig.json
├── tsconfig.node.json
└── vite.config.ts
```

---

## 📝 核心文件說明

### main.tsx
```typescript
import React from 'react'
import ReactDOM from 'react-dom/client'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { RouterProvider } from 'react-router-dom'
import { Toaster } from '@/components/ui/toaster'
import { router } from './router'
import './styles/globals.css'

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1
    }
  }
})

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <RouterProvider router={router} />
      <Toaster />
    </QueryClientProvider>
  </React.StrictMode>
)
```

---

### router.tsx
```typescript
import { createBrowserRouter } from 'react-router-dom'
import { MainLayout } from '@/components/layout/MainLayout'
import { ProtectedRoute } from '@/components/auth/ProtectedRoute'
import Dashboard from '@/pages/Dashboard'
import History from '@/pages/History'
import Strategy from '@/pages/Strategy'
import Settings from '@/pages/Settings'
import AdminUsers from '@/pages/Admin/Users'
import Login from '@/pages/Login'

export const router = createBrowserRouter([
  {
    path: '/',
    element: <ProtectedRoute><MainLayout /></ProtectedRoute>,
    children: [
      { index: true, element: <Dashboard /> },
      { path: 'history', element: <History /> },
      { path: 'strategy', element: <Strategy /> },
      { path: 'settings', element: <Settings /> },
      {
        path: 'admin',
        element: <ProtectedRoute role="admin"><AdminUsers /></ProtectedRoute>
      }
    ]
  },
  { path: '/login', element: <Login /> }
])
```

---

### services/api.ts
```typescript
import axios from 'axios'
import { useAuthStore } from '@/stores/authStore'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  timeout: 10000
})

// 請求攔截器
api.interceptors.request.use((config) => {
  const token = useAuthStore.getState().token
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// 響應攔截器
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      useAuthStore.getState().logout()
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export default api
```

---

### stores/authStore.ts
```typescript
import { create } from 'zustand'
import { persist } from 'zustand/middleware'

interface User {
  id: number
  email: string
  role: 'admin' | 'user'
}

interface AuthStore {
  user: User | null
  token: string | null
  login: (email: string, password: string) => Promise<void>
  logout: () => void
  isAuthenticated: () => boolean
}

export const useAuthStore = create<AuthStore>()(
  persist(
    (set, get) => ({
      user: null,
      token: null,
      
      login: async (email, password) => {
        const response = await api.post('/auth/login', { email, password })
        set({ user: response.data.user, token: response.data.token })
      },
      
      logout: () => {
        set({ user: null, token: null })
      },
      
      isAuthenticated: () => !!get().token
    }),
    { name: 'auth-storage' }
  )
)
```

---

## 🎨 組件設計原則

### 1. 組件分類

#### 基礎組件（UI Components）
- 來自 shadcn/ui
- 可配置、可重用
- 無業務邏輯

#### 業務組件（Business Components）
- 包含業務邏輯
- 連接 API
- 管理狀態

#### 頁面組件（Page Components）
- 組合其他組件
- 定義路由
- 處理頁面級狀態

---

### 2. 命名規範

```typescript
// 組件文件：PascalCase
StatCard.tsx
EarningsChart.tsx

// 工具函數：camelCase
formatCurrency.ts
validateEmail.ts

// 類型定義：PascalCase
User.types.ts
Offer.types.ts

// Hook：use 開頭 + camelCase
useAuth.ts
useDashboard.ts
```

---

### 3. 組件模板

```typescript
import { FC } from 'react'

interface StatCardProps {
  title: string
  value: string | number
  change?: number
  icon?: React.ReactNode
}

export const StatCard: FC<StatCardProps> = ({
  title,
  value,
  change,
  icon
}) => {
  return (
    <div className="p-6 bg-card rounded-lg shadow">
      <div className="flex justify-between items-start">
        <div>
          <p className="text-sm text-muted-foreground">{title}</p>
          <h3 className="text-2xl font-bold mt-2">{value}</h3>
          {change && (
            <p className={cn(
              "text-sm mt-1",
              change > 0 ? "text-green-500" : "text-red-500"
            )}>
              {change > 0 ? '+' : ''}{change}%
            </p>
          )}
        </div>
        {icon && <div className="text-muted-foreground">{icon}</div>}
      </div>
    </div>
  )
}
```

---

## 🔧 配置文件

### vite.config.ts
```typescript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src')
    }
  },
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true
      }
    }
  }
})
```

---

### tailwind.config.js
```javascript
module.exports = {
  darkMode: ['class'],
  content: [
    './index.html',
    './src/**/*.{ts,tsx}'
  ],
  theme: {
    extend: {
      colors: {
        border: 'hsl(var(--border))',
        background: 'hsl(var(--background))',
        foreground: 'hsl(var(--foreground))',
        primary: {
          DEFAULT: 'hsl(var(--primary))',
          foreground: 'hsl(var(--primary-foreground))'
        }
      }
    }
  },
  plugins: [require('tailwindcss-animate')]
}
```

---

## 📦 package.json Scripts

```json
{
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview",
    "lint": "eslint . --ext ts,tsx --report-unused-disable-directives --max-warnings 0",
    "lint:fix": "eslint . --ext ts,tsx --fix",
    "type-check": "tsc --noEmit",
    "format": "prettier --write \"src/**/*.{ts,tsx,css}\""
  }
}
```

---

下一步：閱讀 [組件設計](./components.md) 了解具體組件實現。

