"""Subscription routes exposing CRUD-style operations."""

from flask import Blueprint, request, jsonify, render_template, session
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
        "status": s.status
    } for s in subs])

@subscriptions_bp.route("/create", methods=["POST"])
def create_subscription():
    """Create a new subscription record."""
    data = request.get_json()
    new_sub = Subscription(
        user_id=data["user_id"],
        product_id=data["product_id"],
        status="active"
    )
    db.session.add(new_sub)
    db.session.commit()
    return jsonify({"message": "Subscription created successfully!"}), 201

@subscriptions_bp.route("/<int:sub_id>/cancel", methods=["POST"])
def cancel_subscription(sub_id):
    """Cancel a subscription owned by the logged-in user."""
    sub = Subscription.query.get_or_404(sub_id)

    if "user" not in session or session["user"]["id"] != sub.user_id:
        return jsonify({"error": "unauthorized"}), 403

    sub.status = "canceled"
    db.session.commit()
    return jsonify({"message": "Subscription canceled"}), 200
