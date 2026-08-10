# Devine Designs - Setup Requirements Checklist

## Critical Information Needed to Complete Setup

### 1. **SendGrid Email Service** (Required for lead emails)
- [ ] SendGrid account created
- [ ] SendGrid API Key obtained
- [ ] From email address confirmed in SendGrid
- [ ] Email templates customized (scorecard report email, admin notification)

### 2. **Database Configuration** (Required for production)
- [ ] PostgreSQL host/URL confirmed
- [ ] Database username & password set
- [ ] Database name determined
- [ ] Backup storage location decided
- [ ] Backup retention policy defined (days)

### 3. **Application Security** (Required for production)
- [ ] SECRET_KEY generated (minimum 32 characters)
- [ ] ADMIN_API_KEY set (different from default)
- [ ] CORS origins whitelist defined (your actual domain)
- [ ] SSL/HTTPS certificate obtained (if self-hosted)

### 4. **Analytics & Tracking** (Optional but recommended)
- [ ] Google Analytics 4 Property ID (GA_TRACKING_ID)
- [ ] Meta Pixel ID (FB_PIXEL_ID)
- [ ] Google Search Console verified
- [ ] Facebook Business Account configured

### 5. **WhatsApp Integration** (Optional)
- [ ] WhatsApp Business Account created
- [ ] WhatsApp API Key obtained
- [ ] WhatsApp Phone ID obtained
- [ ] WhatsApp webhook URL configured

### 6. **Domain & Hosting** (Required for production)
- [ ] Domain registered
- [ ] Domain pointing to server (DNS A record)
- [ ] Subdomain strategy decided (api.example.com vs example.com/api)
- [ ] CDN provider selected (optional: Cloudflare, AWS CloudFront)

