# Bitfinex 放貸機器人專案規劃書

## 📋 文檔導航

本專案規劃書採用模組化結構，各部分文檔如下：

### 1. [專案概述](./01-project-overview/)
- [專案簡介](./01-project-overview/overview.md) - 專案背景與目標
- [專案目標](./01-project-overview/goals.md) - 核心目標與成功指標
- [系統架構](./01-project-overview/architecture.md) - 整體架構設計

### 2. [技術棧](./02-tech-stack/)
- [前端技術](./02-tech-stack/frontend.md) - React + TypeScript 生態系
- [後端技術](./02-tech-stack/backend.md) - FastAPI + Python 生態系
- [基礎設施](./02-tech-stack/infrastructure.md) - 資料庫、部署等

### 3. [開發階段](./03-development-phases/)
- [時程總覽](./03-development-phases/timeline.md) - 完整開發時程
- [階段 0：前期準備](./03-development-phases/phase-0-preparation.md)
- [階段 1：核心 MVP](./03-development-phases/phase-1-core-mvp.md)
- [階段 2：完整儀表板](./03-development-phases/phase-2-dashboard.md)
- [階段 3：通知系統](./03-development-phases/phase-3-notification.md)
- [階段 4：多用戶系統](./03-development-phases/phase-4-multi-user.md)
- [階段 5：進階功能](./03-development-phases/phase-5-advanced.md)
- [階段 6：部署上線](./03-development-phases/phase-6-deployment.md)

### 4. [前端規劃](./04-frontend/)
- [專案結構](./04-frontend/structure.md) - 檔案與資料夾組織
- [組件設計](./04-frontend/components.md) - 可重用組件列表
- [頁面規劃](./04-frontend/pages.md) - 完整頁面清單
- [樣式系統](./04-frontend/styling.md) - 設計系統與主題

### 5. [後端規劃](./05-backend/)
- [專案結構](./05-backend/structure.md) - 檔案與資料夾組織
- [API 設計](./05-backend/api-design.md) - RESTful API 端點
- [機器人邏輯](./05-backend/bot-logic.md) - 交易策略實現
- [服務層](./05-backend/services.md) - 業務邏輯服務

### 6. [資料庫設計](./06-database/)
- [資料表結構](./06-database/schema.md) - 完整資料表設計
- [資料遷移](./06-database/migrations.md) - 遷移策略

### 7. [部署規劃](./07-deployment/)
- [Docker 化](./07-deployment/docker.md) - 容器化配置
- [伺服器設置](./07-deployment/server-setup.md) - 生產環境配置
- [CI/CD](./07-deployment/ci-cd.md) - 自動化部署流程

### 8. [測試策略](./08-testing/)
- [測試計劃](./08-testing/testing-strategy.md) - 測試方法與覆蓋率

### 9. [維護與監控](./09-maintenance/)
- [監控系統](./09-maintenance/monitoring.md) - 系統監控方案
- [備份策略](./09-maintenance/backup.md) - 數據備份計劃

---

## 🚀 快速開始

### 給專案管理者
1. 先閱讀 [專案概述](./01-project-overview/) 了解整體方向
2. 查看 [開發階段時程](./03-development-phases/timeline.md) 規劃資源
3. 根據團隊配置調整各階段時程

### 給開發者
1. 前端開發者：從 [前端規劃](./04-frontend/) 開始
2. 後端開發者：從 [後端規劃](./05-backend/) 開始
3. 全端開發者：建議依序閱讀各章節

### 給技術主管
1. 審查 [系統架構](./01-project-overview/architecture.md)
2. 確認 [技術棧選擇](./02-tech-stack/)
3. 評估 [部署方案](./07-deployment/)

---

## 📊 專案概況

- **專案類型**：加密貨幣放貸自動化機器人
- **目標平台**：Bitfinex
- **預計時程**：6-7 週（前後端並行開發）
- **初始用戶**：5 人
- **技術架構**：前後端分離（React + FastAPI）

---

## 📝 文檔維護

- **維護者**：開發團隊
- **更新頻率**：每個階段完成後更新
- **版本控制**：隨代碼一起版本管理

---

## 🔗 相關資源

- [Bitfinex API 文檔](https://docs.bitfinex.com/docs)
- [FastAPI 官方文檔](https://fastapi.tiangolo.com/)
- [React 官方文檔](https://react.dev/)
- [shadcn/ui 組件庫](https://ui.shadcn.com/)

---

最後更新：2025-11-04

