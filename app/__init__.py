import os
from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from .config import Config


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
        from app.models import User   # <-- import User model here
        db.create_all()

        # ✅ Ensure default admin exists
        if not User.query.filter_by(email="admin@example.com").first():
            admin = User(
                username="admin",
                email="admin@example.com",
                password="1234",   # ⚠️ TODO: add password hashing later
                is_admin=True
            )
            db.session.add(admin)
            db.session.commit()

        # Import blueprints after database creation
        from app.routes.auth import auth_bp
        from app.routes.dashboard import dashboard_bp
        from app.routes.products import products_bp
        from app.routes.cart import cart_bp
        from app.routes.payments import payments_bp
        from app.routes.subscriptions import subscriptions_bp

        app.register_blueprint(auth_bp)
        app.register_blueprint(dashboard_bp)
        app.register_blueprint(products_bp)
        app.register_blueprint(cart_bp)
        app.register_blueprint(payments_bp)
        app.register_blueprint(subscriptions_bp)

        # Root route redirects to products page
        @app.route("/")
        def home():
            return redirect(url_for("products.products_page"))

    return app