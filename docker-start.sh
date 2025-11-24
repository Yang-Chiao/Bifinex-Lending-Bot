#!/bin/bash

# Docker Compose 快速啟動腳本

set -e

echo "🐳 Trading Robots - Docker Setup"
echo "================================"
echo ""

# 檢查 Docker 是否安裝
if ! command -v docker &> /dev/null; then
    echo "❌ Docker 未安裝，請先安裝 Docker"
    exit 1
fi

# 檢查 Docker Compose 是否安裝
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose 未安裝，請先安裝 Docker Compose"
    exit 1
fi

# 檢查 .env 文件是否存在
if [ ! -f .env ]; then
    echo "⚠️  .env 文件不存在"
    echo "📝 正在從 env.template 創建 .env 文件..."
    cp env.template .env
    echo "✅ .env 文件已創建"
    echo ""
    echo "⚠️  請編輯 .env 文件並設置您的配置（特別是密碼）"
    echo "   然後重新運行此腳本"
    exit 0
fi

echo "✅ .env 文件存在"
echo ""

# 啟動 PostgreSQL
echo "🚀 正在啟動 PostgreSQL..."
docker-compose up -d postgres

echo ""
echo "⏳ 等待 PostgreSQL 就緒..."
sleep 5

# 檢查 PostgreSQL 健康狀態
if docker-compose ps | grep -q "postgres.*healthy"; then
    echo "✅ PostgreSQL 已成功啟動並運行"
else
    echo "⚠️  PostgreSQL 正在啟動中，請稍候..."
    echo "   您可以使用以下命令檢查狀態："
    echo "   docker-compose ps"
    echo "   docker-compose logs -f postgres"
fi

echo ""
echo "📊 容器狀態："
docker-compose ps

echo ""
echo "================================"
echo "✨ 設置完成！"
echo ""
echo "📌 數據庫連接信息："
echo "   主機: localhost"
echo "   端口: $(grep POSTGRES_PORT .env | cut -d '=' -f2 || echo 5432)"
echo "   數據庫: $(grep POSTGRES_DB .env | cut -d '=' -f2 || echo bitfinex_lending)"
echo "   用戶: $(grep POSTGRES_USER .env | cut -d '=' -f2 || echo user)"
echo ""
echo "🛠️  常用命令："
echo "   查看日誌: docker-compose logs -f postgres"
echo "   停止數據庫: docker-compose down"
echo "   重啟數據庫: docker-compose restart postgres"
echo "   連接數據庫: docker-compose exec postgres psql -U user -d bitfinex_lending"
echo ""
echo "📚 詳細文檔: DOCKER_SETUP.md"
echo ""

# 詢問是否啟動 pgAdmin
read -p "❓ 是否要啟動 pgAdmin？(y/N) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🚀 正在啟動 pgAdmin..."
    docker-compose --profile tools up -d pgadmin
    echo "✅ pgAdmin 已啟動"
    echo "🌐 訪問 http://localhost:$(grep PGADMIN_PORT .env | cut -d '=' -f2 || echo 5050)"
    echo "📧 郵箱: $(grep PGADMIN_EMAIL .env | cut -d '=' -f2 || echo admin@admin.com)"
fi

echo ""
echo "🎉 完成！"


