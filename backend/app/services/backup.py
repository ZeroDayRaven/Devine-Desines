import os
import subprocess
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class DatabaseBackup:
    """Handle database backups and restoration."""
    
    def __init__(self, backup_dir='./backups'):
        self.backup_dir = backup_dir
        os.makedirs(backup_dir, exist_ok=True)

    def backup(self, db_host='localhost', db_user='devine', db_name='devine'):
        """Create a compressed database backup."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = os.path.join(self.backup_dir, f'backup_{db_name}_{timestamp}.sql.gz')
        
        try:
            cmd = f'pg_dump -h {db_host} -U {db_user} {db_name} | gzip > {backup_file}'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode != 0:
                raise Exception(f"Backup failed: {result.stderr}")
            
            file_size = os.path.getsize(backup_file) / (1024 * 1024)  # MB
            logger.info(f"Backup created: {backup_file} ({file_size:.2f} MB)")
            return backup_file
        except Exception as e:
            logger.error(f"Backup error: {e}")
            raise

    def restore(self, backup_file, db_host='localhost', db_user='devine', db_name='devine', db_password=''):
        """Restore database from backup."""
        try:
            env = os.environ.copy()
            if db_password:
                env['PGPASSWORD'] = db_password
            
            # Drop and recreate database
            drop_cmd = f'dropdb -h {db_host} -U {db_user} {db_name}'
            create_cmd = f'createdb -h {db_host} -U {db_user} {db_name}'
            
            subprocess.run(drop_cmd, shell=True, env=env, capture_output=True)
            subprocess.run(create_cmd, shell=True, env=env, capture_output=True, check=True)
            
            # Restore from backup
            if backup_file.endswith('.gz'):
                restore_cmd = f'gunzip -c {backup_file} | psql -h {db_host} -U {db_user} {db_name}'
            else:
                restore_cmd = f'psql -h {db_host} -U {db_user} {db_name} < {backup_file}'
            
            result = subprocess.run(restore_cmd, shell=True, env=env, capture_output=True, text=True)
            
            if result.returncode != 0:
                raise Exception(f"Restore failed: {result.stderr}")
            
            logger.info(f"Database restored from {backup_file}")
            return True
        except Exception as e:
            logger.error(f"Restore error: {e}")
            raise

    def cleanup_old_backups(self, retention_days=30):
        """Delete backups older than retention period."""
        cutoff_time = datetime.now() - timedelta(days=retention_days)
        deleted_count = 0
        
        try:
            for filename in os.listdir(self.backup_dir):
                filepath = os.path.join(self.backup_dir, filename)
                if os.path.isfile(filepath):
                    file_time = datetime.fromtimestamp(os.path.getmtime(filepath))
                    if file_time < cutoff_time:
                        os.remove(filepath)
                        deleted_count += 1
                        logger.info(f"Deleted old backup: {filename}")
            
            logger.info(f"Cleanup completed: {deleted_count} backups deleted")
            return deleted_count
        except Exception as e:
            logger.error(f"Cleanup error: {e}")
            raise

    def list_backups(self):
        """List all available backups."""
        try:
            backups = []
            for filename in sorted(os.listdir(self.backup_dir), reverse=True):
                filepath = os.path.join(self.backup_dir, filename)
                if os.path.isfile(filepath):
                    file_size = os.path.getsize(filepath) / (1024 * 1024)  # MB
                    file_time = datetime.fromtimestamp(os.path.getmtime(filepath))
                    backups.append({
                        'filename': filename,
                        'size_mb': round(file_size, 2),
                        'created': file_time.isoformat()
                    })
            return backups
        except Exception as e:
            logger.error(f"List backups error: {e}")
            raise
