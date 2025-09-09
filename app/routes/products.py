# app/routes/products.py
from flask import (
    Blueprint, request, jsonify, render_template,
    url_for, redirect, current_app
)
from werkzeug.utils import secure_filename
from app.models import db, Product
import os

products_bp = Blueprint("products", __name__, url_prefix="/products")

# Allowed image extensions for uploads
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}

def allowed_file(filename: str) -> bool:
    """Return True if filename has an allowed extension."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# ------------------------
# FRONTEND ROUTE
# ------------------------
@products_bp.route("/", methods=["GET"])
def products_page():
    """Render product list page (frontend bootstraps with JS)."""
    return render_template("index.html", title="Products")


# ------------------------
# API ROUTES
# ------------------------
@products_bp.route("/all", methods=["GET"])
def get_products():
    """
    Return all products as JSON (used by fetch in index.html).
    We convert image_path (stored in DB) into a public URL under /static using url_for.
    """
    products = Product.query.all()
    payload = []
    for p in products:
        image_url = url_for("static", filename=p.image_path) if getattr(p, "image_path", None) else None
        payload.append({
            "id": p.id,
            "name": p.name,
            "price": p.price,
            "description": p.description,
            "image_url": image_url,  # frontend expects image_url
        })
    return jsonify(payload)


@products_bp.route("/add", methods=["GET", "POST"])
def add_product():
    """
    Create a new product.
    - GET: render the HTML form
    - POST (multipart): read fields + optional image file; save file to UPLOAD_FOLDER; store relative path in DB.
    """
    if request.method == "POST":
        # Read basic fields
        name = (request.form.get("name") or "").strip()
        description = (request.form.get("description") or "").strip()
        price_raw = request.form.get("price") or "0"
        try:
            price = float(price_raw)
        except ValueError:
            price = 0.0

        # Handle optional image upload
        image_path = None
        file = request.files.get("image")  # <input type="file" name="image">
        if file and file.filename:
            if not allowed_file(file.filename):
                # 400 - bad request with a json error (can be improved to show in template)
                return jsonify({"message": "Invalid image type. Allowed: png, jpg, jpeg, gif, webp"}), 400
            filename = secure_filename(file.filename)
            # Build full path under the configured UPLOAD_FOLDER (set in app/__init__.py)
            save_dir = current_app.config["UPLOAD_FOLDER"]  # e.g., app/static/uploads
            os.makedirs(save_dir, exist_ok=True)
            save_path = os.path.join(save_dir, filename)
            file.save(save_path)
            # Store a path relative to /static so we can expose it via url_for('static', filename=...)
            image_path = f"uploads/{filename}"

        # Create product row
        new_product = Product(
            name=name,
            description=description,
            price=price,
            image_path=image_path  # path relative to /static
        )
        db.session.add(new_product)
        db.session.commit()

        # After creating, go back to the products page
        return redirect(url_for("products.products_page"))

    # GET → show the form page
    return render_template("add_product.html", title="Add Product")


@products_bp.route("/delete/<int:product_id>", methods=["POST"])
def delete_product(product_id):
    """
    Delete a product by ID.
    If the product has an uploaded image, remove it from disk as well (best effort).
    Returns JSON so the frontend can refresh the list without a full reload.
    """
    product = Product.query.get_or_404(product_id)

    # Attempt to remove the file from disk if present
    if getattr(product, "image_path", None):
        # Build absolute path from app root: app/static/<image_path>
        file_path = os.path.join(current_app.root_path, "static", product.image_path)
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except OSError:
                # Silent fail (you could log this)
                pass

    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": f"Product '{product.name}' deleted successfully"})
