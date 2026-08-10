# Setup Prompt - Use This With ChatGPT, Claude, or Any AI Assistant

Copy this entire section and paste it into ChatGPT or Claude to get a structured walkthrough of what you need to collect.

---

I'm deploying a production Flask web application (Devine Designs) with the following tech stack:
- Backend: Flask + SQLAlchemy + PostgreSQL
- Frontend: HTML/CSS/JavaScript (static)
- Infrastructure: Docker + Docker Compose
- Email: SendGrid integration
- Authentication: API key-based admin access
- Features: Website scorecard generator, lead management, admin dashboard

I need to collect and organize ALL configuration details required to set this up properly and deploy to production.

## Answer these questions systematically to help me complete setup:

### **PART 1: SENDGRID EMAIL CONFIGURATION**

1. Do you have a SendGrid account?
   - If NO: "Help me set up a SendGrid account"
   - If YES: "I have my SendGrid API key: [paste key]"

2. What email address should scorecard reports be sent FROM?
   - Example: noreply@devinedesignssa.com

3. Should admin users receive notifications when new leads submit scorecards?
   - If YES: "Send notifications to: [email address]"

4. Do you want to customize the scorecard email template?
   - If YES: "Help me design a professional scorecard email template"

### **PART 2: DATABASE & STORAGE**

5. Where will your database live?
   - Option A: "Docker PostgreSQL container (local development)"
   - Option B: "Managed PostgreSQL service (e.g., AWS RDS, DigitalOcean Managed DB)"
   - Option C: "Self-hosted PostgreSQL server"
   - Selected: [YOUR ANSWER]

6. Database connection details:
   - Database Host: [your host]
   - Database Name: [your db name]
   - Database User: [your username]
   - Database Password: [your password]

7. Where should backups be stored?
   - Option A: "Local folder on server (/backups)"
   - Option B: "AWS S3 bucket"
   - Option C: "Google Cloud Storage"
   - Selected: [YOUR ANSWER]
   - Bucket/Folder name: [name]

8. Backup retention policy:
   - Keep backups for: [30/60/90/180/365 days]
   - Backup frequency: [Daily/Weekly/Every 4 hours]
   - Backup time (UTC): [HH:MM]

### **PART 3: APPLICATION SECURITY**

9. Generate SECRET_KEY:
   - Current value (leave blank to generate): [BLANK or existing key]
   - **ACTION: Generate a random 32+ character string using a strong password generator**

10. Generate ADMIN_API_KEY:
    - This key controls access to /admin/dashboard
    - Suggested format: [random 32 character key]
    - **ACTION: Generate a random 32+ character string**

11. What domains will serve your app?
    - Primary domain: [e.g., devinedesignssa.com]
    - API subdomain: [e.g., api.devinedesignssa.com or /api]
    - Admin panel: [e.g., admin.devinedesignssa.com or /admin]

12. CORS origins whitelist (comma-separated):
    - Example: https://devinedesignssa.com,https://www.devinedesignssa.com,https://api.devinedesignssa.com
    - Your domains: [PASTE HERE]

### **PART 4: ANALYTICS & TRACKING (OPTIONAL)**

13. Do you use Google Analytics 4?
    - If YES: "My GA4 Property ID is: G-XXXXXXXXXX"
    - If NO: "Skip this section"

14. Do you use Meta Pixel?
    - If YES: "My Meta Pixel ID is: 1234567890"
    - If NO: "Skip this section"

15. Should I track custom events?
    - If YES: "Help me set up custom event tracking"
    - If NO: "Use default tracking only"

### **PART 5: WHATSAPP INTEGRATION (OPTIONAL)**

16. Do you need WhatsApp Business API?
    - If YES: 
      - WhatsApp API Key: [paste key]
      - WhatsApp Phone ID: [paste ID]
    - If NO: "Skip WhatsApp integration"

### **PART 6: DOMAIN & DNS**

17. Domain registration:
    - Domain name: [e.g., devinedesignssa.com]
    - Registered with: [GoDaddy/Namecheap/Google Domains/Other]
    - Domain status: [Active/Needs setup]

