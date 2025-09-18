"""Database models used throughout the application."""

from app import db
from datetime import datetime


class User(db.Model):
    """Represents an authenticated user of the platform."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_admin = db.Column(db.Boolean, default=False)   

    subscriptions = db.relationship("Subscription", backref="user", lazy=True)


class Product(db.Model):
    """Sellable subscription plan exposed to users."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)
    image_path = db.Column(db.String(255), nullable=True)

    subscriptions = db.relationship("Subscription", backref="product", lazy=True)


class Subscription(db.Model):
    """Association table linking users to the products they subscribe to."""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    status = db.Column(db.String(50), default="active")  
    start_date = db.Column(db.DateTime, default=datetime.utcnow)

    payments = db.relationship("Payment", backref="subscription", lazy=True)


class Payment(db.Model):
    """Individual charge associated with a subscription lifecycle."""
    id = db.Column(db.Integer, primary_key=True)
    subscription_id = db.Column(db.Integer, db.ForeignKey("subscription.id"), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), default="pending")  
