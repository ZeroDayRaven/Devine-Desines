#!/bin/bash

# Divine Designs - Ubuntu Server Setup Script
# Run this on your Ubuntu server to deploy the app locally

set -e

echo "🚀 Setting up Divine Designs on Ubuntu Server..."
echo "Server: devine@192.168.110.18"
echo ""

# Update system
echo "📦 Updating system packages..."
sudo apt-get update
sudo apt-get upgrade -y

# Install Docker
echo "🐳 Installing Docker..."
sudo apt-get install -y docker.io docker-compose
sudo usermod -aG docker devine
echo "✅ Docker installed"

# Install Git
echo "📥 Installing Git..."
sudo apt-get install -y git
echo "✅ Git installed"

# Create app directory
echo "📁 Creating app directory..."
mkdir -p ~/apps
cd ~/apps

# Clone your repository (you'll need to update this with your repo)
echo "📦 Cloning repository..."
git clone https://github.com/ZeroDayRaven/Devine-Desines.git
cd Devine-Desines

# Create .env file with server values
echo "⚙️ Creating .env file..."
cat > .env << 'EOF'
FLASK_ENV=production
DEBUG=false
DATABASE_URL=postgresql://devine:password@db:5432/devine
SECRET_KEY=vtUr3.Dlc6Qys,ubE%qBG8&dn"*Vi(h'
ADMIN_API_KEY=z6QVgirf!UZFJK%-IhO,/qye)"A9cECb
SENDGRID_API_KEY=your-sendgrid-key-here
SENDGRID_FROM_EMAIL=info@devinedesignssa.com
CORS_ORIGINS=http://192.168.110.18:5000,http://localhost:5000
EOF

echo "✅ .env created (update SENDGRID_API_KEY manually if needed)"

# Create docker-compose.yml for local server
echo "🐳 Creating docker-compose.yml..."
cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  db:
    image: postgres:15
    environment:
      POSTGRES_USER: devine
      POSTGRES_PASSWORD: password
      POSTGRES_DB: devine
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U devine"]
      interval: 10s
      timeout: 5s
      retries: 5

  web:
    build: .
    command: >
      sh -c "flask db upgrade &&
             gunicorn --workers 2 --worker-class sync --bind 0.0.0.0:5000 --timeout 120 run:app"
    environment:
      - FLASK_ENV=production
      - DEBUG=false
      - DATABASE_URL=postgresql://devine:password@db:5432/devine
      - SECRET_KEY=vtUr3.Dlc6Qys,ubE%qBG8&dn"*Vi(h'
      - ADMIN_API_KEY=z6QVgirf!UZFJK%-IhO,/qye)"A9cECb
      - SENDGRID_API_KEY=${SENDGRID_API_KEY}
      - SENDGRID_FROM_EMAIL=info@devinedesignssa.com
      - CORS_ORIGINS=http://192.168.110.18:5000,http://localhost:5000
    ports:
      - "5000:5000"
    depends_on:
      db:
        condition: service_healthy
    volumes:
      - .:/app
    restart: unless-stopped

volumes:
  postgres_data:
EOF

echo "✅ docker-compose.yml created"

# Build and start services
echo "🚀 Building and starting services..."
sudo docker-compose up -d

echo ""
echo "✅ Setup complete!"
echo ""
echo "Your app is running at:"
echo "  Local: http://localhost:5000"
echo "  Network: http://192.168.110.18:5000"
echo ""
echo "Database:"
echo "  Host: localhost:5432"
echo "  User: devine"
echo "  Password: password"
echo "  Database: devine"
echo ""
echo "Next steps:"
echo "1. Update SENDGRID_API_KEY in .env if needed"
echo "2. View logs: docker-compose logs -f"
echo "3. Stop services: docker-compose down"
echo "4. Restart services: docker-compose up -d"
echo ""
