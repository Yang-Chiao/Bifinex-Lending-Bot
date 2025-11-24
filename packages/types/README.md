# @trading-robots/types

共用類型定義包，提供整個專案的 TypeScript 類型定義。

## 使用方式

```typescript
import { User, Strategy, ApiResponse } from '@trading-robots/types'
```

## 類型結構

### Common（通用類型）
- `ApiResponse<T>` - API 統一響應格式
- `PaginatedResponse<T>` - 分頁響應
- `ErrorCode` - 錯誤代碼枚舉

### Entities（實體類型）
- `User` - 用戶實體
- `Strategy` - 策略實體
- `Offer` - 掛單實體
- `Loan` - 成交記錄實體

### API（API 請求/響應類型）
- `auth.ts` - 認證相關
- `user.ts` - 用戶相關
- `strategy.ts` - 策略相關
- `offer.ts` - 掛單相關
- `loan.ts` - 成交記錄相關

### Bitfinex（Bitfinex API 類型）
- `auth.ts` - 認證相關（API Key、錯誤格式）
- `market.ts` - 市場數據（Ticker、Funding Book）
- `funding.ts` - 放貸操作（提交/取消 Offer、Credits、Loans）
- `wallet.ts` - 錢包相關（餘額查詢、轉帳）

> **重要**：Bitfinex API v2 使用陣列格式回應。詳見 [BITFINEX_API_UPDATES.md](./BITFINEX_API_UPDATES.md)

## 開發

執行類型檢查：

```bash
pnpm typecheck
```

