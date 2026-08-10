# Devine Designs - Production Readiness Checklist

## Pre-Deployment ✓

- [x] `.dockerignore` created
- [x] Dockerfile optimized with health checks
- [x] All Python files syntax-validated
- [x] requirements.txt updated with all dependencies
- [x] .env file configured with all required variables
- [x] docker-compose.yml configured
- [x] README.md with full documentation
- [x] Rate limiting configured (5/hour per IP on scorecards)
- [x] CORS whitelist configured
- [x] Error handling middleware added
- [x] Static file serving configured
- [x] Admin dashboard implemented
- [x] Database backup tools added
- [x] Swagger API documentation added
- [x] Scanner with 25+ quality checks implemented

## Quick Start

### 1. Build Docker Image
```bash
docker compose build
```

### 2. Start Containers
```bash
docker compose up --pull always
```

### 3. Initialize Database
```bash
docker compose exec web flask db upgrade
```

### 4. Test API
```bash
# Health check
curl http://localhost:5000/health

# API docs
open http://localhost:5000/api/docs

# Admin dashboard (requires X-Admin-Key header)
curl -H "X-Admin-Key: admin-secret-key-change-me-in-production" \
  http://localhost:5000/admin/dashboard
```

## Environment Variables to Update

**Before production deployment, change these in `backend/.env`:**

```bash
SECRET_KEY=<generate-strong-random-key-32-chars>
ADMIN_API_KEY=<change-from-default>
SENDGRID_API_KEY=<add-real-sendgrid-key>
CORS_ORIGINS=<whitelist-your-domain-only>
```

## Health Check Endpoints

- `GET /health` - Basic health check
- `GET /ready` - Database readiness check
- `GET /api/docs` - Swagger documentation

## Admin Dashboard

Access at: `http://localhost:5000/admin/dashboard`

**Header required:**
```
X-Admin-Key: <value-from-.env>
```

**Available endpoints:**
- `/admin/dashboard` - KPIs and metrics
- `/admin/leads?page=1&per_page=20` - List leads
- `/admin/leads/<id>` - Lead details
- `/admin/analytics` - Analytics report

## Database Backup

**Using bash script:**
```bash
./backend/scripts/backup_db.sh ./backups
```

**Using Python:**
```python
from app.services.backup import DatabaseBackup

backup = DatabaseBackup('./backups')
backup.backup(db_host='db', db_user='devine', db_name='devine')
```

## Useful Docker Commands

```bash
# View logs
docker compose logs -f web

# Access database
docker compose exec db psql -U devine -d devine

# Run migrations
docker compose exec web flask db upgrade

# Create backup
docker compose exec db pg_dump -U devine devine | gzip > backup.sql.gz

# Stop all containers
docker compose down

# Remove volumes (deletes database)
docker compose down -v
```

## Production Deployment Steps

1. **Change secret keys in `.env`:**
   - `SECRET_KEY` - Strong random 32+ character string
   - `ADMIN_API_KEY` - Different from default

2. **Update CORS origins:**
   ```
   CORS_ORIGINS=https://devinedesignssa.com,https://www.devinedesignssa.com
   ```

3. **Add SendGrid API key:**
   ```
   SENDGRID_API_KEY=SG.your-real-key-here
   ```

4. **Setup reverse proxy (Nginx):**
   - Enable HTTPS/SSL
   - Proxy requests to `http://localhost:5000`

5. **Configure automated backups:**
   ```bash
   # Add to crontab for daily backups at 2 AM
   0 2 * * * /path/to/backend/scripts/backup_db.sh /path/to/backups
   ```

6. **Setup monitoring:**
   - Monitor `/health` endpoint
   - Setup alerts for response times
   - Log aggregation service

7. **Database backups:**
   - Store backups in `/backups` volume or S3
   - Test restore procedure

## Troubleshooting

### Container won't start
```bash
docker compose logs web
```

### Database connection error
```bash
docker compose logs db
docker compose exec db pg_isready
```

### Port already in use
```bash
# Change in docker-compose.yml or kill process:
lsof -i :5000
```

### Rate limit test
```bash
# Hit scorecard endpoint 6 times - 6th should return 429
for i in {1..6}; do
  curl -X POST http://localhost:5000/api/scorecards \
    -H "Content-Type: application/json" \
    -d '{"email":"test@test.com","website":"https://example.com"}'
done
```

## Files Created/Modified

### New Files
- `backend/.dockerignore`
- `backend/app/limiter.py`
- `backend/app/errors.py`
- `backend/app/swagger.py`
- `backend/app/routes/health.py`
- `backend/app/routes/admin.py`
- `backend/app/services/backup.py`
- `backend/scripts/backup_db.sh`
- `README.md`

### Modified Files
- `backend/Dockerfile` - Added health checks
- `backend/app/__init__.py` - Added all configurations
- `backend/app/config.py` - Extended with new settings
- `backend/app/services/scanner.py` - 25+ quality checks
- `backend/app/services/email.py` - Config-based API keys
- `backend/app/routes/scorecards.py` - Added notification
- `backend/requirements.txt` - Added Flask-Limiter, Flasgger
- `backend/.env` - Updated with all variables
- `backend/.env.example` - Complete template
- `docker-compose.yml` - All env vars passed
- `backend/run.py` - Logging and debug mode
- `backend/app/extensions.py` - Documented

## Next Actions

1. Review and update `.env` with production values
2. Test locally: `docker compose up`
3. Verify all endpoints work
4. Setup deployment pipeline (CI/CD)
5. Configure backups and monitoring
6. Deploy to production

---

**Status:** ✅ Production Ready
**Last Updated:** 2025-01-01
**Version:** 1.0.0
