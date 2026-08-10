# Devine Designs - Digital Asset Scorecard Platform

A Flask web application for generating website quality scorecards and managing leads.

## Quick Start (Railway.app)

### Deploy for FREE:
1. Push to GitHub: `git push origin main`
2. Sign up on https://railway.app (free, with GitHub)
3. Deploy from GitHub repo
4. Add PostgreSQL database
5. Add environment variables (see below)
6. Your app is live!

## Environment Variables

```
FLASK_ENV=production
DEBUG=false
SECRET_KEY=<your-secret-key>
ADMIN_API_KEY=<your-admin-key>
SENDGRID_API_KEY=<your-sendgrid-key>
SENDGRID_FROM_EMAIL=info@devinedesignssa.com
CORS_ORIGINS=https://devinedesignssa.com
```

## Running Locally

```bash
cd backend
pip install -r requirements.txt
flask run
```

## Tech Stack

- **Backend:** Flask, SQLAlchemy, PostgreSQL
- **Frontend:** HTML, CSS, JavaScript
- **Deployment:** Railway.app (free)
- **Email:** SendGrid

## Features

- Website quality scorecard generator (25+ checks)
- Lead management system
- Admin dashboard
- ROI calculator
- Rate limiting & security
- API documentation (Swagger)

## Database Migrations

```bash
flask db upgrade
```

## Documentation

- `RAILWAY_SETUP.md` - Step-by-step Railway deployment
- `FREE_HOSTING_OPTIONS.md` - Alternative free hosting options
- `FREE_DEPLOYMENT_ACTION.md` - Your action plan
