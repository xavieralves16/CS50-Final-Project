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

@products_bp.route("/add", methods=["GET", "POST"])
def add_product():
    """Add a new product"""
    if request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")
        price = request.form.get("price")
        image_url = request.form.get("image_url")

        new_product = Product(name=name, description=description, price=float(price), image_url=image_url)
        db.session.add(new_product)
        db.session.commit()

        return render_template("add_product.html", title="Add Product", success=True)

    return render_template("add_product.html", title="Add Product")

@products_bp.route("/delete/<int:product_id>", methods=["POST"])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": f"Product {product.name} deleted successfully"})