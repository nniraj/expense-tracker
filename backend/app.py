from flask import Flask
from flask_cors import CORS
from config import Config
from extensions import db, jwt, migrate


def create_app(config_class=Config):
    """Create and configure the Flask application.
    
    Args:
        config_class: Configuration class to use (default: Config)
        
    Returns:
        Flask application instance
    """
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    CORS(app)
    
    # Register blueprints
    _register_blueprints(app)
    
    return app


def _register_blueprints(app):
    """Register all application blueprints."""
    from routes.auth_routes import auth_bp
    from routes.expense_routes import expense_bp
    from routes.category_routes import category_bp
    from routes.test_routes import test_bp
    
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(expense_bp, url_prefix="/api/expenses")
    app.register_blueprint(category_bp, url_prefix="/api/categories")
    app.register_blueprint(test_bp, url_prefix="/api/test")