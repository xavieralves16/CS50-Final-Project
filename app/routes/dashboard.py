from flask import Blueprint, jsonify, session, render_template
from app.models import User

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")

# Página HTML
@dashboard_bp.route("/", methods=["GET"])
def dashboard_page():
    return render_template("dashboard.html", title="Dashboard")

# Endpoint para fornecer dados em JSON
@dashboard_bp.route("/data", methods=["GET"])
def dashboard_data():
    if "user" not in session:
        return jsonify({"error": "not_logged_in"}), 401

    user_id = session["user"]["id"]
    user = User.query.get(user_id)

    if not user.subscriptions or len(user.subscriptions) == 0:
        return jsonify({"subscriptions": []}), 200

    subs_data = []
    for sub in user.subscriptions:
        subs_data.append({
            "id" : sub.id,
            "product": sub.product.name,
            "status": sub.status,
            "start_date": sub.start_date.strftime("%Y-%m-%d"),
        })

    return jsonify({"subscriptions": subs_data}), 200

