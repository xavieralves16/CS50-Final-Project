from flask import Blueprint, request, jsonify, render_template
from app.models import db, Product

products_bp = Blueprint("products", __name__, url_prefix="/products")

# ------------------------
# FRONTEND ROUTE
# ------------------------
@products_bp.route("/", methods=["GET"])
def products_page():
    """Render product list page"""
    return render_template("index.html", title="Products")

# ------------------------
# API ROUTES
# ------------------------
@products_bp.route("/all", methods=["GET"])
def get_products():
    """Return all products as JSON (used by fetch in index.html)"""
    products = Product.query.all()
    return jsonify([{
        "id": p.id,
        "name": p.name,
        "price": p.price,
        "description": p.description
    } for p in products])