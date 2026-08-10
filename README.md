# Devine Designs - Digital Asset Scorecard Platform

A full-stack application for generating digital asset scorecards and managing leads.

## Project Structure

```
.
├── backend/                    # Flask API + Database
│   ├── app/
│   │   ├── __init__.py        # Flask app factory with all configurations
│   │   ├── config.py          # Configuration management
│   │   ├── limiter.py         # Rate limiting setup
│   │   ├── errors.py          # Error handling & middleware
│   │   ├── swagger.py         # Swagger/OpenAPI documentation
│   │   ├── models.py          # SQLAlchemy ORM models
│   │   ├── routes/
│   │   │   ├── scorecards.py  # Scorecard generation endpoint
│   │   │   ├── leads.py       # Lead management (TODO)
│   │   │   ├── track.py       # Event tracking
│   │   │   ├── admin.py       # Admin dashboard & analytics
│   │   │   └── health.py      # Health checks & static file serving
│   │   ├── services/
│   │   │   ├── scanner.py     # Website quality scanning (25+ checks)
│   │   │   ├── scoring.py     # Score calculation logic
│   │   │   ├── email.py       # SendGrid email integration
│   │   │   ├── lead_scoring.py # Lead qualification scoring
│   │   │   ├── backup.py      # Database backup & restore
│   │   │   └── analytics.py   # Analytics service (optional)
│   │   └── utils/
│   │       ├── security.py    # URL validation & private IP detection
│   │       └── validators.py  # Email & input validation
│   ├── migrations/            # Database migrations
│   ├── scripts/
│   │   └── backup_db.sh      # Bash script for database backups
│   ├── Dockerfile            # Docker image definition
│   ├── .dockerignore         # Docker build exclusions
│   ├── requirements.txt      # Python dependencies
│   ├── .env.example          # Environment variables template
│   ├── run.py               # Application entry point
│   └── config.py            # Flask configuration
├── frontend/                 # Static HTML/CSS/JS
│   ├── index.html           # Main landing page
│   ├── images/              # Logo and assets
│   ├── robots.txt           # SEO
│   ├── sitemap.xml          # SEO
│   └── CNAME               # Custom domain for GitHub Pages
├── docker-compose.yml       # Multi-container orchestration
└── README.md               # This file
```

## Technology Stack

### Backend
- **Framework:** Flask 2.3.3
- **Database:** PostgreSQL 15
- **ORM:** SQLAlchemy
- **Validation:** Flask-CORS, Flask-Limiter
- **Email:** SendGrid
- **Web Scraping:** BeautifulSoup4, Requests
- **Documentation:** Flasgger (Swagger/OpenAPI)
- **Containerization:** Docker & Docker Compose

### Frontend
- **Static:** HTML5, CSS3, JavaScript (vanilla)
- **Styling:** Custom CSS with dark theme
- **Hosting:** GitHub Pages / CDN
- **Analytics:** Google Analytics 4, Meta Pixel

## Quick Start

### Prerequisites
- Docker & Docker Compose
- PostgreSQL client (for backups)
- `.env` file with configuration

### Setup

1. **Clone and configure:**
   ```bash
   cp backend/.env.example backend/.env
   # Edit backend/.env with your actual values
   ```

2. **Build and run:**
   ```bash
   docker compose up --build
   ```

3. **Initialize database:**
   ```bash
   docker compose exec web flask db upgrade
   ```

4. **Access the application:**
   - Frontend: http://localhost:5000
   - API: http://localhost:5000/api
   - API Docs: http://localhost:5000/api/docs
   - Admin Dashboard: http://localhost:5000/admin/dashboard
     - Header: `X-Admin-Key: <ADMIN_API_KEY>`

## Environment Variables

Create a `.env` file in the `backend/` directory:

```env
# Database
DATABASE_URL=postgresql://devine:devine123@db:5432/devine
SECRET_KEY=your-secret-key-min-32-characters

# Email (SendGrid)
SENDGRID_API_KEY=SG.xxxxx
SENDGRID_FROM_EMAIL=noreply@devinedesignssa.com

# CORS
CORS_ORIGINS=http://localhost:5000,https://devinedesignssa.com

# Admin
ADMIN_API_KEY=admin-secret-key-change-in-production

# Analytics (Optional)
GA_TRACKING_ID=G-xxxxx
FB_PIXEL_ID=xxxxx
ANALYTICS_CONSENT=true
```

## API Endpoints

### Scorecard
- `POST /api/scorecards` - Generate website scorecard
  - Rate limited: 5 per hour per IP
  - Returns: score breakdown, lead info, recommendations

