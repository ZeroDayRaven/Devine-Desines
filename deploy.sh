#!/bin/bash

# Devine Designs - DigitalOcean Deployment Script
# This script prepares and deploys your app to DigitalOcean App Platform

set -e

echo "🚀 Devine Designs - DigitalOcean Deployment Script"
echo "=================================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Step 1: Check prerequisites
echo "📋 Step 1: Checking prerequisites..."

if ! command -v git &> /dev/null; then
    echo -e "${RED}❌ Git is not installed${NC}"
    exit 1
fi

if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker is not installed${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Git installed${NC}"
echo -e "${GREEN}✓ Docker installed${NC}"
echo ""

# Step 2: Verify required files
echo "📋 Step 2: Verifying required files..."

REQUIRED_FILES=(
    "app.yaml"
    "backend/Dockerfile"
    "backend/requirements.txt"
    "backend/run.py"
    ".env"
    "backend/.env"
)

for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo -e "${GREEN}✓ $file exists${NC}"
    else
        echo -e "${RED}❌ $file not found${NC}"
        exit 1
    fi
done
echo ""

# Step 3: Verify environment variables
echo "📋 Step 3: Checking environment variables..."

REQUIRED_VARS=(
    "SECRET_KEY"
    "ADMIN_API_KEY"
    "SENDGRID_API_KEY"
    "SENDGRID_FROM_EMAIL"
    "CORS_ORIGINS"
)

source .env

for var in "${REQUIRED_VARS[@]}"; do
    if [ -z "${!var}" ]; then
        echo -e "${RED}❌ $var not set in .env${NC}"
        exit 1
    else
        echo -e "${GREEN}✓ $var is set${NC}"
    fi
done
echo ""

# Step 4: Test Docker build locally
echo "📋 Step 4: Testing Docker build locally..."

if docker build -t test-divine-designs:latest backend/ > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Docker build successful${NC}"
    docker rmi test-divine-designs:latest > /dev/null 2>&1
else
    echo -e "${RED}❌ Docker build failed${NC}"
    docker rmi test-divine-designs:latest > /dev/null 2>&1
    exit 1
fi
echo ""

# Step 5: Git status check
echo "📋 Step 5: Checking Git status..."

if ! git diff-index --quiet HEAD --; then
    echo -e "${YELLOW}⚠️  You have uncommitted changes${NC}"
    echo "Please commit your changes before deploying:"
    echo "  git add ."
    echo "  git commit -m 'Ready for DigitalOcean deployment'"
    echo "  git push origin main"
    exit 1
else
    echo -e "${GREEN}✓ All changes committed${NC}"
fi
echo ""

# Step 6: Verify GitHub repository
echo "📋 Step 6: Checking GitHub connection..."

if git remote -v | grep -q "github.com"; then
    GITHUB_REPO=$(git remote get-url origin)
    echo -e "${GREEN}✓ GitHub repository connected${NC}"
    echo "   Repository: $GITHUB_REPO"
else
    echo -e "${RED}❌ No GitHub remote found${NC}"
    exit 1
fi
echo ""

# Step 7: Instructions for DigitalOcean deployment
echo "🎯 Deployment Steps:"
echo "===================="
echo ""
echo "1. Go to DigitalOcean App Platform:"
echo "   https://cloud.digitalocean.com/apps"
echo ""
echo "2. Click 'Create App'"
echo ""
echo "3. Select 'GitHub' as source"
echo ""
echo "4. Choose your repository and select 'main' branch"
echo ""
echo "5. DigitalOcean will auto-detect app.yaml"
echo ""
echo "6. Before deploying, add these environment variables:"
for var in "${REQUIRED_VARS[@]}"; do
    echo "   • $var = ${!var:0:20}...${!var: -5}"
done
echo ""
echo "7. Click 'Create Resources' and wait for deployment"
echo ""
echo "8. After deployment, update your Squarespace domain DNS:"
echo "   • Go to Squarespace Domain Settings → DNS"
echo "   • Add CNAME record pointing to DigitalOcean URL"
echo ""

# Step 8: Ask for confirmation
echo ""
read -p "Are you ready to deploy? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Deployment cancelled."
    exit 0
fi
echo ""

# Step 9: Generate summary
echo "📊 Deployment Summary:"
echo "======================"
echo ""
echo "App Name: devine-designs"
echo "Repository: $GITHUB_REPO"
echo "Branch: main"
echo "Dockerfile: backend/Dockerfile"
echo "Port: 5000"
echo "Health Check: /health"
echo ""
echo "Environment Variables:"
echo "  • FLASK_ENV = production"
echo "  • DEBUG = false"
for var in "${REQUIRED_VARS[@]}"; do
    echo "  • $var = (set)"
done
echo ""
echo -e "${GREEN}✓ All checks passed!${NC}"
echo ""
echo "Next steps:"
echo "1. Go to https://cloud.digitalocean.com/apps"
echo "2. Click 'Create App'"
echo "3. Follow the on-screen instructions"
echo "4. Enter your environment variables"
echo "5. Click 'Create Resources'"
echo ""
echo "After deployment:"
echo "1. Get your DigitalOcean app URL"
echo "2. Update DNS records in Squarespace"
echo "3. Run: flask db upgrade (via DigitalOcean console)"
echo ""
echo "Monitor deployment at: https://cloud.digitalocean.com/apps"
echo ""
