# Docker Setup Guide

本指南將幫助你使用 Docker Compose 設置 PostgreSQL 數據庫。

## 前置要求

- Docker Desktop (Windows/Mac) 或 Docker Engine (Linux)
- Docker Compose (通常包含在 Docker Desktop 中)

## 快速開始

### 1. 創建環境變數文件

複製 `.env.example` 到 `.env` 並根據需要修改配置：

```bash
cp .env.example .env
```

**重要**: 在生產環境中，請務必修改以下配置：
- `POSTGRES_PASSWORD`: 使用強密碼
- `SECRET_KEY`: 使用隨機生成的密鑰
- `ENCRYPTION_KEY`: 使用 32 字節的 base64 編碼密鑰

### 2. 啟動 PostgreSQL

```bash
# 啟動數據庫
docker-compose up -d postgres

# 查看日誌
docker-compose logs -f postgres

# 檢查狀態
docker-compose ps
```

### 3. (可選) 啟動 pgAdmin

如果你想使用圖形化界面管理數據庫：

```bash
docker-compose --profile tools up -d pgadmin
```

然後訪問 http://localhost:5050，使用 `.env` 中配置的郵箱和密碼登入。

#### 在 pgAdmin 中連接數據庫

1. 登入 pgAdmin
2. 點擊 "Add New Server"
3. 在 "General" 標籤中輸入名稱（例如：Trading Robots）
4. 在 "Connection" 標籤中輸入：
   - Host: `postgres` (容器名稱)
   - Port: `5432`
   - Maintenance database: `bitfinex_lending`
   - Username: 你在 `.env` 中設置的 `POSTGRES_USER`
   - Password: 你在 `.env` 中設置的 `POSTGRES_PASSWORD`

## 常用命令

```bash
# 啟動所有服務
docker-compose up -d

# 啟動特定服務
docker-compose up -d postgres

# 停止所有服務
docker-compose down

# 停止並刪除數據卷（⚠️ 會刪除所有數據）
docker-compose down -v

# 查看運行中的容器
docker-compose ps

# 查看日誌
docker-compose logs -f postgres

# 進入 PostgreSQL 容器
docker-compose exec postgres psql -U user -d bitfinex_lending

# 重啟服務
docker-compose restart postgres

# 查看資源使用情況
docker-compose stats
```

## 數據庫連接

### 從本機連接

使用以下連接字符串：

```
postgresql://user:password@localhost:5432/bitfinex_lending
```

### 從 Docker 容器內連接

如果你的後端也在 Docker 容器中運行，使用：

```
postgresql://user:password@postgres:5432/bitfinex_lending
```

## 備份和恢復

### 備份數據庫

```bash
# 創建備份
docker-compose exec postgres pg_dump -U user bitfinex_lending > backup_$(date +%Y%m%d_%H%M%S).sql

# 或使用自定義格式（推薦）
docker-compose exec postgres pg_dump -U user -Fc bitfinex_lending > backup_$(date +%Y%m%d_%H%M%S).dump
```

### 恢復數據庫

```bash
# 從 SQL 文件恢復
docker-compose exec -T postgres psql -U user bitfinex_lending < backup.sql

# 從自定義格式恢復
docker-compose exec -T postgres pg_restore -U user -d bitfinex_lending backup.dump
```

## 數據持久化

數據存儲在 Docker volume 中：
- `postgres_data`: PostgreSQL 數據
- `pgadmin_data`: pgAdmin 配置和設置

這些 volumes 在容器重啟後會保留。要完全刪除數據，使用 `docker-compose down -v`。

## 故障排除

### 端口已被佔用

如果 5432 端口已被佔用，修改 `.env` 中的 `POSTGRES_PORT`：

```bash
POSTGRES_PORT=5433
```

並更新 `DATABASE_URL`：

```bash
DATABASE_URL=postgresql://user:password@localhost:5433/bitfinex_lending
```

### 容器無法啟動

檢查日誌：

```bash
docker-compose logs postgres
```

### 重置數據庫

```bash
# 停止並刪除所有數據
docker-compose down -v

# 重新啟動
docker-compose up -d postgres
```

## 生產環境建議

1. **安全性**：
   - 使用強密碼
   - 限制端口暴露（考慮不暴露到主機）
   - 定期更新 Docker 鏡像

2. **性能**：
   - 根據需求調整 PostgreSQL 配置
   - 考慮使用 SSD 存儲
   - 監控資源使用情況

3. **備份**：
   - 設置自動備份計劃
   - 測試恢復流程
   - 將備份存儲在多個位置

4. **監控**：
   - 設置健康檢查
   - 監控日誌
   - 使用 APM 工具

## 相關文檔

- [PostgreSQL Official Documentation](https://www.postgresql.org/docs/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [pgAdmin Documentation](https://www.pgadmin.org/docs/)


