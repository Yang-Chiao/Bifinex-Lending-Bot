<!-- 76a17ffa-be37-4472-b601-1954698ec85b c2de8ebc-d858-426c-a62a-b60d9be47029 -->
# Plan 3: UI 組件庫

## 🎯 目標

建立共用 UI 組件庫，為兩個前端應用（Backstage、Website）提供一致的設計系統。

## 📅 時程

**Week 1-2** - 預計 2-3 天完成（可與 Plan 2 並行）

## 📋 依賴關係

✅ 需要先完成：**Plan 1（核心基礎設施）**

- 使用 `@trading-robots/config` 的 Tailwind 和 TypeScript 配置
- 使用 `@trading-robots/types` 的類型定義

---

## 🏗️ 目錄結構

```
packages/ui/
├── src/
│   ├── components/           # UI 組件
│   │   ├── ui/              # 基礎組件（shadcn/ui）
│   │   │   ├── button.tsx
│   │   │   ├── card.tsx
│   │   │   ├── input.tsx
│   │   │   ├── select.tsx
│   │   │   ├── textarea.tsx
│   │   │   ├── badge.tsx
│   │   │   ├── dialog.tsx
│   │   │   ├── table.tsx
│   │   │   ├── tabs.tsx
│   │   │   ├── alert.tsx
│   │   │   └── index.ts
│   │   │
│   │   └── business/        # 業務組件
│   │       ├── stat-card.tsx
│   │       ├── strategy-card.tsx
│   │       ├── loan-history-table.tsx
│   │       ├── rate-display.tsx
│   │       └── index.ts
│   │
│   ├── hooks/               # 共用 Hooks
│   │   ├── use-toast.ts
│   │   └── index.ts
│   │
│   ├── lib/                 # 工具函數
│   │   ├── utils.ts         # cn() 等工具
│   │   └── index.ts
│   │
│   └── index.ts             # 統一導出
│
├── package.json
├── tsconfig.json
├── tailwind.config.js
├── postcss.config.js
├── vite.config.ts           # 用於構建
└── README.md
```

---

## 📦 實作內容

### Task 3.1: 專案初始化

**3.1.1 package.json**

```json
{
  "name": "@trading-robots/ui",
  "version": "1.0.0",
  "type": "module",
  "main": "./src/index.ts",
  "types": "./src/index.ts",
  "exports": {
    ".": "./src/index.ts",
    "./components/*": "./src/components/*/index.ts"
  },
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "typecheck": "tsc --noEmit"
  },
  "dependencies": {
    "@radix-ui/react-dialog": "^1.0.5",
    "@radix-ui/react-dropdown-menu": "^2.0.6",
    "@radix-ui/react-select": "^2.0.0",
    "@radix-ui/react-tabs": "^1.0.4",
    "@radix-ui/react-slot": "^1.0.2",
    "class-variance-authority": "^0.7.0",
    "clsx": "^2.1.0",
    "tailwind-merge": "^2.2.0",
    "lucide-react": "^0.309.0",
    "@trading-robots/types": "workspace:*",
    "@trading-robots/config": "workspace:*"
  },
  "peerDependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0"
  },
  "devDependencies": {
    "@types/react": "^18.2.48",
    "@types/react-dom": "^18.2.18",
    "autoprefixer": "^10.4.17",
    "postcss": "^8.4.33",
    "tailwindcss": "^3.4.1",
    "typescript": "^5.3.3",
    "vite": "^5.0.11"
  }
}
```

**3.1.2 tsconfig.json**

```json
{
  "extends": "@trading-robots/config/typescript/react",
  "compilerOptions": {
    "outDir": "./dist",
    "rootDir": "./src",
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

**3.1.3 tailwind.config.js**

```javascript
import baseConfig from '@trading-robots/config/tailwind'

