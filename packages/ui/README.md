# @trading-robots/ui

共用 UI 組件庫，為 Backstage 和 Website 提供一致的設計系統。

## 📦 安裝

```bash
pnpm add @trading-robots/ui
```

## 🎨 設計系統

基於 [shadcn/ui](https://ui.shadcn.com/) 設計系統，使用 Tailwind CSS 和 Radix UI。

### 顏色主題

使用 `@trading-robots/config` 的共用主題配置：

- **Primary**: 主色調（藍色）
- **Success**: 成功狀態（綠色）
- **Warning**: 警告狀態（黃色）
- **Danger**: 危險狀態（紅色）

## 🧩 組件

### 基礎 UI 組件

#### Button

```typescript
import { Button } from '@trading-robots/ui'

<Button variant="default" size="lg">
  Click me
</Button>

// Variants: default, destructive, outline, ghost, link
// Sizes: default, sm, lg, icon
```

#### Card

```typescript
import { Card, CardHeader, CardTitle, CardContent } from '@trading-robots/ui'

<Card>
  <CardHeader>
    <CardTitle>Title</CardTitle>
  </CardHeader>
  <CardContent>
    Content here
  </CardContent>
</Card>
```

#### Input

```typescript
import { Input } from '@trading-robots/ui'

<Input type="email" placeholder="Email" />
```

#### Badge

```typescript
import { Badge } from '@trading-robots/ui'

<Badge variant="success">Active</Badge>

// Variants: default, success, warning, danger, outline
```

#### Dialog

```typescript
import { Dialog, DialogTrigger, DialogContent, DialogHeader, DialogTitle } from '@trading-robots/ui'

<Dialog>
  <DialogTrigger>Open</DialogTrigger>
  <DialogContent>
    <DialogHeader>
      <DialogTitle>Dialog Title</DialogTitle>
    </DialogHeader>
    <p>Dialog content</p>
  </DialogContent>
</Dialog>
```

#### Table

```typescript
import { Table, TableHeader, TableBody, TableHead, TableRow, TableCell } from '@trading-robots/ui'

<Table>
  <TableHeader>
    <TableRow>
      <TableHead>Name</TableHead>
      <TableHead>Value</TableHead>
    </TableRow>
  </TableHeader>
  <TableBody>
    <TableRow>
      <TableCell>Item</TableCell>
      <TableCell>$100</TableCell>
    </TableRow>
  </TableBody>
</Table>
```

### 業務組件

#### StatCard（統計卡片）

顯示統計數據，支援變化趨勢。

```typescript
import { StatCard } from '@trading-robots/ui'
import { DollarSign } from 'lucide-react'

<StatCard
  title="Total Earnings"
  value={1234.56}
  format="currency"
  change={0.15}
  icon={<DollarSign className="h-4 w-4" />}
/>

// Props:
// - title: string
// - value: number
// - format?: 'currency' | 'percent' | 'number'
// - change?: number (變化百分比)
// - icon?: React.ReactNode
```

#### StrategyCard（策略卡片）

顯示策略信息，支援編輯和啟用/禁用操作。

```typescript
import { StrategyCard } from '@trading-robots/ui'
import type { Strategy } from '@trading-robots/types'

<StrategyCard
  strategy={strategy}
  onEdit={(id) => console.log('Edit', id)}
  onToggle={(id, isActive) => console.log('Toggle', id, isActive)}
/>

// Props:
// - strategy: Strategy
// - onEdit?: (id: string) => void
// - onToggle?: (id: string, isActive: boolean) => void
```

#### LoanHistoryTable（放貸歷史表格）

顯示放貸歷史記錄。

```typescript
import { LoanHistoryTable } from '@trading-robots/ui'
import type { Loan } from '@trading-robots/types'

<LoanHistoryTable loans={loans} />

// Props:
// - loans: Loan[]
```

#### RateDisplay（利率顯示）

顯示利率，支援不同大小和趨勢顏色。

```typescript
import { RateDisplay } from '@trading-robots/ui'

<RateDisplay
  rate={0.0365}
  label="Current Rate"
  size="lg"
  showTrend={true}
  trend="up"
/>

// Props:
// - rate: number
// - label?: string
// - size?: 'sm' | 'md' | 'lg'
// - showTrend?: boolean
// - trend?: 'up' | 'down' | 'neutral'
```

## 🛠️ 工具函數

```typescript
import { cn, formatCurrency, formatPercent, formatDate } from '@trading-robots/ui'

// 合併 Tailwind CSS 類名
const className = cn('text-base', 'font-bold', { 'text-red-500': isError })

// 格式化金額
formatCurrency(1234.56) // "$1,234.56"

// 格式化百分比
formatPercent(0.0365) // "3.65%"
formatPercent(0.0365, 3) // "3.650%"

// 格式化日期
formatDate('2024-01-01') // "Jan 1, 2024"
```

## 🎨 自定義樣式

所有組件都支援 `className` prop，可以覆蓋或擴展樣式：

```typescript
<Button className="w-full">
  Full Width Button
</Button>

<Card className="border-2 border-primary-500">
  Custom Border
</Card>
```

## 📚 類型定義

所有組件都有完整的 TypeScript 類型定義。業務組件使用 `@trading-robots/types` 的類型：

```typescript
import type { Strategy, Loan } from '@trading-robots/types'
import { StrategyCard, LoanHistoryTable } from '@trading-robots/ui'
```

## 🔗 依賴

- `@trading-robots/types` - 共用類型定義
- `@trading-robots/config` - 共用配置（Tailwind 主題）
- `react` ^18.2.0
- `react-dom` ^18.2.0

## 📖 設計原則

1. **一致性**：所有組件使用統一的設計語言
2. **可組合**：組件可以自由組合使用
3. **類型安全**：完整的 TypeScript 支援
4. **可擴展**：支援自定義樣式和行為
5. **無障礙**：基於 Radix UI，符合 ARIA 標準

## 🚀 在應用中使用

### Backstage 或 Website

```typescript
// 在 package.json 添加依賴
{
  "dependencies": {
    "@trading-robots/ui": "workspace:*"
  }
}

// 在組件中使用
import { Button, StatCard, StrategyCard } from '@trading-robots/ui'
import type { Strategy } from '@trading-robots/types'

export function Dashboard() {
  return (
    <div className="space-y-4">
      <StatCard
        title="Total Earnings"
        value={totalEarnings}
        format="currency"
      />
      <StrategyCard strategy={strategy} />
    </div>
  )
}
```

## 📝 開發

```bash
# 類型檢查
pnpm typecheck

# 構建
pnpm build
```

## 🎯 完成狀態

- ✅ 基礎 UI 組件（Button, Card, Input, Badge, Dialog, Table）
- ✅ 業務組件（StatCard, StrategyCard, LoanHistoryTable, RateDisplay）
- ✅ 工具函數（cn, formatCurrency, formatPercent, formatDate）
- ✅ TypeScript 類型定義
- ✅ Tailwind CSS 配置
- ✅ README 文檔

## 📄 License

Private