18. DNS configuration needed:
    - Server IP address: [your server's public IP]
    - Should I set up subdomain? [api.devinedesignssa.com]
    - DNS provider: [Same as registrar/Cloudflare/Route53/Other]

### **PART 7: INFRASTRUCTURE & HOSTING**

19. Where will you host this application?
    - Option A: "Self-hosted VPS (DigitalOcean, Linode, Vultr, etc.)"
    - Option B: "AWS (EC2, ECS, Elastic Beanstalk)"
    - Option C: "Heroku"
    - Option D: "Google Cloud Run"
    - Option E: "Other: [specify]"

20. Server specifications:
    - CPU cores: [1/2/4/8+]
    - RAM: [512MB/1GB/2GB/4GB/8GB+]
    - Storage: [10GB/20GB/50GB/100GB+]
    - Operating system: [Ubuntu 20.04/22.04/CentOS/Other]

21. Do you need SSL/HTTPS certificate?
    - If YES: 
      - Source: [Let's Encrypt (free)/Paid certificate]
      - Instructions: "Set up HTTPS"
    - If NO: "HTTP only (not recommended for production)"

### **PART 8: BACKUP & DISASTER RECOVERY**

22. Automated backup schedule:
    - Frequency: [Daily/Every 4 hours/Weekly]
    - Time: [2 AM UTC/Your preferred time]
    - Retention: [Keep backups for 30/60/90/180/365 days]

23. Have you tested database restore?
    - If NO: "Help me test the backup/restore procedure"
    - If YES: "Restore process confirmed working"

### **PART 9: MONITORING & LOGGING**

24. Monitoring service:
    - Option A: "None (basic health checks only)"
    - Option B: "Datadog"
    - Option C: "New Relic"
    - Option D: "CloudWatch (AWS)"
    - Option E: "Other: [specify]"

25. Logging & log aggregation:
    - Option A: "Local logs only"
    - Option B: "ELK Stack (Elasticsearch/Logstash/Kibana)"
    - Option C: "Papertrail"
    - Option D: "Splunk"
    - Option E: "Other: [specify]"

26. Alerting thresholds:
    - Alert on API error rate > [5%/10%/20%]
    - Alert on response time > [2s/5s/10s]
    - Alert on disk space < [10%/20%/25%]
    - Alert on CPU > [70%/80%/90%]

### **PART 10: CDN & PERFORMANCE (OPTIONAL)**

27. Should I use a Content Delivery Network (CDN)?
    - If YES:
      - CDN provider: [Cloudflare/AWS CloudFront/Fastly/Other]
      - CDN setup: "Help me configure CDN"
    - If NO: "Serve all content from main server"

28. Image optimization:
    - Should images be optimized? [Yes/No]
    - Image format: [Auto/WebP/JPEG/PNG]
    - Max image size: [500KB/1MB/2MB]

### **PART 11: PAYMENT PROCESSING (IF NEEDED)**

29. Do you need payment/subscription features?
    - If NO: "Skip this section"
    - If YES:
      - Payment provider: [Stripe/PayPal/Chargebee/Other]
      - Stripe API key: [paste key]
      - Subscription plans needed: [List your plans]
      - Pricing: [Plan names and prices]

### **PART 12: CRM INTEGRATION (OPTIONAL)**

30. Do you use a CRM system?
    - If NO: "Skip CRM integration"
    - If YES:
      - CRM system: [HubSpot/Pipedrive/Salesforce/Other]
      - CRM API key: [paste key]
      - Auto-sync leads? [Yes/No]

---

## FINAL CHECKLIST BEFORE DEPLOYMENT

Once you've answered all questions above:

- [ ] Create `.env` file in `backend/` directory
- [ ] Fill in all values from your answers above
- [ ] Verify SendGrid API key works (test send email)
- [ ] Verify database connection works
- [ ] Run: `docker compose build`
- [ ] Run: `docker compose up`
- [ ] Run: `docker compose exec web flask db upgrade`
- [ ] Test health endpoint: `curl http://localhost:5000/health`
- [ ] Test API docs: `curl http://localhost:5000/api/docs`
- [ ] Test admin dashboard: `curl -H "X-Admin-Key: [YOUR_KEY]" http://localhost:5000/admin/dashboard`

---

## REQUIRED API KEYS SUMMARY

| Service | Key Name | Status | Value |
|---------|----------|--------|-------|
| SendGrid | SENDGRID_API_KEY | ✅ Required | `SG._________` |
| SendGrid | SENDGRID_FROM_EMAIL | ✅ Required | `noreply@...` |
| Google Analytics | GA_TRACKING_ID | ⚠️ Optional | `G-_________` |
| Meta Pixel | FB_PIXEL_ID | ⚠️ Optional | `___________` |
| WhatsApp | WHATSAPP_API_KEY | ⚠️ Optional | `___________` |
| Stripe | STRIPE_API_KEY | ⚠️ Optional | `sk_live____` |

---

**Once you answer all 30 questions above, your application will be ready to deploy to production!**

