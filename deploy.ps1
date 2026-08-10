# Devine Designs - DigitalOcean Deployment Script (PowerShell)
# This script prepares and deploys your app to DigitalOcean App Platform

Write-Host "🚀 Devine Designs - DigitalOcean Deployment Script" -ForegroundColor Green
Write-Host "=================================================" -ForegroundColor Green
Write-Host ""

# Step 1: Check prerequisites
Write-Host "📋 Step 1: Checking prerequisites..."

try {
    git --version > $null 2>&1
    Write-Host "✓ Git installed" -ForegroundColor Green
}
catch {
    Write-Host "❌ Git is not installed" -ForegroundColor Red
    exit 1
}

try {
    docker --version > $null 2>&1
    Write-Host "✓ Docker installed" -ForegroundColor Green
}
catch {
    Write-Host "❌ Docker is not installed" -ForegroundColor Red
    exit 1
}

Write-Host ""

# Step 2: Verify required files
Write-Host "📋 Step 2: Verifying required files..."

$requiredFiles = @(
    "app.yaml",
    "backend\Dockerfile",
    "backend\requirements.txt",
    "backend\run.py",
    ".env",
    "backend\.env"
)

foreach ($file in $requiredFiles) {
    if (Test-Path $file) {
        Write-Host "✓ $file exists" -ForegroundColor Green
    }
    else {
        Write-Host "❌ $file not found" -ForegroundColor Red
        exit 1
    }
}

Write-Host ""

# Step 3: Verify environment variables
Write-Host "📋 Step 3: Checking environment variables..."

# Load .env file
$envFile = Get-Content .env | Where-Object { $_ -ne "" -and !$_.StartsWith("#") }
$envVars = @{}

foreach ($line in $envFile) {
    $key, $value = $line -split '=', 2
    $envVars[$key.Trim()] = $value.Trim()
}

$requiredVars = @(
    "SECRET_KEY",
    "ADMIN_API_KEY",
    "SENDGRID_API_KEY",
    "SENDGRID_FROM_EMAIL",
    "CORS_ORIGINS"
)

foreach ($var in $requiredVars) {
    if ($envVars.ContainsKey($var) -and ![string]::IsNullOrEmpty($envVars[$var])) {
        Write-Host "✓ $var is set" -ForegroundColor Green
    }
    else {
        Write-Host "❌ $var not set in .env" -ForegroundColor Red
        exit 1
    }
}

Write-Host ""

# Step 4: Test Docker build locally
Write-Host "📋 Step 4: Testing Docker build locally..."

$buildOutput = docker build -t test-devine-designs:latest backend/ 2>&1

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Docker build successful" -ForegroundColor Green
    docker rmi test-devine-designs:latest > $null 2>&1
}
else {
    Write-Host "❌ Docker build failed" -ForegroundColor Red
    Write-Host $buildOutput
    exit 1
}

Write-Host ""

# Step 5: Git status check
Write-Host "📋 Step 5: Checking Git status..."

$gitStatus = git status --porcelain

if ($gitStatus) {
    Write-Host "⚠️  You have uncommitted changes" -ForegroundColor Yellow
    Write-Host "Please commit your changes before deploying:"
    Write-Host "  git add ."
    Write-Host '  git commit -m "Ready for DigitalOcean deployment"'
    Write-Host "  git push origin main"
    exit 1
}
else {
    Write-Host "✓ All changes committed" -ForegroundColor Green
}

Write-Host ""

# Step 6: Verify GitHub repository
Write-Host "📋 Step 6: Checking GitHub connection..."

$gitRemote = git remote get-url origin

if ($gitRemote -like "*github.com*") {
    Write-Host "✓ GitHub repository connected" -ForegroundColor Green
    Write-Host "   Repository: $gitRemote"
}
else {
    Write-Host "❌ No GitHub remote found" -ForegroundColor Red
    exit 1
}

Write-Host ""

# Step 7: Instructions
Write-Host "🎯 Deployment Steps:" -ForegroundColor Cyan
Write-Host "====================" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Go to DigitalOcean App Platform:"
Write-Host "   https://cloud.digitalocean.com/apps"
Write-Host ""
Write-Host "2. Click 'Create App'"
Write-Host ""
Write-Host "3. Select 'GitHub' as source"
Write-Host ""
Write-Host "4. Choose your repository and select 'main' branch"
Write-Host ""
Write-Host "5. DigitalOcean will auto-detect app.yaml"
Write-Host ""
Write-Host "6. Before deploying, add these environment variables:"
foreach ($var in $requiredVars) {
    $value = $envVars[$var]
    $truncated = if ($value.Length -gt 25) { $value.Substring(0, 20) + "..." } else { $value }
    Write-Host "   • $var = $truncated"
}
Write-Host ""
Write-Host "7. Click 'Create Resources' and wait for deployment"
Write-Host ""
Write-Host "8. After deployment, update your Squarespace domain DNS:"
Write-Host "   • Go to Squarespace Domain Settings → DNS"
Write-Host "   • Add CNAME record pointing to DigitalOcean URL"
Write-Host ""

# Step 8: Confirmation
Write-Host ""
$response = Read-Host "Are you ready to deploy? (y/n)"
if ($response -ne 'y' -and $response -ne 'Y') {
    Write-Host "Deployment cancelled."
    exit 0
}

Write-Host ""

# Step 9: Summary
Write-Host "📊 Deployment Summary:" -ForegroundColor Cyan
Write-Host "======================" -ForegroundColor Cyan
Write-Host ""
Write-Host "App Name: devine-designs"
Write-Host "Repository: $gitRemote"
Write-Host "Branch: main"
Write-Host "Dockerfile: backend\Dockerfile"
Write-Host "Port: 5000"
Write-Host "Health Check: /health"
Write-Host ""
Write-Host "Environment Variables:"
Write-Host "  • FLASK_ENV = production"
Write-Host "  • DEBUG = false"
foreach ($var in $requiredVars) {
    Write-Host "  • $var = (set)"
}
Write-Host ""
Write-Host "✓ All checks passed!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:"
Write-Host "1. Go to https://cloud.digitalocean.com/apps"
Write-Host "2. Click 'Create App'"
Write-Host "3. Follow the on-screen instructions"
Write-Host "4. Enter your environment variables"
Write-Host "5. Click 'Create Resources'"
Write-Host ""
Write-Host "After deployment:"
Write-Host "1. Get your DigitalOcean app URL"
Write-Host "2. Update DNS records in Squarespace"
Write-Host "3. Run: flask db upgrade (via DigitalOcean console)"
Write-Host ""
Write-Host "Monitor deployment at: https://cloud.digitalocean.com/apps"
Write-Host ""