export default {
  ...baseConfig,
  content: ['./src/**/*.{ts,tsx}'],
  theme: {
    ...baseConfig.theme,
    extend: {
      ...baseConfig.theme.extend,
      borderRadius: {
        lg: 'var(--radius)',
        md: 'calc(var(--radius) - 2px)',
        sm: 'calc(var(--radius) - 4px)',
      },
      keyframes: {
        'accordion-down': {
          from: { height: '0' },
          to: { height: 'var(--radix-accordion-content-height)' },
        },
        'accordion-up': {
          from: { height: 'var(--radix-accordion-content-height)' },
          to: { height: '0' },
        },
      },
      animation: {
        'accordion-down': 'accordion-down 0.2s ease-out',
        'accordion-up': 'accordion-up 0.2s ease-out',
      },
    },
  },
}
```

**3.1.4 src/lib/utils.ts**

```typescript
import { type ClassValue, clsx } from 'clsx'
import { twMerge } from 'tailwind-merge'

/**
 * 合併 Tailwind CSS 類名
 */
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

/**
 * 格式化金額
 */
export function formatCurrency(amount: number, currency = 'USD'): string {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency,
  }).format(amount)
}

/**
 * 格式化百分比
 */
export function formatPercent(value: number, decimals = 2): string {
  return `${(value * 100).toFixed(decimals)}%`
}

/**
 * 格式化日期
 */
export function formatDate(date: string | Date): string {
  return new Intl.DateTimeFormat('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  }).format(new Date(date))
}
```

---

### Task 3.2: 基礎 UI 組件（shadcn/ui 風格）

**3.2.1 Button 組件**

`src/components/ui/button.tsx`:

```typescript
import * as React from 'react'
import { Slot } from '@radix-ui/react-slot'
import { cva, type VariantProps } from 'class-variance-authority'
import { cn } from '@/lib/utils'

const buttonVariants = cva(
  'inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50',
  {
    variants: {
      variant: {
        default: 'bg-primary-600 text-white hover:bg-primary-700',
        destructive: 'bg-danger-500 text-white hover:bg-danger-600',
        outline: 'border border-gray-300 bg-white hover:bg-gray-50',
        ghost: 'hover:bg-gray-100',
        link: 'text-primary-600 underline-offset-4 hover:underline',
      },
      size: {
        default: 'h-10 px-4 py-2',
        sm: 'h-9 rounded-md px-3',
        lg: 'h-11 rounded-md px-8',
        icon: 'h-10 w-10',
      },
    },
    defaultVariants: {
      variant: 'default',
      size: 'default',
    },
  }
)

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  asChild?: boolean
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, asChild = false, ...props }, ref) => {
    const Comp = asChild ? Slot : 'button'
    return (
      <Comp
        className={cn(buttonVariants({ variant, size, className }))}
        ref={ref}
        {...props}
      />
    )
  }
)
Button.displayName = 'Button'

export { Button, buttonVariants }
```

**3.2.2 Card 組件**

`src/components/ui/card.tsx`:

```typescript
import * as React from 'react'
import { cn } from '@/lib/utils'

const Card = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn(
      'rounded-lg border border-gray-200 bg-white shadow-sm',
      className
    )}
    {...props}
  />
))
Card.displayName = 'Card'

const CardHeader = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn('flex flex-col space-y-1.5 p-6', className)}
    {...props}
  />
))
CardHeader.displayName = 'CardHeader'

const CardTitle = React.forwardRef<
  HTMLParagraphElement,
  React.HTMLAttributes<HTMLHeadingElement>
>(({ className, ...props }, ref) => (
  <h3
    ref={ref}
    className={cn('text-2xl font-semibold leading-none tracking-tight', className)}
    {...props}
  />
))
CardTitle.displayName = 'CardTitle'

const CardDescription = React.forwardRef<
  HTMLParagraphElement,
  React.HTMLAttributes<HTMLParagraphElement>
>(({ className, ...props }, ref) => (
  <p
    ref={ref}
    className={cn('text-sm text-gray-500', className)}
    {...props}
  />
))
CardDescription.displayName = 'CardDescription'

const CardContent = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div ref={ref} className={cn('p-6 pt-0', className)} {...props} />
))
CardContent.displayName = 'CardContent'

const CardFooter = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn('flex items-center p-6 pt-0', className)}
    {...props}
  />
))
CardFooter.displayName = 'CardFooter'

