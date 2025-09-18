"""Application factory and global objects for the CS50 final project."""

import os
from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from .config import Config
from werkzeug.security import generate_password_hash

# SQLAlchemy instance shared across the application. It is initialised
# with the Flask app inside ``create_app`` to keep the module import-safe.
db = SQLAlchemy()

def create_app():
    """Create, configure and return a fully initialised Flask application."""
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

        # Ensure that a deterministic administrator account exists so that
        # the back-office can be accessed immediately after deployment.
        admin = User.query.filter_by(email="admin@example.com").first()
        if not admin:
            admin = User(
                username="admin",
                email="admin@example.com",
                password=generate_password_hash("1234"),
                is_admin=True
            )
            db.session.add(admin)
            db.session.commit()
        
        elif not admin.password.startswith("pbkdf2:"):
            # Early data used plain-text passwords; migrate them lazily by
            # hashing on first run.
            admin.password = generate_password_hash("1234")
            db.session.commit()

        # Register blueprints once the database is ready so views can use the
        # models without risking premature imports.
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
            """Redirect the root URL to the public product catalogue."""
            return redirect(url_for("products.products_page"))

    return app