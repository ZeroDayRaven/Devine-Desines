# 🏗️ Server Architecture Overview

## Current Setup

```
Ubuntu 22.04.5 LTS (divine-server)
192.168.110.152
│
├── Hardware
│   ├── CPU: x86_64 (64-bit)
│   ├── RAM: 3.7GB (2.5GB available)
│   ├── Disk: 98GB (85GB available)
│   └── Storage: 85GB+ free space
│
├── Software (Installed)
│   ├── Docker ✅ (running)
│   ├── containerd ✅ (running)
│   ├── Git ✅ 2.34.1
│   ├── Python ✅ 3.10.12
│   ├── SSH ✅ (OpenSSH)
│   └── Docker Compose ⚠️ (not installed)
│
├── User Account
│   ├── Username: devine
│   ├── Groups: docker, sudo, etc.
│   ├── SSH: Accessible
│   └── Permissions: All necessary ✅
│
└── Ready for Deployment
    ├── Docker: Clean (0 images, 0 containers)
    ├── Home: /home/devine
    ├── Apps location: /home/devine/apps (will create)
    └── Status: Ready ✅
```

---

## Proposed Deployment Architecture

### What Will Be Deployed (When Ready)

```
/home/devine/apps/Devine-Desines/
│
├── Docker Containers:
│   ├── db (PostgreSQL)
│   │   ├── Port: 5432 (internal)
│   │   ├── Data: /var/lib/postgresql/data
│   │   ├── User: devine
│   │   └── Password: postgres_password_123
│   │
│   └── web (Flask App)
│       ├── Port: 5000 (external: http://192.168.110.152:5000)
│       ├── Framework: Flask
│       ├── Server: Gunicorn
│       ├── Workers: 2
│       └── Auto-reload: Yes
│
├── Volumes:
│   ├── postgres_data/ (database persistence)
│   └── Code: /home/devine/apps/Devine-Desines
│
├── Environment:
│   ├── FLASK_ENV: production
│   ├── DEBUG: false
│   ├── DATABASE_URL: postgresql://devine:***@db:5432/devine
│   ├── Secret keys: (from .env file)
│   └── API keys: (from .env file)
│
└── Network:
    ├── Internal: devine_network (Docker)
    ├── External: 192.168.110.152:5000
    └── Accessible: From any device on 192.168.110.x network
```

---

## Data Flow (After Deployment)

```
External Device (192.168.110.x)
    ↓
http://192.168.110.152:5000
    ↓
Docker Network (devine_network)
    ↓
┌─────────────────────────────────┐
│ Web Container (Flask + Gunicorn) │
│ Port 5000                        │
└──────────────┬──────────────────┘
               ↓
         Database Queries
               ↓
┌─────────────────────────────────┐
│ DB Container (PostgreSQL)        │
│ Port 5432 (internal only)        │
│ Persistent Volume: postgres_data │
└─────────────────────────────────┘
```

---

## Network Configuration

```
Your Network: 192.168.110.x
│
└── Your Server (devine-server)
    ├── IP: 192.168.110.152
    ├── SSH Access: Enabled
    ├── Docker: Ready
    │
    └── When Deployed:
        └── App URL: http://192.168.110.152:5000
            (Accessible from any device on network)
```

---

## Resource Allocation (Estimated)

### Current Usage
- **Disk:** 8.6G used / 85G available (10% → 0% after deployment)
- **RAM:** 913M used / 3.7G available (25% → ~70% after deployment)
- **Swap:** 1.0M used / 3.7G available (minimal)

### After Deployment Estimate
- **Disk:** +2-3GB for images/containers (still ~80GB+ free)
- **RAM:** +1-1.5GB for containers (still ~1GB+ free)
- **Status:** Still healthy ✅

---

## Connections & Ports

### SSH
- **Port:** 22
- **User:** devine
- **Password:** Lizzy@0928
- **Status:** ✅ Active

### Application (When Deployed)
- **Port:** 5000
- **URL:** http://192.168.110.152:5000
- **Access:** Network-wide (192.168.110.x)
- **Status:** Ready (not running yet)

### Database (When Deployed)
- **Port:** 5432
- **Access:** Internal Docker network only
- **External Access:** Via application only
- **Status:** Ready (not running yet)

---

## Summary

✅ **Your server is perfectly configured for Devine Designs deployment**

- Server is clean and ready
- All dependencies present
- Plenty of resources
- Network connectivity verified
- User permissions correct
- Docker ready
- Just needs deployment command when you're ready

**Current Status:** Scanned, documented, awaiting deployment instructions ✅