export { Card, CardHeader, CardFooter, CardTitle, CardDescription, CardContent }
```

**3.2.3 Input 組件**

`src/components/ui/input.tsx`:

```typescript
import * as React from 'react'
import { cn } from '@/lib/utils'

export interface InputProps
  extends React.InputHTMLAttributes<HTMLInputElement> {}

const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ className, type, ...props }, ref) => {
    return (
      <input
        type={type}
        className={cn(
          'flex h-10 w-full rounded-md border border-gray-300 bg-white px-3 py-2 text-sm',
          'placeholder:text-gray-400',
          'focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent',
          'disabled:cursor-not-allowed disabled:opacity-50',
          className
        )}
        ref={ref}
        {...props}
      />
    )
  }
)
Input.displayName = 'Input'

export { Input }
```

**3.2.4 Badge 組件**

`src/components/ui/badge.tsx`:

```typescript
import * as React from 'react'
import { cva, type VariantProps } from 'class-variance-authority'
import { cn } from '@/lib/utils'

const badgeVariants = cva(
  'inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-semibold transition-colors',
  {
    variants: {
      variant: {
        default: 'bg-primary-100 text-primary-700',
        success: 'bg-green-100 text-green-700',
        warning: 'bg-yellow-100 text-yellow-700',
        danger: 'bg-red-100 text-red-700',
        outline: 'border border-gray-300 text-gray-700',
      },
    },
    defaultVariants: {
      variant: 'default',
    },
  }
)

export interface BadgeProps
  extends React.HTMLAttributes<HTMLDivElement>,
    VariantProps<typeof badgeVariants> {}

function Badge({ className, variant, ...props }: BadgeProps) {
  return (
    <div className={cn(badgeVariants({ variant }), className)} {...props} />
  )
}

export { Badge, badgeVariants }
```

**3.2.5 Table 組件**

`src/components/ui/table.tsx`:

```typescript
import * as React from 'react'
import { cn } from '@/lib/utils'

const Table = React.forwardRef<
  HTMLTableElement,
  React.HTMLAttributes<HTMLTableElement>
>(({ className, ...props }, ref) => (
  <div className="relative w-full overflow-auto">
    <table
      ref={ref}
      className={cn('w-full caption-bottom text-sm', className)}
      {...props}
    />
  </div>
))
Table.displayName = 'Table'

const TableHeader = React.forwardRef<
  HTMLTableSectionElement,
  React.HTMLAttributes<HTMLTableSectionElement>
>(({ className, ...props }, ref) => (
  <thead ref={ref} className={cn('[&_tr]:border-b', className)} {...props} />
))
TableHeader.displayName = 'TableHeader'

const TableBody = React.forwardRef<
  HTMLTableSectionElement,
  React.HTMLAttributes<HTMLTableSectionElement>
>(({ className, ...props }, ref) => (
  <tbody
    ref={ref}
    className={cn('[&_tr:last-child]:border-0', className)}
    {...props}
  />
))
TableBody.displayName = 'TableBody'

const TableRow = React.forwardRef<
  HTMLTableRowElement,
  React.HTMLAttributes<HTMLTableRowElement>
>(({ className, ...props }, ref) => (
  <tr
    ref={ref}
    className={cn(
      'border-b transition-colors hover:bg-gray-50',
      className
    )}
    {...props}
  />
))
TableRow.displayName = 'TableRow'

const TableHead = React.forwardRef<
  HTMLTableCellElement,
  React.ThHTMLAttributes<HTMLTableCellElement>
>(({ className, ...props }, ref) => (
  <th
    ref={ref}
    className={cn(
      'h-12 px-4 text-left align-middle font-medium text-gray-500',
      className
    )}
    {...props}
  />
))
TableHead.displayName = 'TableHead'

const TableCell = React.forwardRef<
  HTMLTableCellElement,
  React.TdHTMLAttributes<HTMLTableCellElement>
>(({ className, ...props }, ref) => (
  <td
    ref={ref}
    className={cn('p-4 align-middle', className)}
    {...props}
  />
))
TableCell.displayName = 'TableCell'

