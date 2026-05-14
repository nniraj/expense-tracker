from flask import Flask
from extensions import db, jwt, migrate

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Vedant%40065@localhost/expense_tracker'
    app.config['JWT_SECRET_KEY'] = 'secret'

    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    # import routes here (IMPORTANT: after db init)
    from routes.auth_routes import auth_bp
    from routes.expense_routes import expense_bp
    from routes.category_routes import category_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(expense_bp, url_prefix="/expenses")
    app.register_blueprint(category_bp, url_prefix="/categories")

    return app