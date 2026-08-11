# 🖥️ Ubuntu Server Setup - Divine Designs

Your server: `devine@192.168.110.18`

## Quick Start (5 minutes)

### 1. SSH into Your Server

```bash
ssh devine@192.168.110.18
```

### 2. Download and Run Setup Script

```bash
cd ~
curl -O https://raw.githubusercontent.com/ZeroDayRaven/Devine-Desines/main/setup-server.sh
chmod +x setup-server.sh
./setup-server.sh
```

This will:
- ✅ Update system
- ✅ Install Docker
- ✅ Install Git
- ✅ Clone your repo
- ✅ Create PostgreSQL database
- ✅ Start your app

### 3. Access Your App

**Local (on the server):**
```
http://localhost:5000
```

**From your network:**
```
http://192.168.110.18:5000
```

**From other computers on your network:**
```
http://192.168.110.18:5000
```

---

## Manual Setup (if script fails)

### 1. Update System
```bash
sudo apt-get update
sudo apt-get upgrade -y
```

### 2. Install Docker
```bash
sudo apt-get install -y docker.io docker-compose
sudo usermod -aG docker devine
# Logout and login again for group changes to take effect
```

### 3. Install Git
```bash
sudo apt-get install -y git
```

### 4. Clone Repository
```bash
mkdir -p ~/apps
cd ~/apps
git clone https://github.com/ZeroDayRaven/Devine-Desines.git
cd Devine-Desines
```

### 5. Create .env File
```bash
cat > .env << 'EOF'
FLASK_ENV=production
DEBUG=false
DATABASE_URL=postgresql://devine:postgres_password_123@db:5432/devine
SECRET_KEY=vtUr3.Dlc6Qys,ubE%qBG8&dn"*Vi(h'
ADMIN_API_KEY=z6QVgirf!UZFJK%-IhO,/qye)"A9cECb
SENDGRID_API_KEY=your-sendgrid-key
SENDGRID_FROM_EMAIL=info@devinedesignssa.com
CORS_ORIGINS=http://192.168.110.18:5000,http://localhost:5000
EOF
```

### 6. Start Services
```bash
docker-compose up -d
```

---

## Common Commands

### View Running Containers
```bash
docker-compose ps
```

### View Logs
```bash
# All logs
docker-compose logs -f

# Just web app
docker-compose logs -f web

# Just database
docker-compose logs -f db
```

### Stop Services
```bash
docker-compose down
```

### Restart Services
```bash
docker-compose restart
```

### Restart and Rebuild
```bash
docker-compose down
docker-compose up -d --build
```

### Access Database
```bash
docker-compose exec db psql -U devine -d devine
```

### View Database Tables
```bash
docker-compose exec db psql -U devine -d devine -c "\dt"
```

### Run Migrations
```bash
docker-compose exec web flask db upgrade
```

### Run Migrations (Fresh)
```bash
docker-compose exec web flask db downgrade
docker-compose exec web flask db upgrade
```

---

## Database Info

- **Host:** localhost (or db from inside container)
- **Port:** 5432
- **User:** devine
- **Password:** postgres_password_123
- **Database:** devine

---

## Network Access

Your server is available on your local network:
- **IP:** 192.168.110.18
- **Port:** 5000
- **URL:** http://192.168.110.18:5000

Other computers on your network can access:
```
http://192.168.110.18:5000
```

---

## Troubleshooting

### Port 5000 already in use
```bash
# Kill process on port 5000
sudo lsof -i :5000
sudo kill -9 <PID>
```

### Docker permission denied
```bash
# Add user to docker group
sudo usermod -aG docker $USER
# Logout and login again
```

### Database connection failed
```bash
# Check database is running
docker-compose ps

# Check database logs
docker-compose logs db

# Restart database
docker-compose restart db
```

### Can't connect from other computers
- Check firewall: `sudo ufw status`
- Enable port: `sudo ufw allow 5000`
- Check if service is running: `docker-compose ps`

---

## Keep Running After Logout

Services restart automatically with `restart: unless-stopped`

But if server reboots, run:
```bash
cd ~/apps/Devine-Desines
docker-compose up -d
```

Or create a systemd service for auto-start on reboot.

---

## Stop Everything

```bash
docker-compose down
```

---

## Need Help?

Check logs:
```bash
docker-compose logs -f
```

View specific container:
```bash
docker-compose logs -f web
```

SSH into container:
```bash
docker-compose exec web bash
```
