# 🚀 Ubuntu Server - Quick Start

**Server:** devine@192.168.110.18

## 5-Minute Setup

### Step 1: SSH Into Your Server
```bash
ssh devine@192.168.110.18
```

### Step 2: Run One Command
```bash
curl https://raw.githubusercontent.com/ZeroDayRaven/Devine-Desines/main/setup-server.sh | bash
```

**That's it!** The script will:
- Install Docker
- Clone your repo
- Start PostgreSQL
- Run your app

### Step 3: Access Your App

**On the server:**
```
http://localhost:5000
```

**From other computers on your network:**
```
http://192.168.110.18:5000
```

---

## What's Running

- **Web App:** `http://192.168.110.18:5000`
- **Database:** PostgreSQL on port 5432
- **User:** devine
- **Password:** postgres_password_123 (change later if needed)

---

## Common Commands (SSH into server first)

```bash
# View status
docker-compose ps

# View logs
docker-compose logs -f

# Stop everything
docker-compose down

# Restart everything
docker-compose restart

# Rebuild after code changes
docker-compose up -d --build
```

---

## If Script Fails

Check `SERVER_SETUP.md` for manual installation steps.

---

## Need to Update Code?

On your server:
```bash
cd ~/apps/Devine-Desines
git pull origin main
docker-compose up -d --build
```

---

## Share Your App

Tell your team:
```
http://192.168.110.18:5000
```

They can access it from any computer on your network!

---

**That's all you need!** 🎉