### Tracking
- `POST /api/track` - Track user events
  - Requires: lead_id, event_type
  - Optional: metadata

### Health
- `GET /health` - API health check
- `GET /ready` - Database readiness check

### Admin (requires `X-Admin-Key` header)
- `GET /admin/dashboard` - KPIs and metrics
- `GET /admin/leads` - List all leads (paginated)
- `GET /admin/leads/<id>` - Detailed lead info
- `GET /admin/analytics` - Lead analytics

### Static Files
- `GET /` - Serve index.html (frontend)
- `GET /images/*` - Serve images
- `GET /api/docs` - Swagger documentation

## Features

### Scoring Engine
The website scanner performs **25+ quality checks** across 4 categories:

1. **Technical** - HTTPS, mobile responsiveness, compression
2. **SEO** - Title, meta description, H1, canonical, OG tags, robots, sitemap
3. **Conversion** - CTAs, contact form, contact info, images, internal links
4. **Business** - Trust badges, testimonials, pricing, footer, social links, content

### Rate Limiting
- Default: 200 requests/day, 50/hour per IP
- Scorecard endpoint: 5/hour per IP
- Returns 429 on limit exceeded

### Admin Dashboard
- Real-time KPIs (total leads, scorecards, avg score, conversion rate)
- Lead management with filtering by stage
- Scorecard history per lead
- Analytics: stage distribution, score distribution, source tracking

### Security
- Private IP detection (prevents internal network scanning)
- URL validation and sanitization
- CORS origin whitelist
- Admin API key authentication
- Error handling with detailed logging

### Database Backup
Two backup options:

**Bash Script:**
```bash
./backend/scripts/backup_db.sh ./backups
```

**Python API:**
```python
from app.services.backup import DatabaseBackup

backup = DatabaseBackup(backup_dir='./backups')
backup.backup(db_host='db', db_user='devine', db_name='devine')
backup.cleanup_old_backups(retention_days=30)
backup.list_backups()
```

## Docker Commands

```bash
# Build images
docker compose build

# Start containers
docker compose up

# View logs
docker compose logs -f web

# Run migrations
docker compose exec web flask db upgrade

# Access database
docker compose exec db psql -U devine -d devine

# Stop all
docker compose down

# Remove volumes (deletes database)
docker compose down -v
```

## Deployment

### Production Checklist
- [ ] Change `SECRET_KEY` to a strong value (min 32 characters)
- [ ] Change `ADMIN_API_KEY` from default
- [ ] Set `SENDGRID_API_KEY` with valid key
- [ ] Whitelist CORS origins to your domain only
- [ ] Enable HTTPS (use reverse proxy like Nginx)
- [ ] Setup automated backups (cron job with `backup_db.sh`)
- [ ] Configure logging aggregation (e.g., CloudWatch, Datadog)
- [ ] Setup monitoring & alerts
- [ ] Use environment-specific `.env` files

### Docker Compose Production Config
Update `docker-compose.yml`:
```yaml
web:
  restart: always
  environment:
    - FLASK_ENV=production
    - DEBUG=false
  healthcheck:
    interval: 30s
    timeout: 10s
    retries: 3
```

## Development

### Local Setup (without Docker)
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r backend/requirements.txt

# Set environment variables
export DATABASE_URL="postgresql://localhost/devine"
export SECRET_KEY="dev-secret"

# Initialize database
cd backend
flask db upgrade

# Run development server
python run.py
```

### Database Migrations
```bash
# Create new migration
flask db migrate -m "Add column"

# Apply migration
flask db upgrade

# Revert migration
flask db downgrade
```

### Testing
```bash
# Run tests (TODO: add test suite)
pytest

# With coverage
pytest --cov=app
```

## Troubleshooting

### Port Already in Use
```bash
# Change port in docker-compose.yml
# Or kill existing process
lsof -i :5000
kill -9 <PID>
```

### Database Connection Error
```bash
# Check database health
docker compose exec db pg_isready

# Check logs
docker compose logs db

# Recreate database
docker compose down -v
docker compose up
```

### Rate Limit Issues
- Endpoints return 429 with `"error": "Rate limit exceeded"`
- Wait 1 hour or modify `RATELIMIT_STORAGE_URL` in production

### Email Not Sending
- Verify `SENDGRID_API_KEY` in `.env`
- Check SendGrid dashboard for bounced emails
- Review `docker logs` for SendGrid errors

## API Documentation

Interactive Swagger documentation available at:
```
http://localhost:5000/api/docs
```

## Contributing

1. Create a feature branch
2. Make changes
3. Test locally with `docker compose up`
4. Submit PR

## License

Proprietary - Devine Designs

## Support

Contact: info@devinedesignssa.com
