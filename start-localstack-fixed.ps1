# PowerShell script to start Amigurumi Store with LocalStack S3
Write-Host "🚀 Starting Amigurumi Store with LocalStack S3..." -ForegroundColor Green

# Step 1: Clean up any existing containers
Write-Host "🧹 Cleaning up existing containers..." -ForegroundColor Yellow
docker-compose down -v 2>$null
if ($LASTEXITCODE -ne 0) { Write-Host "No existing containers to clean up" -ForegroundColor Gray }

# Step 2: Remove any problematic images
Write-Host "🗑️ Removing old images..." -ForegroundColor Yellow
docker image rm -f amigurumi_store-localstack 2>$null
docker image rm -f amigurumi_store-backend 2>$null
docker image rm -f amigurumi_store-frontend 2>$null

# Step 3: Build and start services in correct order
Write-Host "🏗️ Building and starting infrastructure services..." -ForegroundColor Cyan
docker-compose up -d --build db localstack

# Step 4: Wait for LocalStack to be ready
Write-Host "⏳ Waiting for LocalStack to be ready..." -ForegroundColor Yellow
$maxRetries = 60
$retryCount = 0

while ($retryCount -lt $maxRetries) {
    try {
        $response = docker-compose exec -T localstack curl -f http://localhost:4566/health 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ LocalStack is ready!" -ForegroundColor Green
            break
        }
    }
    catch {
        # Continue to retry
    }
    
    $retryCount++
    Write-Host "⏳ Waiting for LocalStack... (attempt $retryCount/$maxRetries)" -ForegroundColor Gray
    Start-Sleep 5
}

if ($retryCount -eq $maxRetries) {
    Write-Host "❌ LocalStack failed to start within timeout" -ForegroundColor Red
    Write-Host "📋 LocalStack logs:" -ForegroundColor Yellow
    docker-compose logs localstack
    exit 1
}

# Step 5: Initialize infrastructure
Write-Host "🔧 Initializing infrastructure with Terraform..." -ForegroundColor Cyan
docker-compose up --build terraform-init

# Step 6: Verify S3 bucket creation
Write-Host "🧪 Verifying S3 infrastructure..." -ForegroundColor Cyan
docker-compose exec -T localstack aws --endpoint-url=http://localhost:4566 s3 ls

# Step 7: Start backend and frontend
Write-Host "🚀 Starting backend and frontend services..." -ForegroundColor Green
docker-compose up -d --build backend frontend

# Step 8: Wait for all services to be healthy
Write-Host "⏳ Waiting for all services to be healthy..." -ForegroundColor Yellow
Start-Sleep 30

# Step 9: Show service status
Write-Host "📊 Service status:" -ForegroundColor Cyan
docker-compose ps

# Step 10: Test connectivity
Write-Host "🧪 Testing service connectivity..." -ForegroundColor Cyan

# Test LocalStack
Write-Host "🔍 Testing LocalStack..." -ForegroundColor Gray
try {
    $null = Invoke-WebRequest -Uri "http://localhost:4566/health" -UseBasicParsing -TimeoutSec 10
    Write-Host "✅ LocalStack is accessible" -ForegroundColor Green
}
catch {
    Write-Host "❌ LocalStack is not accessible" -ForegroundColor Red
}

# Test Backend
Write-Host "🔍 Testing Backend..." -ForegroundColor Gray
try {
    $null = Invoke-WebRequest -Uri "http://localhost:8000/api/products/" -UseBasicParsing -TimeoutSec 10
    Write-Host "✅ Backend API is accessible" -ForegroundColor Green
}
catch {
    Write-Host "❌ Backend API is not accessible" -ForegroundColor Red
}

# Test Frontend
Write-Host "🔍 Testing Frontend..." -ForegroundColor Gray
try {
    $null = Invoke-WebRequest -Uri "http://localhost:3000" -UseBasicParsing -TimeoutSec 10
    Write-Host "✅ Frontend is accessible" -ForegroundColor Green
}
catch {
    Write-Host "❌ Frontend is not accessible" -ForegroundColor Red
}

Write-Host ""
Write-Host "🎉 Startup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "📱 Access your application:" -ForegroundColor Cyan
Write-Host "   Frontend: http://localhost:3000" -ForegroundColor White
Write-Host "   Backend API: http://localhost:8000/api/" -ForegroundColor White
Write-Host "   Django Admin: http://localhost:8000/admin/ (admin/admin123)" -ForegroundColor White
Write-Host "   LocalStack: http://localhost:4566" -ForegroundColor White
Write-Host ""
Write-Host "🔧 To check logs:" -ForegroundColor Cyan
Write-Host "   docker-compose logs [service_name]" -ForegroundColor White
Write-Host ""
Write-Host "🛑 To stop:" -ForegroundColor Cyan
Write-Host "   docker-compose down" -ForegroundColor White
Write-Host ""