export { Table, TableHeader, TableBody, TableHead, TableRow, TableCell }
```

**3.2.6 Dialog 組件**

`src/components/ui/dialog.tsx`:

```typescript
import * as React from 'react'
import * as DialogPrimitive from '@radix-ui/react-dialog'
import { X } from 'lucide-react'
import { cn } from '@/lib/utils'

const Dialog = DialogPrimitive.Root
const DialogTrigger = DialogPrimitive.Trigger
const DialogPortal = DialogPrimitive.Portal
const DialogClose = DialogPrimitive.Close

const DialogOverlay = React.forwardRef<
  React.ElementRef<typeof DialogPrimitive.Overlay>,
  React.ComponentPropsWithoutRef<typeof DialogPrimitive.Overlay>
>(({ className, ...props }, ref) => (
  <DialogPrimitive.Overlay
    ref={ref}
    className={cn(
      'fixed inset-0 z-50 bg-black/50 backdrop-blur-sm',
      'data-[state=open]:animate-in data-[state=closed]:animate-out',
      className
    )}
    {...props}
  />
))
DialogOverlay.displayName = DialogPrimitive.Overlay.displayName

const DialogContent = React.forwardRef<
  React.ElementRef<typeof DialogPrimitive.Content>,
  React.ComponentPropsWithoutRef<typeof DialogPrimitive.Content>
>(({ className, children, ...props }, ref) => (
  <DialogPortal>
    <DialogOverlay />
    <DialogPrimitive.Content
      ref={ref}
      className={cn(
        'fixed left-[50%] top-[50%] z-50 translate-x-[-50%] translate-y-[-50%]',
        'w-full max-w-lg rounded-lg bg-white p-6 shadow-lg',
        className
      )}
      {...props}
    >
      {children}
      <DialogPrimitive.Close className="absolute right-4 top-4 rounded-sm opacity-70 hover:opacity-100">
        <X className="h-4 w-4" />
        <span className="sr-only">Close</span>
      </DialogPrimitive.Close>
    </DialogPrimitive.Content>
  </DialogPortal>
))
DialogContent.displayName = DialogPrimitive.Content.displayName

const DialogHeader = ({
  className,
  ...props
}: React.HTMLAttributes<HTMLDivElement>) => (
  <div
    className={cn('flex flex-col space-y-1.5 text-center sm:text-left', className)}
    {...props}
  />
)
DialogHeader.displayName = 'DialogHeader'

const DialogTitle = React.forwardRef<
  React.ElementRef<typeof DialogPrimitive.Title>,
  React.ComponentPropsWithoutRef<typeof DialogPrimitive.Title>
>(({ className, ...props }, ref) => (
  <DialogPrimitive.Title
    ref={ref}
    className={cn('text-lg font-semibold leading-none tracking-tight', className)}
    {...props}
  />
))
DialogTitle.displayName = DialogPrimitive.Title.displayName

export {
  Dialog,
  DialogTrigger,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogClose,
}
```

---

### Task 3.3: 業務組件

**3.3.1 StatCard（統計卡片）**

`src/components/business/stat-card.tsx`:

```typescript
import * as React from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card'
import { cn, formatCurrency, formatPercent } from '@/lib/utils'
import { TrendingUp, TrendingDown } from 'lucide-react'

export interface StatCardProps {
  title: string
  value: number
  format?: 'currency' | 'percent' | 'number'
  change?: number // 變化百分比
  icon?: React.ReactNode
  className?: string
}

