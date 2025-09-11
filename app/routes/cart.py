from flask import Blueprint, session, render_template, jsonify
from app.models import Product

cart_bp = Blueprint("cart", __name__, url_prefix="/cart")

@cart_bp.route("/", methods=["GET"])
def view_cart():
    cart = session.get("cart", {})
    items = []
    total = 0.0
    for pid_str, quantity in cart.items():
        product = Product.query.get(int(pid_str))
        if product:
            subtotal = product.price * quantity
            total += subtotal
            items.append({
                "id": product.id,
                "name": product.name,
                "price": product.price,
                "quantity": quantity,
                "subtotal": subtotal,
            })
    return render_template("cart.html", title="Your Cart", items=items, total=total)

@cart_bp.route("/add/<int:product_id>", methods=["POST"])
def add_to_cart(product_id):
    cart = session.get("cart", {})
    pid = str(product_id)
    cart[pid] = cart.get(pid, 0) + 1
    session["cart"] = cart
    return jsonify({"message": "Product added to cart", "cart": cart})

@cart_bp.route("/remove/<int:product_id>", methods=["POST"])
def remove_from_cart(product_id):
    cart = session.get("cart", {})
    pid = str(product_id)
    if pid in cart:
        cart[pid] -= 1
        if cart[pid] <= 0:
            del cart[pid]
        session["cart"] = cart
    return jsonify({"message": "Product removed", "cart": cart})

@cart_bp.route("/clear", methods=["POST"])
def clear_cart():
    session["cart"] = {}
    return jsonify({"message": "Cart cleared"})