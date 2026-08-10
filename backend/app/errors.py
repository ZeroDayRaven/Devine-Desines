from flask import request, jsonify
import logging
from functools import wraps
from werkzeug.exceptions import HTTPException

logger = logging.getLogger(__name__)

class APIError(Exception):
    """Custom API Error."""
    def __init__(self, message, status_code=400, payload=None):
        super().__init__()
        self.message = message
        self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['error'] = self.message
        return rv

def register_error_handlers(app):
    """Register global error handlers."""
    
    @app.errorhandler(APIError)
    def handle_api_error(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    @app.errorhandler(400)
    def handle_bad_request(error):
        return jsonify({'error': 'Bad request'}), 400

    @app.errorhandler(404)
    def handle_not_found(error):
        return jsonify({'error': 'Resource not found'}), 404

    @app.errorhandler(405)
    def handle_method_not_allowed(error):
        return jsonify({'error': 'Method not allowed'}), 405

    @app.errorhandler(429)
    def handle_rate_limit(error):
        return jsonify({'error': 'Rate limit exceeded. Too many requests.'}), 429

    @app.errorhandler(500)
    def handle_internal_error(error):
        logger.error(f"Internal server error: {error}")
        return jsonify({'error': 'Internal server error'}), 500

    @app.errorhandler(Exception)
    def handle_unexpected_error(error):
        logger.error(f"Unexpected error: {error}", exc_info=True)
        if isinstance(error, HTTPException):
            return jsonify({'error': error.description}), error.code
        return jsonify({'error': 'An unexpected error occurred'}), 500

def handle_request_errors(f):
    """Decorator to handle common request validation errors."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            # Validate JSON content type for POST/PUT
            if request.method in ['POST', 'PUT']:
                if not request.is_json:
                    return jsonify({'error': 'Content-Type must be application/json'}), 400
            
            return f(*args, **kwargs)
        except Exception as e:
            logger.error(f"Request error in {f.__name__}: {e}", exc_info=True)
            return jsonify({'error': 'Request processing failed'}), 400
    return decorated_function