export function StatCard({
  title,
  value,
  format = 'number',
  change,
  icon,
  className,
}: StatCardProps) {
  const formatValue = () => {
    switch (format) {
      case 'currency':
        return formatCurrency(value)
      case 'percent':
        return formatPercent(value)
      default:
        return value.toLocaleString()
    }
  }

  const isPositive = change !== undefined && change >= 0

  return (
    <Card className={cn('', className)}>
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle className="text-sm font-medium text-gray-600">
          {title}
        </CardTitle>
        {icon && <div className="text-gray-400">{icon}</div>}
      </CardHeader>
      <CardContent>
        <div className="text-2xl font-bold">{formatValue()}</div>
        {change !== undefined && (
          <div
            className={cn(
              'flex items-center text-xs mt-1',
              isPositive ? 'text-green-600' : 'text-red-600'
            )}
          >
            {isPositive ? (
              <TrendingUp className="h-3 w-3 mr-1" />
            ) : (
              <TrendingDown className="h-3 w-3 mr-1" />
            )}
            <span>
              {isPositive ? '+' : ''}
              {formatPercent(Math.abs(change), 1)} from last period
            </span>
          </div>
        )}
      </CardContent>
    </Card>
  )
}
```

**3.3.2 StrategyCard（策略卡片）**

`src/components/business/strategy-card.tsx`:

```typescript
import * as React from 'react'
import type { Strategy } from '@trading-robots/types'
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card'
import { Badge } from '../ui/badge'
import { Button } from '../ui/button'
import { formatDate } from '@/lib/utils'

export interface StrategyCardProps {
  strategy: Strategy
  onEdit?: (id: string) => void
  onToggle?: (id: string, isActive: boolean) => void
}

export function StrategyCard({ strategy, onEdit, onToggle }: StrategyCardProps) {
  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between">
        <CardTitle className="text-lg">{strategy.strategyType}</CardTitle>
        <Badge variant={strategy.isActive ? 'success' : 'default'}>
          {strategy.isActive ? 'Active' : 'Inactive'}
        </Badge>
      </CardHeader>
      <CardContent>
        <div className="space-y-2 text-sm">
          <div className="flex justify-between">
            <span className="text-gray-600">Created:</span>
            <span>{formatDate(strategy.createdAt)}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-600">Updated:</span>
            <span>{formatDate(strategy.updatedAt)}</span>
          </div>
        </div>
        <div className="flex gap-2 mt-4">
          {onEdit && (
            <Button variant="outline" size="sm" onClick={() => onEdit(strategy.id)}>
              Edit
            </Button>
          )}
          {onToggle && (
            <Button
              variant={strategy.isActive ? 'destructive' : 'default'}
              size="sm"
              onClick={() => onToggle(strategy.id, !strategy.isActive)}
            >
              {strategy.isActive ? 'Disable' : 'Enable'}
            </Button>
          )}
        </div>
      </CardContent>
    </Card>
  )
}
```

**3.3.3 LoanHistoryTable（放貸歷史表格）**

`src/components/business/loan-history-table.tsx`:

```typescript
import * as React from 'react'
import type { Loan } from '@trading-robots/types'
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '../ui/table'
import { Badge } from '../ui/badge'
import { formatCurrency, formatPercent, formatDate } from '@/lib/utils'

export interface LoanHistoryTableProps {
  loans: Loan[]
}

