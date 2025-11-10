# 前端技術棧

## 📦 核心技術

### React 18
```json
{
  "version": "^18.2.0",
  "用途": "UI 框架",
  "特性": [
    "Concurrent Rendering",
    "Automatic Batching",
    "Hooks API"
  ]
}
```

**選擇理由**：
- ✅ 生態系最成熟
- ✅ TypeScript 支援完善
- ✅ 豐富的第三方組件庫
- ✅ 團隊熟悉度高

---

### TypeScript
```json
{
  "version": "^5.0.0",
  "用途": "類型安全",
  "配置": "strict mode"
}
```

**優勢**：
- ✅ 編譯時錯誤檢查
- ✅ 智能提示
- ✅ 重構安全
- ✅ 自我文檔化

---

### Vite
```json
{
  "version": "^5.0.0",
  "用途": "建構工具",
  "特點": "極快的冷啟動"
}
```

**優勢**：
- ✅ HMR 超快（<50ms）
- ✅ 開箱即用 TypeScript
- ✅ 生產打包優化
- ✅ 插件生態豐富

---

## 🎨 UI 框架與組件

### TailwindCSS
```json
{
  "version": "^3.4.0",
  "用途": "CSS 框架",
  "方法": "Utility-first"
}
```

**配置**：
```javascript
// tailwind.config.js
module.exports = {
  darkMode: 'class',
  content: ['./src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        // 加密貨幣風格色彩
        primary: {
          50: '#f0f9ff',
          // ...
          900: '#0c4a6e'
        }
      }
    }
  }
}
```

---

### shadcn/ui
```json
{
  "version": "latest",
  "用途": "UI 組件庫",
  "特點": "可複製的組件"
}
```

**使用的組件**：
```typescript
// 基礎組件
- Button
- Input
- Card
- Dialog
- Dropdown Menu
- Select
- Switch
- Slider
- Tabs

// 數據展示
- Table
- Badge
- Progress
- Skeleton

// 反饋
- Toast
- Alert
- Loading
```

**安裝命令**：
```bash
npx shadcn-ui@latest init
npx shadcn-ui@latest add button
npx shadcn-ui@latest add card
# ... 按需安裝
```

---

### Radix UI
```json
{
  "version": "latest",
  "用途": "無障礙組件基礎",
  "特點": "shadcn/ui 的底層"
}
```

**優勢**：
- ✅ WAI-ARIA 兼容
- ✅ 鍵盤導航支援
- ✅ 無樣式（可自定義）

---

## 📊 數據管理

### React Query (TanStack Query)
```json
{
  "version": "^5.0.0",
  "用途": "服務端狀態管理"
}
```

**核心功能**：
```typescript
// 數據獲取
const { data, isLoading, error } = useQuery({
  queryKey: ['dashboard'],
  queryFn: fetchDashboard
})

// 數據更新
const mutation = useMutation({
  mutationFn: updateStrategy,
  onSuccess: () => {
    queryClient.invalidateQueries(['dashboard'])
  }
})

// 自動重新獲取
useQuery({
  queryKey: ['offers'],
  queryFn: fetchOffers,
  refetchInterval: 30000  // 30 秒
})
```

**優勢**：
- ✅ 自動快取
- ✅ 背景更新
- ✅ 重試機制
- ✅ 樂觀更新

---

### Zustand
```json
{
  "version": "^4.5.0",
  "用途": "客戶端狀態管理"
}
```

**使用場景**：
```typescript
// stores/auth.ts
import { create } from 'zustand'

interface AuthStore {
  user: User | null
  token: string | null
  login: (email: string, password: string) => Promise<void>
  logout: () => void
}

export const useAuthStore = create<AuthStore>((set) => ({
  user: null,
  token: localStorage.getItem('token'),
  
  login: async (email, password) => {
    const { user, token } = await authAPI.login(email, password)
    localStorage.setItem('token', token)
    set({ user, token })
  },
  
  logout: () => {
    localStorage.removeItem('token')
    set({ user: null, token: null })
  }
}))
```

**優勢**：
- ✅ 極簡 API
- ✅ 無需 Provider
- ✅ TypeScript 友好
- ✅ DevTools 支援

---

## 📈 圖表庫

### Recharts
```json
{
  "version": "^2.10.0",
  "用途": "數據視覺化"
}
```

**使用範例**：
```typescript
import { LineChart, Line, XAxis, YAxis, Tooltip } from 'recharts'

<LineChart width={600} height={300} data={earningsData}>
  <XAxis dataKey="date" />
  <YAxis />
  <Tooltip />
  <Line 
    type="monotone" 
    dataKey="earnings" 
    stroke="#8884d8" 
    strokeWidth={2}
  />
</LineChart>
```

**支援的圖表**：
- 折線圖（Line Chart）
- 柱狀圖（Bar Chart）
- 面積圖（Area Chart）
- 餅圖（Pie Chart）
- 進度圓（Radial Bar）

---

## 🛣️ 路由

### React Router
```json
{
  "version": "^6.20.0",
  "用途": "客戶端路由"
}
```

