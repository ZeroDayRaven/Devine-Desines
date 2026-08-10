# DigitalOcean Deployment Guide for Devine Designs

## Prerequisites

- DigitalOcean account (https://digitalocean.com)
- GitHub account with your code pushed
- SendGrid API key (already have)
- Your security keys (SECRET_KEY, ADMIN_API_KEY)

---

## Step 1: Create DigitalOcean App Platform Project

### Option A: Via Web Dashboard (Easiest)

1. **Go to DigitalOcean Dashboard**
   - https://cloud.digitalocean.com/apps

2. **Click "Create App"**

3. **Select GitHub as source**
   - Authorize DigitalOcean to access your GitHub
   - Select your repository
   - Select branch: `main`

4. **Configure the app**
   - App name: `devine-designs`
   - Region: Choose closest to your users
   - SourceDirectory: `backend`

5. **Add Environment Variables**
   - Click "Edit" in the environment variables section
   - Add these:
   ```
   FLASK_ENV=production
   DEBUG=false
   SECRET_KEY=<your-secret-key>
   ADMIN_API_KEY=<your-admin-api-key>
   SENDGRID_API_KEY=<your-sendgrid-api-key>
   SENDGRID_FROM_EMAIL=info@devinedesignssa.com
   CORS_ORIGINS=https://devinedesignssa.com,https://www.devinedesignssa.com
   ```

6. **Configure Database**
   - Click "Components"
   - Click "Create" → Add Database
   - Engine: PostgreSQL
   - Version: 15
   - Name: `postgres`

7. **Configure Web Service**
   - HTTP Port: `5000`
   - Run Command: `gunicorn --workers 2 --bind 0.0.0.0:5000 --timeout 120 run:app`
   - Health Check: `/health`

8. **Deploy**
   - Click "Next"
   - Review settings
   - Click "Create Resources"
   - Wait 5-10 minutes for deployment

---

### Option B: Via app.yaml (Advanced)

1. **Push app.yaml to your repository root**
   ```bash
   git add app.yaml
   git commit -m "Add DigitalOcean app spec"
   git push origin main
   ```

2. **Go to DigitalOcean Dashboard**
   - https://cloud.digitalocean.com/apps

3. **Click "Create App"**

4. **Select GitHub**

5. **App will auto-detect app.yaml**

6. **Add environment variables before deploying**
   - SECRET_KEY, ADMIN_API_KEY, SENDGRID_API_KEY, etc.

7. **Click "Create Resources"**

---

## Step 2: Update requirements.txt

Add `gunicorn` for production:

```bash
# In backend/requirements.txt, add:
gunicorn==21.2.0
```

---

## Step 3: Update Dockerfile for Production

Your Dockerfile should have:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=run.py
ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

CMD ["gunicorn", "--workers", "2", "--worker-class", "sync", "--bind", "0.0.0.0:5000", "--timeout", "120", "run:app"]
```

---

## Step 4: Update run.py for Production

```python
from app import create_app
import os
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

app = create_app()

if __name__ == '__main__':
    debug_mode = os.getenv('DEBUG', 'false').lower() == 'true'
    app.run(host='0.0.0.0', port=5000, debug=debug_mode)
```

---

## Step 5: Database Migrations

Once deployed, run migrations:

1. **In DigitalOcean Dashboard**
   - Go to your app
   - Click "Console"
   - Select the `web` component
   - Run: `flask db upgrade`

Or connect via SSH and run migrations manually.

---

## Step 6: Point Your Domain (Squarespace)

### Get Your DigitalOcean URL

1. Go to your app in DigitalOcean
2. Find the live app URL (looks like: `https://devine-designs-abcd1234.ondigitalocean.app`)

### Update Squarespace DNS

1. **Log into Squarespace**
2. **Go to Domain Settings**
3. **Find DNS Settings**
4. **Add/Update CNAME record:**
   ```
   Type: CNAME
   Name: www
   Value: devine-designs-abcd1234.ondigitalocean.app
   ```

5. **Wait 24-48 hours for DNS propagation**

---

## Step 7: Connect Custom Domain

In DigitalOcean:

1. **Go to your app**
2. **Click "Settings"**
3. **Go to "Domains"**
4. **Click "Add Domain"**
5. **Enter:** `devinedesignssa.com`
6. **Follow instructions to add DNS records to Squarespace**

---

## Troubleshooting

### App won't start

**Check logs:**
```bash
# In DigitalOcean Console
docker logs <container-id>
```

**Common issues:**
- Missing environment variable → Add to app settings
- Database connection failed → Check DATABASE_URL format
- Port already in use → Change port in app.yaml

### Database connection error

**Verify:**
1. Database component exists in DigitalOcean
2. DATABASE_URL is set correctly
3. Format: `postgresql://user:password@host:port/dbname`

**Get DATABASE_URL:**
1. Go to "Components" in your app
2. Find PostgreSQL database
3. Click it
4. Copy the connection string

### 502 Bad Gateway

**Usually means:**
- App crashed (check logs)
- Gunicorn not running properly
- Port mismatch (must be 5000)

---

## Production Checklist

- [ ] App.yaml created and committed
- [ ] requirements.txt includes gunicorn
- [ ] Dockerfile updated
- [ ] run.py configured
- [ ] Environment variables set in DigitalOcean
- [ ] Database created and connected
- [ ] Migrations run (`flask db upgrade`)
- [ ] Custom domain added
- [ ] DNS records updated
- [ ] Health check endpoint working
- [ ] All API endpoints responding
- [ ] Admin dashboard accessible
- [ ] Logs monitored

---

## Monitoring & Logging

**In DigitalOcean Dashboard:**

1. **View Logs:**
   - Click app name
   - Click "Runtime Logs"
   - View real-time logs

2. **View Alerts:**
   - Click "Alerts"
   - Set up notifications for failures

3. **View Metrics:**
   - Click app name
   - Click "Insights"
   - Monitor CPU, memory, requests

---

## Next Steps After Deployment

1. **Set up automated backups:**
   ```bash
   # In DigitalOcean database settings
   - Enable automated backups
   - Set retention to 30 days
   ```

2. **Configure SSL/HTTPS:**
   - DigitalOcean includes free SSL
   - Auto-renews certificates

3. **Set up custom domain email (optional):**
   - Use SendGrid for transactional emails
   - Already configured in your app

4. **Monitor uptime:**
   - Use StatusPage (https://www.statuspage.io)
   - Free tier available

5. **Set up CI/CD:**
   - Push to main → Auto-deploys in DigitalOcean
   - Already configured with app.yaml

---

## Getting Help

**If deployment fails:**

1. **Check DigitalOcean logs:**
   - Dashboard → Your App → Runtime Logs

2. **Common errors:**
   - "Port already in use" → Change run command
   - "Database connection failed" → Check DATABASE_URL
   - "Module not found" → Check requirements.txt
   - "Permission denied" → Check file permissions

3. **Test locally first:**
   ```bash
   docker compose up
   curl http://localhost:5000/health
   ```

---

**Your app should be live on DigitalOcean within 10 minutes!** 🚀
