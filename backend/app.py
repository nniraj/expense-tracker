from flask import Flask, jsonify, request
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
    
    # Configure CORS - Allow all origins since we're using proxy during development
    CORS(app, supports_credentials=False)

    # Handle OPTIONS requests globally to prevent redirects
    @app.before_request
    def handle_preflight():
        """Handle CORS preflight requests globally before any route processing."""
        if request.method == 'OPTIONS':
            return '', 204

    # Ensure all responses have correct JSON headers
    @app.after_request
    def set_json_headers(response):
        """Ensure JSON responses have correct Content-Type."""
        if response.content_type is None or 'json' in response.content_type.lower():
            response.headers['Content-Type'] = 'application/json'
        return response

    # JWT error handlers
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({
            "msg": "The token has expired"
        }), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({
            "msg": "Signature verification failed"
        }), 401

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({
            "msg": "Request does not contain an access token"
        }), 401
    
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