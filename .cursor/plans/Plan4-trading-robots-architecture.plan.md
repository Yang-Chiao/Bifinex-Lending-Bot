<!-- 76a17ffa-be37-4472-b601-1954698ec85b a096ee9f-3e95-45a0-b825-6360d9c6f9b1 -->
# Plan 4: Backstage 用戶後台

## 🎯 目標

建立用戶後台應用，提供完整的放貸機器人管理界面。

## 📅 時程

**Week 2-3** - 預計 3-4 天完成

## 📋 依賴關係

✅ 需要先完成：

- **Plan 1: 核心基礎設施**
- **Plan 2: Backend 架構**（至少 Auth API 完成）
- **Plan 3: UI 組件庫**

---

## 🏗️ 目錄結構

```
apps/backstage/
├── src/
│   ├── components/           # 頁面組件
│   │   ├── layout/
│   │   │   ├── Header.tsx
│   │   │   ├── Sidebar.tsx
│   │   │   └── MainLayout.tsx
│   │   ├── auth/
│   │   │   ├── LoginForm.tsx
│   │   │   └── ProtectedRoute.tsx
│   │   └── dashboard/
│   │       ├── StatsOverview.tsx
│   │       ├── RecentLoans.tsx
│   │       └── ActiveStrategies.tsx
│   │
│   ├── pages/                # 路由頁面
│   │   ├── Login.tsx
│   │   ├── Dashboard.tsx
│   │   ├── Strategies.tsx
│   │   ├── History.tsx
│   │   ├── Settings.tsx
│   │   └── NotFound.tsx
│   │
│   ├── hooks/                # 自定義 Hooks
│   │   ├── useAuth.ts
│   │   └── useApi.ts
│   │
│   ├── services/             # API 服務
│   │   ├── api.ts            # Axios 實例
│   │   ├── auth.service.ts
│   │   ├── strategy.service.ts
│   │   ├── offer.service.ts
│   │   └── loan.service.ts
│   │
│   ├── stores/               # Zustand 狀態管理
│   │   ├── auth.store.ts
│   │   └── user.store.ts
│   │
│   ├── lib/                  # 工具函數
│   │   ├── constants.ts
│   │   └── utils.ts
│   │
│   ├── App.tsx               # 應用入口
│   ├── main.tsx              # React 入口
│   └── router.tsx            # 路由配置
│
├── public/
│   └── favicon.ico
│
├── index.html
├── vite.config.ts
├── tailwind.config.js
├── tsconfig.json
├── package.json
└── README.md
```

---

## 📦 實作內容

### Task 4.1: 專案初始化

**4.1.1 package.json**

```json
{
  "name": "backstage",
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview",
    "typecheck": "tsc --noEmit"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.21.3",
    "axios": "^1.6.5",
    "@tanstack/react-query": "^5.17.19",
    "zustand": "^4.4.7",
    "lucide-react": "^0.309.0",
    "recharts": "^2.10.3",
    "@trading-robots/ui": "workspace:*",
    "@trading-robots/types": "workspace:*",
    "@trading-robots/config": "workspace:*"
  },
  "devDependencies": {
    "@types/react": "^18.2.48",
    "@types/react-dom": "^18.2.18",
    "@vitejs/plugin-react": "^4.2.1",
    "autoprefixer": "^10.4.17",
    "postcss": "^8.4.33",
    "tailwindcss": "^3.4.1",
    "typescript": "^5.3.3",
    "vite": "^5.0.11"
  }
}
```

**4.1.2 vite.config.ts**

```typescript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
})
```

**4.1.3 tailwind.config.js**

```javascript
import baseConfig from '@trading-robots/config/tailwind'

export default {
  ...baseConfig,
  content: [
    './index.html',
    './src/**/*.{js,ts,jsx,tsx}',
    '../../packages/ui/src/**/*.{js,ts,jsx,tsx}',
  ],
}
```

**4.1.4 tsconfig.json**

```json
{
  "extends": "@trading-robots/config/typescript/react",
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["src"],
  "references": [
    { "path": "../../packages/ui" },
    { "path": "../../packages/types" }
  ]
}
```

---

### Task 4.2: API 服務層

**4.2.1 src/services/api.ts**（Axios 配置）

```typescript
import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// 請求攔截器：添加 Token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

// 響應攔截器：處理錯誤
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token 過期，清除並跳轉到登入頁
      localStorage.removeItem('access_token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export default api
```

**4.2.2 src/services/auth.service.ts**