export function LoanHistoryTable({ loans }: LoanHistoryTableProps) {
  const getStatusVariant = (status: Loan['status']) => {
    switch (status) {
      case 'active':
        return 'success'
      case 'completed':
        return 'default'
      case 'cancelled':
        return 'danger'
      default:
        return 'outline'
    }
  }

  return (
    <Table>
      <TableHeader>
        <TableRow>
          <TableHead>Amount</TableHead>
          <TableHead>Rate</TableHead>
          <TableHead>Period</TableHead>
          <TableHead>Earnings</TableHead>
          <TableHead>Status</TableHead>
          <TableHead>Date</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {loans.map((loan) => (
          <TableRow key={loan.id}>
            <TableCell className="font-medium">
              {formatCurrency(loan.amount)}
            </TableCell>
            <TableCell>{formatPercent(loan.rate)}</TableCell>
            <TableCell>
              {formatDate(loan.startDate)} - {formatDate(loan.endDate)}
            </TableCell>
            <TableCell className="text-green-600 font-medium">
              {formatCurrency(loan.earnings)}
            </TableCell>
            <TableCell>
              <Badge variant={getStatusVariant(loan.status)}>
                {loan.status}
              </Badge>
            </TableCell>
            <TableCell className="text-gray-500 text-sm">
              {formatDate(loan.createdAt)}
            </TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  )
}
```

**3.3.4 RateDisplay（利率顯示）**

`src/components/business/rate-display.tsx`:

```typescript
import * as React from 'react'
import { cn, formatPercent } from '@/lib/utils'

export interface RateDisplayProps {
  rate: number
  label?: string
  size?: 'sm' | 'md' | 'lg'
  showTrend?: boolean
  trend?: 'up' | 'down' | 'neutral'
  className?: string
}

export function RateDisplay({
  rate,
  label,
  size = 'md',
  showTrend = false,
  trend = 'neutral',
  className,
}: RateDisplayProps) {
  const sizeClasses = {
    sm: 'text-lg',
    md: 'text-2xl',
    lg: 'text-4xl',
  }

  const trendColors = {
    up: 'text-green-600',
    down: 'text-red-600',
    neutral: 'text-gray-900',
  }

  return (
    <div className={cn('flex flex-col', className)}>
      {label && (
        <span className="text-sm text-gray-600 mb-1">{label}</span>
      )}
      <span
        className={cn(
          'font-bold',
          sizeClasses[size],
          showTrend && trendColors[trend]
        )}
      >
        {formatPercent(rate)} APR
      </span>
    </div>
  )
}
```

---

### Task 3.4: 統一導出

**src/components/ui/index.ts**:

```typescript
export * from './button'
export * from './card'
export * from './input'
export * from './select'
export * from './textarea'
export * from './badge'
export * from './dialog'
export * from './table'
export * from './tabs'
export * from './alert'
```

**src/components/business/index.ts**:

```typescript
export * from './stat-card'
export * from './strategy-card'
export * from './loan-history-table'
export * from './rate-display'
```

**src/index.ts**:

```typescript
// UI Components
export * from './components/ui'

// Business Components
export * from './components/business'

// Hooks
export * from './hooks'

// Utils
export * from './lib/utils'
```

---

## ✅ 驗收標準

### 組件完整性

- [ ] 所有基礎 UI 組件實作完成
- [ ] 所有業務組件實作完成
- [ ] 組件有適當的 TypeScript 類型定義
- [ ] 組件支援自定義 className

### 設計一致性

- [ ] 使用共用的 Tailwind 主題
- [ ] 組件風格統一（shadcn/ui 風格）
- [ ] 顏色和間距符合設計系統

### 可用性

- [ ] 組件可以在其他 package 中引用
- [ ] TypeScript 類型檢查通過
- [ ] 無 Console 錯誤或警告

### 文檔

- [ ] README 包含使用範例
- [ ] 每個組件有 props 說明

---

## 📚 使用範例（README.md）

```typescript
// 在 Backstage 或 Website 中使用

// 1. 基礎組件
import { Button, Card, Input } from '@trading-robots/ui'

<Button variant="default" size="lg">
  Click me
</Button>

// 2. 業務組件
import { StatCard, StrategyCard } from '@trading-robots/ui'

<StatCard
  title="Total Earnings"
  value={1234.56}
  format="currency"
  change={0.15}
/>

// 3. 工具函數
import { formatCurrency, cn } from '@trading-robots/ui'

const formatted = formatCurrency(1234.56) // $1,234.56
```

---

## 🔗 後續整合

完成此計劃後，可以進行：

- **Plan 4: Backstage**（使用這些組件）
- **Plan 5: Website**（使用這些組件）

---

## ⏱️ 預計時間

- Task 3.1: 1 小時（初始化）
- Task 3.2: 4 小時（基礎組件）
- Task 3.3: 3 小時（業務組件）
- Task 3.4: 1 小時（導出和文檔）

**總計：約 9 小時（1.5-2 個工作日）**

### To-dos

- [ ] 初始化 UI 專案（package.json, tsconfig, tailwind）
- [ ] 建立工具函數（cn, formatCurrency, formatPercent）
- [ ] 實作 Button 和 Card 組件
- [ ] 實作表單組件（Input, Select, Textarea）
- [ ] 實作回饋組件（Badge, Dialog, Alert）
- [ ] 實作 Table 和 Tabs 組件
- [ ] 實作 StatCard 業務組件
- [ ] 實作 StrategyCard 業務組件
- [ ] 實作 LoanHistoryTable 業務組件
- [ ] 實作 RateDisplay 業務組件
- [ ] 設置統一導出和文檔