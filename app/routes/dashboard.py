from flask import Blueprint, jsonify, render_template
from app.models import db, User, Product, Subscription

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")

# ------------------------
# FRONTEND ROUTE
# ------------------------
@dashboard_bp.route("/", methods=["GET"])
def dashboard_page():
    """Render dashboard page"""
    return render_template("dashboard.html", title="Dashboard")

# ------------------------
# API ROUTE
# ------------------------
@dashboard_bp.route("/stats", methods=["GET"])
def get_stats():
    """Return statistics as JSON (used by fetch in dashboard.html)"""
    users_count = User.query.count()
    products_count = Product.query.count()
    subs_count = Subscription.query.count()

    return jsonify({
        "users": users_count,
        "products": products_count,
        "subscriptions": subs_count
    })