```typescript
import api from './api'
import type { LoginRequest, LoginResponse, RegisterRequest } from '@trading-robots/types'

export const authService = {
  async login(data: LoginRequest): Promise<LoginResponse> {
    const response = await api.post<LoginResponse>('/auth/login', data)
    return response.data
  },

  async register(data: RegisterRequest): Promise<{ message: string }> {
    const response = await api.post('/auth/register', data)
    return response.data
  },

  async getCurrentUser() {
    const response = await api.get('/auth/me')
    return response.data
  },

  logout() {
    localStorage.removeItem('access_token')
  },
}
```

**4.2.3 src/services/strategy.service.ts**

```typescript
import api from './api'
import type {
  Strategy,
  CreateStrategyRequest,
  UpdateStrategyRequest,
  StrategyListResponse,
  PaginationParams,
} from '@trading-robots/types'

export const strategyService = {
  async getAll(params?: PaginationParams): Promise<StrategyListResponse> {
    const response = await api.get<StrategyListResponse>('/strategies', { params })
    return response.data
  },

  async getById(id: string): Promise<Strategy> {
    const response = await api.get<Strategy>(`/strategies/${id}`)
    return response.data
  },

  async create(data: CreateStrategyRequest): Promise<Strategy> {
    const response = await api.post<Strategy>('/strategies', data)
    return response.data
  },

  async update(id: string, data: UpdateStrategyRequest): Promise<Strategy> {
    const response = await api.patch<Strategy>(`/strategies/${id}`, data)
    return response.data
  },

  async delete(id: string): Promise<void> {
    await api.delete(`/strategies/${id}`)
  },

  async toggle(id: string, isActive: boolean): Promise<Strategy> {
    const response = await api.patch<Strategy>(`/strategies/${id}`, { isActive })
    return response.data
  },
}
```

---

### Task 4.3: 狀態管理（Zustand）

**4.3.1 src/stores/auth.store.ts**

```typescript
import { create } from 'zustand'
import type { User } from '@trading-robots/types'

interface AuthState {
  user: User | null
  isAuthenticated: boolean
  setUser: (user: User | null) => void
  logout: () => void
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  isAuthenticated: false,
  setUser: (user) =>
    set({
      user,
      isAuthenticated: !!user,
    }),
  logout: () =>
    set({
      user: null,
      isAuthenticated: false,
    }),
}))
```

---

### Task 4.4: 自定義 Hooks

**4.4.1 src/hooks/useAuth.ts**

```typescript
import { useAuthStore } from '@/stores/auth.store'
import { authService } from '@/services/auth.service'
import { useMutation, useQuery } from '@tanstack/react-query'
import type { LoginRequest } from '@trading-robots/types'

export function useAuth() {
  const { user, isAuthenticated, setUser, logout: storeLogout } = useAuthStore()

  // 登入
  const loginMutation = useMutation({
    mutationFn: (data: LoginRequest) => authService.login(data),
    onSuccess: (response) => {
      localStorage.setItem('access_token', response.accessToken)
      setUser(response.user)
    },
  })

  // 獲取當前用戶
  const { refetch } = useQuery({
    queryKey: ['currentUser'],
    queryFn: authService.getCurrentUser,
    enabled: !!localStorage.getItem('access_token'),
    onSuccess: (data) => setUser(data),
  })

  // 登出
  const logout = () => {
    authService.logout()
    storeLogout()
  }

  return {
    user,
    isAuthenticated,
    login: loginMutation.mutateAsync,
    logout,
    refetch,
  }
}
```

---

### Task 4.5: 路由與布局

**4.5.1 src/router.tsx**

```typescript
import { createBrowserRouter } from 'react-router-dom'
import MainLayout from './components/layout/MainLayout'
import ProtectedRoute from './components/auth/ProtectedRoute'
import Login from './pages/Login'
import Dashboard from './pages/Dashboard'
import Strategies from './pages/Strategies'
import History from './pages/History'
import Settings from './pages/Settings'
import NotFound from './pages/NotFound'

export const router = createBrowserRouter([
  {
    path: '/login',
    element: <Login />,
  },
  {
    path: '/',
    element: (
      <ProtectedRoute>
        <MainLayout />
      </ProtectedRoute>
    ),
    children: [
      {
        index: true,
        element: <Dashboard />,
      },
      {
        path: 'strategies',
        element: <Strategies />,
      },
      {
        path: 'history',
        element: <History />,
      },
      {
        path: 'settings',
        element: <Settings />,
      },
    ],
  },
  {
    path: '*',
    element: <NotFound />,
  },
])
```

**4.5.2 src/components/auth/ProtectedRoute.tsx**

