# UI Components Demo

## 🚀 快速啟動

### 方法 1：使用根目錄命令
```bash
cd TradingRobots
pnpm --filter @trading-robots/ui dev
```

### 方法 2：直接在 ui 目錄
```bash
cd packages/ui
pnpm dev
```

### 方法 3：使用 Windows 批次檔
```bash
cd packages/ui
start-demo.bat
```

## 📱 訪問地址

開發服務器會自動在以下地址啟動：

```
http://localhost:5173
```

瀏覽器應該會自動打開。如果沒有，請手動訪問上述地址。

## 🎨 展示內容

頁面包含所有 10 個 UI 組件的完整展示：

### 基礎 UI 組件（6 個）
1. **Button** - 所有變體（default, destructive, outline, ghost, link）和尺寸
2. **Badge** - 所有狀態顏色（default, success, warning, danger, outline）
3. **Input** - 不同類型的輸入框
4. **Card** - 卡片組件示例
5. **Dialog** - 對話框（點擊按鈕測試）
6. **Table** - 在 LoanHistoryTable 中展示

### 業務組件（4 個）
7. **StatCard** - 統計卡片（帶趨勢指示器）
8. **RateDisplay** - 利率顯示（三種尺寸）
9. **StrategyCard** - 策略卡片（可點擊編輯/切換）
10. **LoanHistoryTable** - 放貸歷史表格

## 🐛 常見問題

### 問題：端口被佔用
如果 5173 端口被佔用，Vite 會自動使用下一個可用端口（5174, 5175 等）。
請查看終端輸出的實際端口號。

### 問題：看不到樣式
確保所有依賴都已安裝：
```bash
cd packages/ui
pnpm install
```

### 問題：TypeScript 錯誤
運行類型檢查：
```bash
pnpm typecheck
```

## 📝 技術細節

- **Framework**: React 19 + TypeScript
- **Build Tool**: Vite 5
- **Styling**: Tailwind CSS
- **UI Library**: Radix UI
- **Icons**: Lucide React

所有組件使用 `@trading-robots/types` 的類型定義，確保與整個系統的類型一致性。

