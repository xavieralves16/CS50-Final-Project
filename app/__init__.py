from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from .config import Config
import os

db = SQLAlchemy()

def create_app():
    """Factory function to create and configure the Flask app"""
    app = Flask(__name__)
    app.config.from_object(Config)  # Use centralized config

    # --------------------------
    # Upload folder configuration
    # --------------------------
    app.config["UPLOAD_FOLDER"] = os.path.join(app.root_path, "static", "uploads")
    app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024  # 5 MB
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    # --------------------------
    # Initialize database
    # --------------------------
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