```typescript
import { Navigate } from 'react-router-dom'
import { useAuth } from '@/hooks/useAuth'

interface ProtectedRouteProps {
  children: React.ReactNode
}

export default function ProtectedRoute({ children }: ProtectedRouteProps) {
  const { isAuthenticated } = useAuth()

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />
  }

  return <>{children}</>
}
```

**4.5.3 src/components/layout/MainLayout.tsx**

```typescript
import { Outlet } from 'react-router-dom'
import Header from './Header'
import Sidebar from './Sidebar'

export default function MainLayout() {
  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      <div className="flex">
        <Sidebar />
        <main className="flex-1 p-6">
          <Outlet />
        </main>
      </div>
    </div>
  )
}
```

**4.5.4 src/components/layout/Header.tsx**

```typescript
import { useAuth } from '@/hooks/useAuth'
import { Button } from '@trading-robots/ui'
import { LogOut, User } from 'lucide-react'

export default function Header() {
  const { user, logout } = useAuth()

  return (
    <header className="bg-white border-b border-gray-200 h-16 flex items-center justify-between px-6">
      <h1 className="text-xl font-bold text-primary-600">Trading Robots</h1>
      <div className="flex items-center gap-4">
        <div className="flex items-center gap-2">
          <User className="h-5 w-5 text-gray-400" />
          <span className="text-sm text-gray-700">{user?.email}</span>
        </div>
        <Button variant="ghost" size="sm" onClick={logout}>
          <LogOut className="h-4 w-4 mr-2" />
          Logout
        </Button>
      </div>
    </header>
  )
}
```

**4.5.5 src/components/layout/Sidebar.tsx**

```typescript
import { NavLink } from 'react-router-dom'
import { LayoutDashboard, TrendingUp, History, Settings } from 'lucide-react'
import { cn } from '@trading-robots/ui'

const navigation = [
  { name: 'Dashboard', href: '/', icon: LayoutDashboard },
  { name: 'Strategies', href: '/strategies', icon: TrendingUp },
  { name: 'History', href: '/history', icon: History },
  { name: 'Settings', href: '/settings', icon: Settings },
]

export default function Sidebar() {
  return (
    <aside className="w-64 bg-white border-r border-gray-200 min-h-[calc(100vh-4rem)]">
      <nav className="p-4 space-y-1">
        {navigation.map((item) => (
          <NavLink
            key={item.name}
            to={item.href}
            end={item.href === '/'}
            className={({ isActive }) =>
              cn(
                'flex items-center gap-3 px-4 py-3 rounded-lg text-sm font-medium transition-colors',
                isActive
                  ? 'bg-primary-50 text-primary-700'
                  : 'text-gray-700 hover:bg-gray-50'
              )
            }
          >
            <item.icon className="h-5 w-5" />
            {item.name}
          </NavLink>
        ))}
      </nav>
    </aside>
  )
}
```

---

### Task 4.6: 核心頁面

**4.6.1 src/pages/Login.tsx**

```typescript
import { useState } from 'react'
import { Navigate } from 'react-router-dom'
import { useAuth } from '@/hooks/useAuth'
import { Button, Card, CardContent, CardHeader, CardTitle, Input } from '@trading-robots/ui'

export default function Login() {
  const { isAuthenticated, login } = useAuth()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')

  if (isAuthenticated) {
    return <Navigate to="/" replace />
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    try {
      await login({ email, password })
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Login failed')
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <Card className="w-full max-w-md">
        <CardHeader>
          <CardTitle className="text-center">Trading Robots</CardTitle>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium mb-1">Email</label>
              <Input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Password</label>
              <Input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>
            {error && <p className="text-sm text-red-600">{error}</p>}
            <Button type="submit" className="w-full">
              Login
            </Button>
          </form>
        </CardContent>
      </Card>
    </div>
  )
}
```

**4.6.2 src/pages/Dashboard.tsx**

```typescript
import { useQuery } from '@tanstack/react-query'
import { StatCard } from '@trading-robots/ui'
import { DollarSign, TrendingUp, Activity } from 'lucide-react'

export default function Dashboard() {
  // TODO: 實際 API 呼叫
  const stats = {
    totalEarnings: 1234.56,
    activeStrategies: 3,
    activeLoans: 5,
  }

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Dashboard</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <StatCard
          title="Total Earnings"
          value={stats.totalEarnings}
          format="currency"
          change={0.15}
          icon={<DollarSign className="h-5 w-5" />}
        />
        <StatCard
          title="Active Strategies"
          value={stats.activeStrategies}
          icon={<TrendingUp className="h-5 w-5" />}
        />
        <StatCard
          title="Active Loans"
          value={stats.activeLoans}
          icon={<Activity className="h-5 w-5" />}
        />
      </div>

      {/* TODO: 添加圖表和最近記錄 */}
    </div>
  )
}
```

