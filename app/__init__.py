from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    """Factory function to create and configure the Flask app"""
    app = Flask(__name__)
    app.config.from_object("config.Config")

    # Initialize database and migrations
    db.init_app(app)
    migrate.init_app(app, db)

    # Import models so that Flask-Migrate knows them
    from app import models

    # Register blueprints (modular routes)
    from app.routes.auth import auth_bp
    from app.routes.products import products_bp
    from app.routes.subscriptions import subs_bp
    from app.routes.payments import payments_bp
    from app.routes.dashboard import dashboard_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(products_bp, url_prefix="/products")
    app.register_blueprint(subs_bp, url_prefix="/subscriptions")
    app.register_blueprint(payments_bp, url_prefix="/payments")
    app.register_blueprint(dashboard_bp, url_prefix="/dashboard")

    return app