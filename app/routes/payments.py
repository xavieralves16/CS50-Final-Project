from flask import Blueprint, request, jsonify, render_template
from app.models import db, Payment

payments_bp = Blueprint("payments", __name__, url_prefix="/payments")

# ------------------------
# FRONTEND ROUTE
# ------------------------
@payments_bp.route("/", methods=["GET"])
def payments_page():
    """Render payments page"""
    return render_template("payments.html", title="Payments")

# ------------------------
# API ROUTES
# ------------------------
@payments_bp.route("/all", methods=["GET"])
def get_payments():
    """Return all payments as JSON"""
    payments = Payment.query.all()
    return jsonify([{
        "id": p.id,
        "user_id": p.user_id,
        "amount": p.amount,
        "status": p.status,
        "created_at": p.created_at.isoformat()
    } for p in payments])