**4.6.3 src/pages/Strategies.tsx**

```typescript
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { strategyService } from '@/services/strategy.service'
import { StrategyCard, Button } from '@trading-robots/ui'
import { Plus } from 'lucide-react'

export default function Strategies() {
  const queryClient = useQueryClient()

  const { data: strategies, isLoading } = useQuery({
    queryKey: ['strategies'],
    queryFn: () => strategyService.getAll(),
  })

  const toggleMutation = useMutation({
    mutationFn: ({ id, isActive }: { id: string; isActive: boolean }) =>
      strategyService.toggle(id, isActive),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['strategies'] })
    },
  })

  if (isLoading) return <div>Loading...</div>

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold">Strategies</h1>
        <Button>
          <Plus className="h-4 w-4 mr-2" />
          New Strategy
        </Button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {strategies?.items.map((strategy) => (
          <StrategyCard
            key={strategy.id}
            strategy={strategy}
            onToggle={(id, isActive) => toggleMutation.mutate({ id, isActive })}
          />
        ))}
      </div>
    </div>
  )
}
```

**4.6.4 src/pages/History.tsx**

```typescript
import { useQuery } from '@tanstack/react-query'
import { LoanHistoryTable } from '@trading-robots/ui'

export default function History() {
  // TODO: 實際 API 呼叫
  const loans = []

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">History</h1>
      <LoanHistoryTable loans={loans} />
    </div>
  )
}
```

**4.6.5 src/pages/Settings.tsx**

```typescript
import { Card, CardContent, CardHeader, CardTitle } from '@trading-robots/ui'

export default function Settings() {
  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Settings</h1>
      <Card>
        <CardHeader>
          <CardTitle>Account Settings</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-gray-600">Settings page coming soon...</p>
        </CardContent>
      </Card>
    </div>
  )
}
```

---

### Task 4.7: 應用入口

**4.7.1 src/App.tsx**

```typescript
import { RouterProvider } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { router } from './router'

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
    },
  },
})

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <RouterProvider router={router} />
    </QueryClientProvider>
  )
}

export default App
```

**4.7.2 src/main.tsx**

```typescript
import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
)
```

**4.7.3 src/index.css**

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

:root {
  --radius: 0.5rem;
}
```

---

## ✅ 驗收標準

### 功能完整性

- [ ] 登入功能正常（連接到 Backend Auth API）
- [ ] 登入後可以訪問 Dashboard
- [ ] 未登入時自動跳轉到 Login
- [ ] 側邊欄導航正常切換頁面
- [ ] 登出功能正常

### UI/UX

- [ ] 使用共用 UI 組件庫（@trading-robots/ui）
- [ ] 響應式設計（支援桌面和平板）
- [ ] 視覺風格統一
- [ ] Loading 和 Error 狀態處理

### 代碼品質

- [ ] TypeScript 檢查通過
- [ ] API 服務層結構清晰
- [ ] 狀態管理正確使用
- [ ] 無 Console 錯誤

### 文檔

- [ ] README 包含啟動指南
- [ ] 環境變數說明

---

## 📚 後續優化（本次不實作）

- 添加 Toast 通知系統
- 實作策略創建/編輯表單
- 添加數據圖表（Recharts）
- 實作分頁和搜索
- 添加 Loading Skeleton
- Error Boundary

---

## ⏱️ 預計時間

- Task 4.1-4.2: 2 小時（初始化和 API 層）
- Task 4.3-4.4: 2 小時（狀態和 Hooks）
- Task 4.5: 3 小時（路由和布局）
- Task 4.6: 4 小時（頁面實作）
- Task 4.7: 1 小時（整合和測試）

**總計：約 12 小時（1.5-2 個工作日）**

### To-dos

- [ ] 初始化 Backstage 專案（package.json, vite, tailwind, tsconfig）
- [ ] 建立 API 服務層（api.ts, auth, strategy）
- [ ] 建立 Zustand stores（auth, user）
- [ ] 實作自定義 Hooks（useAuth, useApi）
- [ ] 實作布局組件（Header, Sidebar, MainLayout）
- [ ] 實作認證組件（LoginForm, ProtectedRoute）
- [ ] 配置路由系統（React Router）
- [ ] 實作 Login 頁面
- [ ] 實作 Dashboard 頁面
- [ ] 實作 Strategies 頁面
- [ ] 實作 History 和 Settings 頁面（基礎版）
- [ ] 整合 App.tsx 和 main.tsx，配置 React Query