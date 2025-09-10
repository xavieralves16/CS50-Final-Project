from flask import Blueprint, request, jsonify, render_template, redirect, url_for, session, flash
from app.models import db, Product
import os
from werkzeug.utils import secure_filename

products_bp = Blueprint("products", __name__, url_prefix="/products")

# ------------------------
# FRONTEND ROUTES
# ------------------------
@products_bp.route("/", methods=["GET"])
def products_page():
    """Render index page with products list"""
    return render_template(
        "index.html",
        title="Products",
        is_admin=session.get("user", {}).get("is_admin", False)  # <-- flag para Jinja/JS
    )

@products_bp.route("/add", methods=["GET", "POST"])
def add_product():
    """Page + form handler to add a new product (only for admins)"""
    if not session.get("user") or not session["user"].get("is_admin"):
        flash("Unauthorized access – only admins can add products.", "error")
        return redirect(url_for("products.products_page"))

    if request.method == "POST":
        name = request.form["name"]
        price = request.form["price"]
        description = request.form.get("description")
        image_file = request.files.get("image")

        image_path = None
        if image_file:
            filename = secure_filename(image_file.filename)
            upload_folder = os.path.join("app", "static", "uploads")
            os.makedirs(upload_folder, exist_ok=True)
            file_path = os.path.join(upload_folder, filename)
            image_file.save(file_path)
            image_path = f"/static/uploads/{filename}"

        new_product = Product(
            name=name,
            price=price,
            description=description,
            image_path=image_path
        )
        db.session.add(new_product)
        db.session.commit()
        flash("Product added successfully!", "success")
        return redirect(url_for("products.products_page"))

    return render_template("add_product.html", title="Add Product")

# ------------------------
# API ROUTES
# ------------------------
@products_bp.route("/all", methods=["GET"])
def get_all_products():
    """Return all products as JSON"""
    products = Product.query.all()
    data = []
    for p in products:
        data.append({
            "id": p.id,
            "name": p.name,
            "price": p.price,
            "description": p.description,
            "image_url": p.image_path
        })
    return jsonify(data)

@products_bp.route("/delete/<int:product_id>", methods=["POST"])
def delete_product(product_id):
    """Delete a product (only for admins)"""
    if not session.get("user") or not session["user"].get("is_admin"):
        return jsonify({"error": "Unauthorized"}), 403

    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": f"Product '{product.name}' deleted successfully!"})

