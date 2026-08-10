# Devine Designs - Digital Asset Scorecard Platform

A Flask web application for generating website quality scorecards and managing leads.

**Tech Stack:** Flask, SQLAlchemy, PostgreSQL, Gunicorn

**Deployment:** Railway.app (Free tier)

## Quick Deploy to Railway

1. Sign up: https://railway.app (with GitHub)
2. Create new project from this GitHub repo
3. Add PostgreSQL database
4. Set environment variables (see below)
5. Auto-deploys on push to main

## Environment Variables

Railway reads from your `.env` file. Required:

```
DATABASE_URL=postgresql://...  # Railway auto-injects this
FLASK_ENV=production
DEBUG=false
SECRET_KEY=<your-secret-key>
ADMIN_API_KEY=<your-admin-key>
SENDGRID_API_KEY=<your-sendgrid-key>
SENDGRID_FROM_EMAIL=info@devinedesignssa.com
CORS_ORIGINS=https://devinedesignssa.com
```

## Local Development

```bash
cd backend
pip install -r ../requirements.txt
flask run
```

## Database Migrations

```bash
flask db upgrade
```

## Project Structure

```
backend/
  ├── app/               # Flask application
  ├── migrations/        # Database migrations
  └── run.py            # Entry point

frontend/
  ├── index.html        # Landing page
  ├── images/           # Assets
  └── robots.txt        # SEO

Dockerfile             # Production image
Procfile              # Railway config
requirements.txt      # Python dependencies
```

## Features

- Website quality scorecard (25+ checks)
- Lead management
- Admin dashboard
- Rate limiting & security
- API documentation (Swagger)
- SendGrid email integration