### 7. **Infrastructure** (Required for production)
- [ ] Server/VPS provider selected (AWS, DigitalOcean, Linode, etc.)
- [ ] Server specs finalized (CPU, RAM, storage)
- [ ] Reverse proxy setup (Nginx, Apache)
- [ ] SSL certificate issued (Let's Encrypt recommended)
- [ ] Firewall rules configured

### 8. **Backup & Disaster Recovery** (Required for production)
- [ ] Backup storage location (local, S3, Google Cloud Storage)
- [ ] Backup frequency determined (daily, weekly)
- [ ] Backup retention policy (30 days, 90 days, etc.)
- [ ] Restore procedure tested

### 9. **Monitoring & Logging** (Required for production)
- [ ] Monitoring service selected (Datadog, New Relic, CloudWatch)
- [ ] Log aggregation service (ELK, Splunk, Papertrail)
- [ ] Alert thresholds configured
- [ ] Uptime monitoring setup (StatusCake, UptimeRobot)

### 10. **Payment & Subscription** (If using subscription model)
- [ ] Stripe account created
- [ ] Stripe API keys obtained
- [ ] Subscription pricing configured
- [ ] Invoice template designed

### 11. **CRM & Sales Tools** (Optional but recommended)
- [ ] CRM system selected (HubSpot, Pipedrive, etc.)
- [ ] CRM API key obtained
- [ ] Lead sync rules configured
- [ ] Sales pipeline setup

### 12. **Performance & CDN** (Recommended for production)
- [ ] CDN provider selected (Cloudflare, AWS CloudFront)
- [ ] CDN configured
- [ ] Image optimization setup
- [ ] Caching strategy defined

---

## API Keys Summary Table

| Service | API Key Name | Required | Where to Get | Example |
|---------|-------------|----------|-------------|---------|
| SendGrid | `SENDGRID_API_KEY` | ✅ YES | https://app.sendgrid.com/settings/api_keys | `SG.abc123xyz...` |
| SendGrid | `SENDGRID_FROM_EMAIL` | ✅ YES | Your email verified in SendGrid | `noreply@devinedesignssa.com` |
| Google Analytics | `GA_TRACKING_ID` | ⚠️ Optional | https://analytics.google.com | `G-XXXXXXXXXX` |
| Meta Pixel | `FB_PIXEL_ID` | ⚠️ Optional | https://business.facebook.com/pixels | `1234567890` |
| WhatsApp | `WHATSAPP_API_KEY` | ⚠️ Optional | https://www.whatsapp.com/business/api | Your API key |
| WhatsApp | `WHATSAPP_PHONE_ID` | ⚠️ Optional | WhatsApp Business Manager | Your phone ID |
| Stripe | `STRIPE_API_KEY` | ⚠️ Optional (for payments) | https://dashboard.stripe.com/apikeys | `sk_live_...` |
| Stripe | `STRIPE_WEBHOOK_SECRET` | ⚠️ Optional (for payments) | https://dashboard.stripe.com/webhooks | `whsec_...` |

---

## Environment Variables Reference

### **Database**
```
DATABASE_URL=postgresql://username:password@host:5432/database_name
```

### **Security**
```
SECRET_KEY=your-super-secret-key-min-32-characters
ADMIN_API_KEY=your-admin-api-key-change-in-production
```

### **Email**
```
SENDGRID_API_KEY=SG.your-sendgrid-api-key
SENDGRID_FROM_EMAIL=noreply@devinedesignssa.com
```

### **CORS/Domains**
```
CORS_ORIGINS=https://devinedesignssa.com,https://www.devinedesignssa.com,https://api.devinedesignssa.com
```

### **Analytics**
```
GA_TRACKING_ID=G-XXXXXXXXXX
FB_PIXEL_ID=1234567890
ANALYTICS_CONSENT=true
```

### **WhatsApp (Optional)**
```
WHATSAPP_API_KEY=your-api-key
WHATSAPP_PHONE_ID=your-phone-id
```

### **Flask**
```
FLASK_ENV=production
DEBUG=false
```

---

## Information Collection Prompt

**Use this prompt with ChatGPT/Claude to collect all required information systematically:**

---

# 🚀 Devine Designs - Complete Setup Information Collector

I'm setting up a full-stack application (Flask backend + PostgreSQL + Docker) with email automation, rate limiting, and admin dashboard. Please help me collect and organize ALL the required information to complete the setup.

## Section 1: SendGrid Email Configuration
- What SendGrid account do I need? (Do I have one? If not, help me set it up)
- What SendGrid API Key should I use? (Where do I find it?)
- What email address should be the "from" address? (It must be verified in SendGrid)
- Should I customize the scorecard email template? (What should it say?)
- Do I need an admin notification email? (Who should receive it?)

## Section 2: Database Setup
- What's my PostgreSQL connection string? (host, user, password, database name)
- Should I use the included Docker PostgreSQL or an external database?
- Where should database backups be stored? (Local folder, AWS S3, Google Cloud Storage?)
- How long should I keep backups? (30 days? 90 days? 1 year?)
- How often should backups run? (Daily? Weekly?)

## Section 3: Security Configuration
- What should my SECRET_KEY be? (Generate a 32+ character random string)
- What should my ADMIN_API_KEY be? (For accessing /admin/dashboard)
- What domains will my app be served from? (e.g., devinedesignssa.com, api.devinedesignssa.com)
- Should I use HTTPS/SSL? (Yes for production, how should I get the certificate?)

## Section 4: Analytics & Tracking (Optional)
- Do I have a Google Analytics 4 account? (Where's my GA_TRACKING_ID?)
- Do I use Meta/Facebook Ads? (Where's my Pixel ID?)
- Do I want to track user events? (Yes/No)
- Should I use cookie consent? (Already implemented in frontend)

## Section 5: WhatsApp Integration (Optional)
- Do I need WhatsApp Business API? (For automated messages)
- Do I have a WhatsApp Business Account? (Where's the API key?)
- What's my WhatsApp Phone ID? (For sending/receiving messages)

## Section 6: Domain & Hosting
- What's my primary domain? (e.g., devinedesignssa.com)
- Do I have the domain registered? (Where? GoDaddy, Namecheap, etc.?)
- Do I need subdomains? (api.devinedesignssa.com, admin.devinedesignssa.com?)
- What hosting provider am I using? (AWS, DigitalOcean, Linode, Heroku?)
- What's my server IP address? (For DNS A record)

## Section 7: Infrastructure & DevOps
- Where will I host the Docker containers? (AWS ECS, DigitalOcean App Platform, self-hosted VPS?)
- How much CPU/RAM do I need? (1GB? 2GB? 4GB?)
- Do I need auto-scaling? (Yes/No)
- What's my deployment strategy? (Docker Compose? Kubernetes? Heroku?)
- Do I need a CDN? (Cloudflare, AWS CloudFront, etc.?)

## Section 8: Backup & Disaster Recovery
- Where should backups be stored? (Local /backups folder, AWS S3, Google Cloud Storage?)
- How often should backups run? (Daily at 2 AM? Weekly?)
- How long should I keep backups? (30 days, 90 days, 1 year?)
- Have I tested restoring from a backup?
- Do I need geo-redundant backups?

## Section 9: Monitoring & Logging
- What monitoring service should I use? (Datadog, New Relic, CloudWatch?)
- Where should logs go? (Local logs, ELK Stack, Splunk, Papertrail?)
- What should trigger an alert? (High error rate? API down? Response time > 5s?)
- Do I want uptime monitoring? (StatusCake, UptimeRobot?)

## Section 10: Payment Processing (If Needed)
- Do I need payment processing? (Stripe, PayPal?)
- What subscription plans should I offer?
- What are the prices? (Monthly, annual?)
- Should I use Stripe webhooks for automated billing?

## Section 11: CRM Integration (Optional)
- Do I use a CRM? (HubSpot, Pipedrive, Salesforce?)
- Should I sync leads to my CRM automatically?
- What CRM API key/credentials do I need?

## Section 12: Performance & Optimization
- What's my expected traffic? (100 requests/day? 10,000/day?)
- Should I use a CDN? (For images, CSS, JS)
- Should I implement caching? (Redis? CDN cache?)
- What's my target page load time? (<2s? <3s?)

---

## Quick Action Items

Before running `docker compose up`:

- [ ] Create `.env` file from `.env.example`
- [ ] Fill in all required variables from above
- [ ] Verify SendGrid API key works
- [ ] Test database connection
- [ ] Verify frontend files exist in `/frontend`
- [ ] Run: `docker compose up --build`
- [ ] Run: `docker compose exec web flask db upgrade`
- [ ] Test: `curl http://localhost:5000/health`

---

**Status: Ready to proceed once all sections above are completed** ✅

