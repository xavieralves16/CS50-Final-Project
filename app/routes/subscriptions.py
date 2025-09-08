from flask import Blueprint, request, jsonify, render_template
from app.models import db, Subscription, Product, User

subscriptions_bp = Blueprint("subscriptions", __name__, url_prefix="/subscriptions")

# ------------------------
# FRONTEND ROUTE
# ------------------------
@subscriptions_bp.route("/", methods=["GET"])
def subscriptions_page():
    """Render subscriptions page"""
    return render_template("subscriptions.html", title="Subscriptions")

# ------------------------
# API ROUTES
# ------------------------
@subscriptions_bp.route("/all", methods=["GET"])
def get_subscriptions():
    """Return all subscriptions as JSON"""
    subs = Subscription.query.all()
    return jsonify([{
        "id": s.id,
        "user_id": s.user_id,
        "product_id": s.product_id,
        "start_date": s.start_date.isoformat(),
        "active": s.active
    } for s in subs])

@subscriptions_bp.route("/create", methods=["POST"])
def create_subscription():
    """Create new subscription (from frontend or API)"""
    data = request.get_json()
    new_sub = Subscription(
        user_id=data["user_id"],
        product_id=data["product_id"],
        active=True
    )
    db.session.add(new_sub)
    db.session.commit()
    return jsonify({"message": "Subscription created successfully!"}), 201
