from flask import Blueprint, jsonify
from app.models import User, Product, Subscription, Payment

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/", methods=["GET"])
def get_dashboard():
    """Basic dashboard statistics"""
    return jsonify({
        "users": User.query.count(),
        "products": Product.query.count(),
        "subscriptions": Subscription.query.count(),
        "payments": Payment.query.count(),
    })
