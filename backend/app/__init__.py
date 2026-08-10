from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
import os
from dotenv import load_dotenv
from .limiter import limiter
from .errors import register_error_handlers
from .swagger import register_swagger

load_dotenv()

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__, static_folder='../frontend', static_url_path='/')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
    app.config['JSON_SORT_KEYS'] = False

    db.init_app(app)
    migrate.init_app(app, db)
    limiter.init_app(app)
    
    # CORS with origin whitelist
    allowed_origins = os.getenv('CORS_ORIGINS', 'http://localhost:3000,http://localhost:5000').split(',')
    CORS(app, resources={r"/api/*": {"origins": allowed_origins}})

    # Register error handlers
    register_error_handlers(app)

    # Register Swagger documentation
    register_swagger(app)

    # Register blueprints
    from .routes.scorecards import scorecards_bp
    from .routes.leads import leads_bp
    from .routes.track import track_bp
    from .routes.admin import admin_bp
    from .routes.health import health_bp

    app.register_blueprint(scorecards_bp, url_prefix='/api')
    app.register_blueprint(leads_bp, url_prefix='/api')
    app.register_blueprint(track_bp, url_prefix='/api')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(health_bp)

    return app
