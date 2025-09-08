from flask import Blueprint, jsonify
from app.models import Product

products_bp = Blueprint("products", __name__)

@products_bp.route("/", methods=["GET"])
def list_products():
    """List all available products"""
    products = Product.query.all()
    return jsonify([{"id": p.id, "name": p.name, "price": p.price} for p in products])
