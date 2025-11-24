# 快速開始指南

## 🚀 3 分鐘了解專案

### 這是什麼？
**Bitfinex 放貸機器人** - 一個自動化管理 Bitfinex 融資借貸的系統，讓你的閒置資金 24/7 自動賺取利息。

### 核心功能
- ✅ 自動掛單放貸
- ✅ 多種策略（市場跟隨、階梯式）
- ✅ 精美的 Web 管理後台
- ✅ Telegram 即時通知
- ✅ 支援多用戶

### 技術棧
```
前端：React + TypeScript + shadcn/ui
後端：FastAPI + PostgreSQL
機器人：Python + APScheduler
```

### 開發時程
```
6-7 週完成 MVP（前後端並行開發）
```

---

## 📚 文檔導覽

### 想了解專案？→ 從這裡開始
1. [專案簡介](./01-project-overview/overview.md) - 背景、定位、價值
2. [專案目標](./01-project-overview/goals.md) - 功能需求與優先級
3. [系統架構](./01-project-overview/architecture.md) - 整體設計

### 要開始開發？→ 看這些
**前端開發者**：
1. [前端技術棧](./02-tech-stack/frontend.md)
2. [前端專案結構](./04-frontend/structure.md)
3. [API 設計](./05-backend/api-design.md) - 了解後端介面
4. [開發時程](./03-development-phases/timeline.md)

**後端開發者**：
1. [後端技術棧](./02-tech-stack/backend.md)
2. [API 設計](./05-backend/api-design.md)
3. [資料庫結構](./06-database/schema.md)
4. [開發時程](./03-development-phases/timeline.md)

**全端開發者**：
- 依序閱讀上述所有文檔 😊

### 準備部署？→ 這些有幫助
1. [Docker 化](./07-deployment/docker.md) ⚠️ 待創建
2. [伺服器設置](./07-deployment/server-setup.md) ⚠️ 待創建

---

## 🎯 30 秒決策樹

```
想了解專案是什麼？
  └→ 讀 01-project-overview/

確定要做了，想看技術細節？
  └→ 讀 02-tech-stack/

準備開始寫 code？
  └→ 前端看 04-frontend/
     後端看 05-backend/ + 06-database/

要排時程和資源？
  └→ 讀 03-development-phases/timeline.md

要上線部署？
  └→ 讀 07-deployment/ (待創建)
```

---

## 💡 常見問題

### Q1: 我是前端，需要看後端文檔嗎？
**A**: 需要看 `05-backend/api-design.md`，了解 API 介面和數據格式。其他後端細節可以跳過。

### Q2: 我是後端，需要看前端文檔嗎？
**A**: 不強制，但建議瀏覽 `04-frontend/structure.md` 了解前端如何調用 API。

### Q3: 文檔太多了，最小集是什麼？
**A**: 如果只看 3 份文檔：
1. `01-project-overview/goals.md` - 知道要做什麼
2. `03-development-phases/timeline.md` - 知道怎麼排時程
3. `05-backend/api-design.md` - 知道前後端怎麼溝通

### Q4: 我想貢獻文檔，從哪開始？
**A**: 查看 `PROGRESS.md` 看哪些文檔還沒創建，然後參考已有文檔的格式。

### Q5: 文檔會更新嗎？
**A**: 會！每個階段完成後都會更新對應的文檔。

---

## 🎬 第一天應該做什麼？

### 如果你是前端開發者
```bash
# 1. Clone 專案（假設）
git clone <repo>

# 2. 安裝依賴
cd frontend
npm install

# 3. 閱讀文檔
讀 docs/04-frontend/structure.md
讀 docs/05-backend/api-design.md

# 4. 開始開發
npm run dev
```

### 如果你是後端開發者
```bash
# 1. Clone 專案
git clone <repo>

# 2. 設置環境
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 3. 閱讀文檔
讀 docs/05-backend/api-design.md
讀 docs/06-database/schema.md

# 4. 設置資料庫
創建 PostgreSQL 資料庫
alembic upgrade head

# 5. 啟動開發服務器
uvicorn app.main:app --reload
```

### 如果你是專案經理
```
1. 讀 docs/01-project-overview/
2. 讀 docs/03-development-phases/timeline.md
3. 召集團隊 Kickoff Meeting
4. 確認資源與時程
```

---

## 📊 文檔完成度

```
核心文檔：█████████░ 90%
開發階段：███░░░░░░░ 30%
前端規劃：███░░░░░░░ 30%
後端規劃：███░░░░░░░ 30%
部署文檔：░░░░░░░░░░  0%

總體：████░░░░░░ 40%
```

**已經可以開始開發了！** 🎉

---

## 🔗 外部資源

- [Bitfinex API 文檔](https://docs.bitfinex.com/docs)
- [FastAPI 官方文檔](https://fastapi.tiangolo.com/)
- [React 官方文檔](https://react.dev/)
- [shadcn/ui 組件庫](https://ui.shadcn.com/)

---

## 📞 需要幫助？

- **技術問題**：查看對應的技術棧文檔
- **專案理解**：查看專案概述文檔
- **開發規劃**：查看開發階段文檔
- **文檔缺失**：查看 PROGRESS.md 了解進度

---

**開始你的開發之旅吧！** 🚀✨

