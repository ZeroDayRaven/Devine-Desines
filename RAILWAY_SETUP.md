# 🚀 Railway.app - FREE Deployment (5 Minutes)

## Cost: $0/month

---

## Step 1: Push Procfile to GitHub (2 min)

```bash
git add Procfile
git commit -m "Add Procfile for Railway deployment"
git push origin main
```

---

## Step 2: Create Railway Account (2 min)

1. Go to: https://railway.app
2. Click "Start Free"
3. Sign up with GitHub
4. Authorize Railway to access your repos

---

## Step 3: Deploy Your App (1 min)

1. Click "New Project"
2. Click "Deploy from GitHub repo"
3. Select your repository
4. Select `main` branch
5. Railway auto-detects your Procfile and deploys!

---

## Step 4: Add PostgreSQL Database (1 min)

1. In your Railway project, click "Add"
2. Search for "PostgreSQL"
3. Click "Add PostgreSQL"

Railway automatically:
- ✅ Creates database
- ✅ Sets DATABASE_URL environment variable
- ✅ Connects to your app

---

## Step 5: Add Environment Variables (2 min)

1. Click "Variables" in your project
2. Click "Add Variable"
3. Add these 7 variables:

```
FLASK_ENV = production
DEBUG = false
SECRET_KEY = vtUr3.Dlc6Qys,ubE%qBG8&dn"*Vi(h'
ADMIN_API_KEY = z6QVgirf!UZFJK%-IhO,/qye)"A9cECb
SENDGRID_API_KEY = YOUR_SENDGRID_API_KEY
SENDGRID_FROM_EMAIL = info@devinedesignssa.com
CORS_ORIGINS = https://devinedesignssa.com,https://www.devinedesignssa.com
```

---

## Step 6: Get Your Public URL (instant)

1. Railway generates a URL like: `divine-designs-prod.railway.app`
2. Copy this URL
3. This is your live app!

---

## Step 7: Update Squarespace DNS (5 min)

1. Go to Squarespace domain settings
2. Find DNS settings
3. Add CNAME record:
   - **Type:** CNAME
   - **Name:** Leave blank or `@`
   - **Value:** `divine-designs-prod.railway.app`
4. Save

Wait 24-48 hours for DNS to propagate.

---

## Step 8: Run Database Migrations (1 min)

1. In Railway dashboard, click "Deployments"
2. Click the running deployment
3. Click the "Shell" tab
4. Run: `flask db upgrade`

---

## Done! 🎉

Your app is now:
- ✅ Live on Railway
- ✅ Using free PostgreSQL
- ✅ Auto-deploying on every GitHub push
- ✅ Costs: $0/month

---

## Automatic Redeploy

Every time you push to GitHub:
```bash
git push origin main
```

Railway automatically:
1. Pulls latest code
2. Rebuilds image
3. Deploys new version
4. Live in 2-5 minutes

---

## Free Tier Details

**You get:**
- 500 GB-hours/month
- Roughly = $5/month value
- Enough for your small app indefinitely for FREE

**When you upgrade:**
- Only if you want more resources
- Starts at $5/month (still cheap)

---

## What to Do Now

1. ✅ Push Procfile to GitHub
2. ✅ Sign up on Railway.app
3. ✅ Deploy from GitHub
4. ✅ Add PostgreSQL
5. ✅ Add environment variables
6. ✅ Get public URL
7. ✅ Update Squarespace DNS
8. ✅ Run migrations
9. ✅ Your app is live for FREE!

---

**Total time: ~15 minutes**
**Cost: $0** ✅
**Perfect for getting clients!** 🚀
