"""
Application factory and initialization module.

This module contains the Flask application factory and core configurations.
"""

from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_caching import Cache
from sqlalchemy.exc import SQLAlchemyError
import logging
from logging.handlers import RotatingFileHandler
import os

# Initialize extensions
db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()
cache = Cache(config={'CACHE_TYPE': 'simple'})


def create_app(config_name='development'):
    """
    Application factory function.
    
    Args:
        config_name: Configuration environment ('development', 'production', 'testing')
    
    Returns:
        Configured Flask application instance
    """
    app = Flask(__name__)
    
    # Load configuration. Accept either a preset name ('development', 'production')
    # or an explicit config object/class used by tests and other callers.
    from backend.config import config

    if isinstance(config_name, str):
        config_obj = config.get(config_name)
        if config_obj is None:
            config_obj = config.get('default')
        if config_obj is None:
            config_obj = next((value for value in config.values() if value is not None), None)
    else:
        config_obj = config_name

    app.config.from_object(config_obj)
    
    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    cache.init_app(app)
    
    # Enable CORS
    CORS(app, resources={
        r"/api/*": {
            "origins": app.config['CORS_ORIGINS'],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True
        }
    })
    
    # Register blueprints
    register_blueprints(app)
    
    # Setup error handlers
    setup_error_handlers(app)
    
    # Setup logging
    setup_logging(app)
    
    # CLI commands
    register_cli_commands(app)
    
    # Create tables when the database is reachable.
    # On Render, a misconfigured or unreachable DB host should not prevent the app
    # from starting so the health endpoint and fallback behavior remain available.
    with app.app_context():
        try:
            db.create_all()
            app.config['DB_AVAILABLE'] = True
        except SQLAlchemyError as exc:
            app.config['DB_AVAILABLE'] = False
            app.logger.warning('Database initialization skipped: %s', exc)
    
    return app


def register_blueprints(app):
    """Register all route blueprints."""
    from backend.app.routes import (
        auth_bp, chat_bp, assessment_bp, counselling_bp, 
        resources_bp, admin_bp
    )
    
    blueprints = [
        (auth_bp, '/api/auth'),
        (chat_bp, '/api/chat'),
        (assessment_bp, '/api/assessment'),
        (counselling_bp, '/api/counselling'),
        (resources_bp, '/api/resources'),
        (admin_bp, '/api/admin'),
    ]
    
    for blueprint, url_prefix in blueprints:
        app.register_blueprint(blueprint, url_prefix=url_prefix)


def setup_error_handlers(app):
    """Setup error handlers for the application."""
    from flask import jsonify
    
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({'error': 'Bad request', 'message': str(error)}), 400
    
    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({'error': 'Unauthorized', 'message': 'Authentication required'}), 401
    
    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({'error': 'Forbidden', 'message': 'Access denied'}), 403
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not found', 'message': 'Resource not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return jsonify({'error': 'Internal server error', 'message': 'An unexpected error occurred'}), 500


def setup_logging(app):
    """Setup logging configuration."""
    if not app.debug:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        
        file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240000, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        
        app.logger.setLevel(logging.INFO)
        app.logger.info('Talk to Me application startup')


def register_cli_commands(app):
    """Register CLI commands."""
    @app.cli.command()
    def init_db():
        """Initialize the database."""
        db.create_all()
        print('Database initialized.')
    
    @app.cli.command()
    def seed_db():
        """Seed the database with initial data."""
        from backend.app.utils.seed import seed_data
        seed_data()
        print('Database seeded.')
