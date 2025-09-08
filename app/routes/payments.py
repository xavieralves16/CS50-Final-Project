from flask import Blueprint, jsonify
# Stripe integration will be added later
payments_bp = Blueprint("payments", __name__)

@payments_bp.route("/", methods=["GET"])
def get_payments():
    """Placeholder route for payments"""
    return jsonify({"message": "Payments endpoint (to be implemented)"})
