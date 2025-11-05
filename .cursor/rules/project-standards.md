---
description: Trading Robots 專案開發規範
globs: ['**/*.ts', '**/*.tsx', '**/*.py']
alwaysApply: true
---

# Trading Robots 開發規範

## 🏗️ 專案架構

Monorepo 結構：
- `apps/backend` - FastAPI 後端
- `apps/backstage` - React 用戶後台
- `apps/website` - Next.js 官網
- `packages/ui` - shadcn/ui 組件庫
- `packages/types` - TypeScript 類型
- `packages/config` - 共用配置

**依賴規則**：
- apps 可依賴 packages
- packages 間可互相依賴（避免循環）
- 使用 `workspace:*` 引用內部包

## 💻 編碼風格

### TypeScript/React
- 嚴格模式，避免 `any`
- 命名：camelCase 變數/函數，PascalCase 組件/類型
- 使用 `@trading-robots/ui` 的組件和 `cn()` 工具
- 狀態管理：Zustand（全局）+ React Query（服務端）
- 使用中文註釋，英文命名

### Python/FastAPI
- 遵循 PEP 8，使用 Black 格式化
- 命名：snake_case 函數/變數，PascalCase 類別
- 必須使用類型提示
- 使用中文註釋

## 🎨 UI 規範

- 使用 Tailwind CSS + shadcn/ui 設計系統
- 顏色：`primary-600`, `green-600`, `red-600`, `gray-50`
- 響應式：優先移動端，使用 `sm:`, `md:`, `lg:` 前綴

## 🔌 API 設計

- RESTful：`GET /api/strategies`, `POST /api/strategies`, `PATCH /api/strategies/:id`
- 統一響應格式：`{ data: {...}, meta: {...} }`
- 統一錯誤格式：`{ detail: "...", code: "...", status: 404 }`
- 認證：Bearer Token

## 🗄️ 資料庫

- 表名：snake_case 複數（`strategies`, `loan_history`）
- 欄位名：snake_case（`user_id`, `created_at`）
- 必須加索引於外鍵和查詢欄位

## 📝 文檔與註釋

- 使用中文註釋，英文命名
- 函數/組件必須有 JSDoc/docstring
- 複雜邏輯必須加註解

## 🚀 Git 規範

分支：`main`, `develop`, `feature/{name}`, `bugfix/{name}`

Commit 格式（中文）：
```
feat: 新功能簡述
fix: 錯誤修復
docs: 文檔更新
refactor: 重構
test: 測試
```

## ⚠️ 重要原則

- TypeScript 嚴格模式，不使用 `any`
- 所有 API 請求必須錯誤處理
- 敏感資料使用環境變數，不可硬編碼
- 保持函數簡短（< 50 行）
- 提取重複邏輯到工具函數或 Hooks
- 優先使用共用組件庫，避免重複造輪子

