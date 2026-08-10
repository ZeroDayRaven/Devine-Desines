from flask import Blueprint, send_from_directory, current_app
from sqlalchemy import text
import os

health_bp = Blueprint('health', __name__)

@health_bp.route('/health')
def health_check():
    """Health check endpoint for Docker."""
    return {'status': 'healthy'}, 200

@health_bp.route('/ready')
def readiness_check():
    """Readiness check - database connectivity."""
    try:
        from .. import db
        db.session.execute(text('SELECT 1'))
        return {'status': 'ready'}, 200
    except Exception as e:
        return {'status': 'not ready', 'error': str(e)}, 503

@health_bp.route('/')
def serve_index():
    """Serve index.html for frontend."""
    static_folder = current_app.static_folder
    if os.path.exists(os.path.join(static_folder, 'index.html')):
        return send_from_directory(static_folder, 'index.html')
    return {'message': 'Devine Designs API'}, 200

@health_bp.route('/<path:path>')
def serve_static(path):
    """Serve static files (CSS, JS, images)."""
    static_folder = current_app.static_folder
    file_path = os.path.join(static_folder, path)
    
    if os.path.exists(file_path):
        if os.path.isdir(file_path):
            return send_from_directory(static_folder, path + '/index.html')
        return send_from_directory(static_folder, path)
    
    # Fallback to index.html for SPA routing
    if os.path.exists(os.path.join(static_folder, 'index.html')):
        return send_from_directory(static_folder, 'index.html')
    
    return {'error': 'Not found'}, 404
