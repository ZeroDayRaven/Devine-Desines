# 🚀 Devine Designs - Quick Reference Guide

## What You Need to Collect (One Page Summary)

### **CRITICAL - Must Have Before Deployment**

| Item | Where to Get | Status |
|------|-------------|--------|
| SendGrid API Key | https://app.sendgrid.com/settings/api_keys | ⏳ Get it |
| SendGrid Email | Your verified email in SendGrid | ⏳ Confirm it |
| Database URL | PostgreSQL connection string | ⏳ Decide DB |
| SECRET_KEY | Generate random 32+ characters | ⏳ Generate it |
| ADMIN_API_KEY | Generate random 32+ characters | ⏳ Generate it |
| Domain Name | Your website domain | ⏳ Have ready |
| Server IP | Your hosting provider | ⏳ Get it |
| CORS Origins | Your domain(s) | ⏳ List them |

### **OPTIONAL - Nice to Have**

| Item | Where to Get | Status |
|------|-------------|--------|
| Google Analytics ID | https://analytics.google.com | ⏳ Optional |
| Meta Pixel ID | https://business.facebook.com/pixels | ⏳ Optional |
| WhatsApp API Key | WhatsApp Business | ⏳ Optional |
| Stripe API Key | https://dashboard.stripe.com | ⏳ Optional |

---

## 5-Minute Setup Flow

```
1. Collect information (use SETUP_PROMPT_FOR_AI.md)
   ↓
2. Fill backend/.env with your values
   ↓
3. Run: docker compose up --build
   ↓
4. Run: docker compose exec web flask db upgrade
   ↓
5. Test: curl http://localhost:5000/health
   ↓
✅ DONE!
```

---

## Essential Environment Variables Template

```bash
# Copy this to backend/.env and fill in YOUR values

# REQUIRED
DATABASE_URL=postgresql://user:password@host:5432/dbname
SECRET_KEY=generate-a-random-32-character-string-here
SENDGRID_API_KEY=SG.your-sendgrid-api-key-here
SENDGRID_FROM_EMAIL=noreply@devinedesignssa.com

# IMPORTANT
ADMIN_API_KEY=generate-random-admin-key-here
CORS_ORIGINS=https://devinedesignssa.com,https://www.devinedesignssa.com

# OPTIONAL
GA_TRACKING_ID=G-XXXXXXXXXX
FB_PIXEL_ID=1234567890
WHATSAPP_API_KEY=your-key-if-needed
WHATSAPP_PHONE_ID=your-id-if-needed

# PRODUCTION
FLASK_ENV=production
DEBUG=false
```

---

## API Keys You Need

### SendGrid (Email) - **REQUIRED**
```
1. Go to https://app.sendgrid.com/settings/api_keys
2. Click "Create API Key"
3. Give it a name like "Devine Designs Production"
4. Copy the key: SG.xxxxxxxxxxxxxxxxxxxxxxx
5. Add to .env as SENDGRID_API_KEY
```

### Google Analytics (Optional)
```
1. Go to https://analytics.google.com
2. Create new property (or use existing)
3. Get the Measurement ID: G-XXXXXXXXXX
4. Add to .env as GA_TRACKING_ID
```

### Meta Pixel (Optional)
```
1. Go to https://business.facebook.com/pixels
2. Create new pixel or copy existing ID
3. Add to .env as FB_PIXEL_ID
```

### Stripe (Optional - for payments)
```
1. Go to https://dashboard.stripe.com/apikeys
2. Copy Live Secret Key: sk_live_xxxxx
3. Add to .env as STRIPE_API_KEY
```

### WhatsApp (Optional - for messaging)
```
1. Set up WhatsApp Business Account
2. Get API Key from Business Manager
3. Get Phone ID from Business Manager
4. Add to .env as WHATSAPP_API_KEY and WHATSAPP_PHONE_ID
```

---

## Critical Decisions You Need to Make

- [ ] Where will database live? (Docker container vs managed service)
- [ ] Where will server live? (AWS, DigitalOcean, Linode, etc.)
- [ ] Where will backups go? (Local, S3, Google Cloud)
- [ ] What's your domain? (devinedesignssa.com)
- [ ] Do you need HTTPS? (Yes - required for production)
- [ ] Do you need monitoring? (Recommended for production)

---

## Generate Random Keys Quickly

**In your terminal:**

```bash
# Generate SECRET_KEY (32 characters)
openssl rand -base64 32

# Generate ADMIN_API_KEY (32 characters)
openssl rand -hex 32

# On Windows PowerShell:
[System.Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes((1..32 | ForEach-Object {[char](Get-Random -Minimum 33 -Maximum 126)}) -join ''))
```

Or use online: https://generateadmiral.com/ (open-source, runs locally)

---

## File Reference

| File | Purpose | Action |
|------|---------|--------|
| `SETUP_REQUIREMENTS.md` | Complete requirements list | Read first |
| `SETUP_PROMPT_FOR_AI.md` | Detailed prompt for ChatGPT/Claude | Use to collect info |
| `DEPLOYMENT_CHECKLIST.md` | Pre-deployment checklist | Follow before deploy |
| `backend/.env.example` | Environment template | Copy & fill |
| `README.md` | Full documentation | Reference |
| `backend/scripts/backup_db.sh` | Backup script | Use for backups |

---

## Troubleshooting

### "I don't have a SendGrid account"
→ Create one at https://sendgrid.com (free tier available: 100 emails/day)

### "I don't know my database URL"
→ If using Docker Compose, it's: `postgresql://devine:devine123@db:5432/devine`

### "I don't have a domain"
→ Buy one at Namecheap, GoDaddy, or Google Domains (~$10-15/year)

### "I don't have a server"
→ Start with DigitalOcean App Platform or AWS ECS (easiest Docker deployment)

### "I don't understand the prompt"
→ Paste the SETUP_PROMPT_FOR_AI.md content into ChatGPT and ask it to walk you through

---

## Quick Start Command

Once you have `.env` filled in:

```bash
# Terminal 1: Start containers
docker compose up --build

# Terminal 2: Initialize database
docker compose exec web flask db upgrade

# Terminal 3: Test it works
curl http://localhost:5000/health

# Access it
- Frontend: http://localhost:5000
- API Docs: http://localhost:5000/api/docs
- Admin: http://localhost:5000/admin/dashboard
  (Header: X-Admin-Key: your-admin-key-value)
```

---

**📋 Status: Use SETUP_PROMPT_FOR_AI.md to collect everything, then come back here for deployment**

