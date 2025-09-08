from flask import Blueprint, jsonify, request
from app import db
from app.models import Subscription

subs_bp = Blueprint("subscriptions", __name__)

@subs_bp.route("/", methods=["POST"])
def create_subscription():
    """Create a new subscription (dummy, without payment yet)"""
    data = request.json
    sub = Subscription(user_id=data["user_id"], product_id=data["product_id"])
    db.session.add(sub)
    db.session.commit()
    return jsonify({"message": "Subscription created"}), 201
