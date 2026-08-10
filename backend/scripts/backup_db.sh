#!/bin/bash

# PostgreSQL Backup Script
# Usage: ./backup_db.sh [backup_dir]

set -e

BACKUP_DIR="${1:-.}"
DB_HOST="${DB_HOST:-db}"
DB_USER="${DB_USER:-devine}"
DB_NAME="${DB_NAME:-devine}"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/backup_${DB_NAME}_${TIMESTAMP}.sql.gz"
RETENTION_DAYS=30

# Create backup directory if it doesn't exist
mkdir -p "$BACKUP_DIR"

echo "Starting database backup..."
echo "Database: $DB_NAME"
echo "Host: $DB_HOST"
echo "Backup file: $BACKUP_FILE"

# Create the backup
pg_dump -h "$DB_HOST" -U "$DB_USER" "$DB_NAME" | gzip > "$BACKUP_FILE"

if [ $? -eq 0 ]; then
    FILE_SIZE=$(du -h "$BACKUP_FILE" | cut -f1)
    echo "✓ Backup completed successfully: $FILE_SIZE"
    
    # List recent backups
    echo ""
    echo "Recent backups:"
    ls -lh "$BACKUP_DIR"/backup_${DB_NAME}_*.sql.gz | tail -5
    
    # Cleanup old backups
    echo ""
    echo "Removing backups older than $RETENTION_DAYS days..."
    find "$BACKUP_DIR" -name "backup_${DB_NAME}_*.sql.gz" -mtime +$RETENTION_DAYS -delete
    echo "Cleanup completed"
else
    echo "✗ Backup failed"
    exit 1
fi
