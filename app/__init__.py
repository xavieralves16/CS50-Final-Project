from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from .config import Config

db = SQLAlchemy()

def create_app():
    """Factory function to create and configure the Flask app"""
    app = Flask(__name__)
    app.config.from_object(Config)  # Use centralized config

    db.init_app(app)

    with app.app_context():
        # Import models and create tables if database doesn't exist
        from app import models
        db.create_all()
        print("Database and tables created!")

        # Import blueprints after database creation
        from app.routes.auth import auth_bp
        from app.routes.dashboard import dashboard_bp
        from app.routes.products import products_bp

        app.register_blueprint(auth_bp)
        app.register_blueprint(dashboard_bp)
        app.register_blueprint(products_bp)

        # Root route redirects to products page
        @app.route("/")
        def home():
            return redirect(url_for("products.products_page"))

    return app