**路由結構**：
```typescript
import { createBrowserRouter } from 'react-router-dom'

const router = createBrowserRouter([
  {
    path: '/',
    element: <Layout />,
    children: [
      { path: '/', element: <Dashboard /> },
      { path: '/history', element: <History /> },
      { path: '/strategy', element: <Strategy /> },
      { path: '/settings', element: <Settings /> },
      {
        path: '/admin',
        element: <ProtectedRoute role="admin" />,
        children: [
          { path: 'users', element: <UserManagement /> },
          { path: 'system', element: <SystemMonitor /> }
        ]
      }
    ]
  },
  { path: '/login', element: <Login /> },
  { path: '/register', element: <Register /> }
])
```

---

## 📝 表單處理

### React Hook Form
```json
{
  "version": "^7.48.0",
  "用途": "表單管理"
}
```

**使用範例**：
```typescript
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'

const schema = z.object({
  minRate: z.number().min(0).max(1),
  duration: z.enum(['2', '7', '30'])
})

function StrategyForm() {
  const { register, handleSubmit, formState: { errors } } = useForm({
    resolver: zodResolver(schema)
  })
  
  const onSubmit = (data) => {
    mutation.mutate(data)
  }
  
  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input {...register('minRate')} />
      {errors.minRate && <span>{errors.minRate.message}</span>}
    </form>
  )
}
```

---

### Zod
```json
{
  "version": "^3.22.0",
  "用途": "運行時類型驗證"
}
```

**優勢**：
- ✅ TypeScript 類型推導
- ✅ 詳細的錯誤訊息
- ✅ 可組合的驗證規則

---

## 🎭 動畫

### Framer Motion
```json
{
  "version": "^10.16.0",
  "用途": "動畫庫"
}
```

**使用場景**：
```typescript
import { motion } from 'framer-motion'

// 數字跳動
<motion.div
  initial={{ scale: 1 }}
  animate={{ scale: 1.1 }}
  transition={{ duration: 0.3 }}
>
  ${earnings}
</motion.div>

// 列表動畫
<motion.ul>
  {items.map((item, i) => (
    <motion.li
      key={item.id}
      initial={{ opacity: 0, x: -20 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ delay: i * 0.1 }}
    >
      {item.name}
    </motion.li>
  ))}
</motion.ul>
```

---

## 🔧 工具庫

### date-fns
```json
{
  "version": "^3.0.0",
  "用途": "日期處理"
}
```

```typescript
import { format, differenceInDays } from 'date-fns'

format(new Date(), 'yyyy-MM-dd HH:mm:ss')
differenceInDays(endDate, startDate)
```

---

### Axios
```json
{
  "version": "^1.6.0",
  "用途": "HTTP 請求"
}
```

**配置範例**：
```typescript
// services/api.ts
import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  timeout: 10000
})

// 請求攔截器
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
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
      // 跳轉到登入頁
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export default api
```

---

### Lucide Icons
```json
{
  "version": "^0.300.0",
  "用途": "圖標庫"
}
```

```typescript
import { TrendingUp, AlertCircle, Settings } from 'lucide-react'

<TrendingUp className="w-4 h-4" />
```

---

## 📦 完整 package.json

```json
{
  "name": "bitfinex-lending-frontend",
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview",
    "lint": "eslint . --ext ts,tsx",
    "type-check": "tsc --noEmit"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.20.0",
    "@tanstack/react-query": "^5.0.0",
    "zustand": "^4.5.0",
    "axios": "^1.6.0",
    "react-hook-form": "^7.48.0",
    "@hookform/resolvers": "^3.3.0",
    "zod": "^3.22.0",
    "recharts": "^2.10.0",
    "framer-motion": "^10.16.0",
    "date-fns": "^3.0.0",
    "lucide-react": "^0.300.0",
    "clsx": "^2.0.0",
    "tailwind-merge": "^2.2.0"
  },
  "devDependencies": {
    "@types/react": "^18.2.0",
    "@types/react-dom": "^18.2.0",
    "@vitejs/plugin-react": "^4.2.0",
    "typescript": "^5.3.0",
    "vite": "^5.0.0",
    "tailwindcss": "^3.4.0",
    "postcss": "^8.4.0",
    "autoprefixer": "^10.4.0",
    "eslint": "^8.55.0",
    "@typescript-eslint/eslint-plugin": "^6.15.0",
    "@typescript-eslint/parser": "^6.15.0"
  }
}
```

---

## 🎯 開發工具

### VS Code 推薦擴展
```json
{
  "recommendations": [
    "dbaeumer.vscode-eslint",
    "esbenp.prettier-vscode",
    "bradlc.vscode-tailwindcss",
    "lokalise.i18n-ally"
  ]
}
```

### ESLint 配置
```javascript
// .eslintrc.cjs
module.exports = {
  extends: [
    'eslint:recommended',
    'plugin:@typescript-eslint/recommended',
    'plugin:react-hooks/recommended'
  ],
  rules: {
    '@typescript-eslint/no-unused-vars': 'warn',
    'react-hooks/exhaustive-deps': 'warn'
  }
}
```

---

## 🚀 開發工作流

```bash
# 安裝依賴
npm install

# 啟動開發服務器
npm run dev

# 類型檢查
npm run type-check

# 建構生產版本
npm run build

# 預覽生產版本
npm run preview
```

---

下一步：閱讀 [後端技術棧](./backend.md) 了解後端技術選型。

