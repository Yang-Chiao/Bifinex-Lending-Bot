<!-- 76a17ffa-be37-4472-b601-1954698ec85b 27e2c355-fb43-4143-be3c-c8dc97e91f03 -->
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
│   │   │

### To-dos

- [ ] 初始化 Backend 專案（requirements, .env.example, main.py）
- [ ] 實作核心模組（config, database, security）
- [ ] 建立 Base 模型和 User 模型（完整）
- [ ] 實作 Auth Schemas（完整範例）
- [ ] 實作 Auth Services 和 API deps（完整範例）
- [ ] 實作 Auth API 路由（完整範例）
- [ ] 建立測試配置和 Auth 測試範例
- [ ] 建立其他模組骨架（Strategy, Offer, Loan）含詳細註解
- [ ] 撰寫 SETUP.md 和 ARCHITECTURE.md
- [ ] 撰寫 API_DESIGN.md 和 DATABASE.md
- [ ] 撰寫 DEVELOPMENT.md（新手指南）和 CODE_REVIEW.md
- [ ] 建立輔助腳本（init_db, create_admin）
- [ ] 撰寫 Backend README 和整合文檔