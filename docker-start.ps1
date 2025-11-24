# Docker Compose 快速啟動腳本 (PowerShell)

Write-Host "🐳 Trading Robots - Docker Setup" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# 檢查 Docker 是否安裝
if (!(Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Docker 未安裝，請先安裝 Docker Desktop" -ForegroundColor Red
    exit 1
}

# 檢查 Docker Compose 是否可用
if (!(Get-Command docker-compose -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Docker Compose 未安裝，請確保使用最新版本的 Docker Desktop" -ForegroundColor Red
    exit 1
}

# 檢查 .env 文件是否存在
if (!(Test-Path .env)) {
    Write-Host "⚠️  .env 文件不存在" -ForegroundColor Yellow
    Write-Host "📝 正在從 env.template 創建 .env 文件..." -ForegroundColor Yellow
    Copy-Item env.template .env
    Write-Host "✅ .env 文件已創建" -ForegroundColor Green
    Write-Host ""
    Write-Host "⚠️  請編輯 .env 文件並設置您的配置（特別是密碼）" -ForegroundColor Yellow
    Write-Host "   然後重新運行此腳本" -ForegroundColor Yellow
    exit 0
}

Write-Host "✅ .env 文件存在" -ForegroundColor Green
Write-Host ""

# 啟動 PostgreSQL
Write-Host "🚀 正在啟動 PostgreSQL..." -ForegroundColor Cyan
docker-compose up -d postgres

Write-Host ""
Write-Host "⏳ 等待 PostgreSQL 就緒..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# 檢查 PostgreSQL 狀態
$status = docker-compose ps --format json | ConvertFrom-Json
$postgresStatus = $status | Where-Object { $_.Name -like "*postgres*" }

if ($postgresStatus -and $postgresStatus.State -eq "running") {
    Write-Host "✅ PostgreSQL 已成功啟動並運行" -ForegroundColor Green
} else {
    Write-Host "⚠️  PostgreSQL 正在啟動中，請稍候..." -ForegroundColor Yellow
    Write-Host "   您可以使用以下命令檢查狀態：" -ForegroundColor Yellow
    Write-Host "   docker-compose ps" -ForegroundColor Gray
    Write-Host "   docker-compose logs -f postgres" -ForegroundColor Gray
}

Write-Host ""
Write-Host "📊 容器狀態：" -ForegroundColor Cyan
docker-compose ps

Write-Host ""
Write-Host "================================" -ForegroundColor Cyan
Write-Host "✨ 設置完成！" -ForegroundColor Green
Write-Host ""

# 讀取配置
$envContent = Get-Content .env
$postgresPort = ($envContent | Where-Object { $_ -match "^POSTGRES_PORT=" }) -replace "POSTGRES_PORT=", ""
$postgresDb = ($envContent | Where-Object { $_ -match "^POSTGRES_DB=" }) -replace "POSTGRES_DB=", ""
$postgresUser = ($envContent | Where-Object { $_ -match "^POSTGRES_USER=" }) -replace "POSTGRES_USER=", ""

if (!$postgresPort) { $postgresPort = "5432" }
if (!$postgresDb) { $postgresDb = "bitfinex_lending" }
if (!$postgresUser) { $postgresUser = "user" }

Write-Host "📌 數據庫連接信息：" -ForegroundColor Cyan
Write-Host "   主機: localhost" -ForegroundColor White
Write-Host "   端口: $postgresPort" -ForegroundColor White
Write-Host "   數據庫: $postgresDb" -ForegroundColor White
Write-Host "   用戶: $postgresUser" -ForegroundColor White
Write-Host ""
Write-Host "🛠️  常用命令：" -ForegroundColor Cyan
Write-Host "   查看日誌: docker-compose logs -f postgres" -ForegroundColor Gray
Write-Host "   停止數據庫: docker-compose down" -ForegroundColor Gray
Write-Host "   重啟數據庫: docker-compose restart postgres" -ForegroundColor Gray
Write-Host "   連接數據庫: docker-compose exec postgres psql -U $postgresUser -d $postgresDb" -ForegroundColor Gray
Write-Host ""
Write-Host "📚 詳細文檔: DOCKER_SETUP.md" -ForegroundColor Cyan
Write-Host ""

# 詢問是否啟動 pgAdmin
$response = Read-Host "❓ 是否要啟動 pgAdmin？(y/N)"
if ($response -match "^[Yy]$") {
    Write-Host "🚀 正在啟動 pgAdmin..." -ForegroundColor Cyan
    docker-compose --profile tools up -d pgadmin
    
    $pgadminPort = ($envContent | Where-Object { $_ -match "^PGADMIN_PORT=" }) -replace "PGADMIN_PORT=", ""
    $pgadminEmail = ($envContent | Where-Object { $_ -match "^PGADMIN_EMAIL=" }) -replace "PGADMIN_EMAIL=", ""
    
    if (!$pgadminPort) { $pgadminPort = "5050" }
    if (!$pgadminEmail) { $pgadminEmail = "admin@admin.com" }
    
    Write-Host "✅ pgAdmin 已啟動" -ForegroundColor Green
    Write-Host "🌐 訪問 http://localhost:$pgadminPort" -ForegroundColor Cyan
    Write-Host "📧 郵箱: $pgadminEmail" -ForegroundColor White
}

Write-Host ""
Write-Host "🎉 完成！" -ForegroundColor Green


