import stripe
from flask import Blueprint, render_template, session, current_app, url_for, redirect
from app.models import Product, Subscription, Payment, db

payments_bp = Blueprint("payments", __name__, url_prefix="/payments")


def compute_cart_total_and_items():
    """Calcula o total e os itens do carrinho."""
    cart = session.get("cart", {})
    items = []
    total = 0.0
    for pid_str, qty in cart.items():
        try:
            pid = int(pid_str)
        except ValueError:
            continue
        product = Product.query.get(pid)
        if product:
            subtotal = product.price * qty
            total += subtotal
            items.append({
                "id": product.id,
                "name": product.name,
                "price": product.price,
                "quantity": qty,
                "subtotal": subtotal
            })
    return round(total, 2), items


@payments_bp.route("/", methods=["GET"])
def payments_page():
    """Página inicial do checkout"""
    total, items = compute_cart_total_and_items()
    if total <= 0:
        return redirect(url_for("cart.view_cart"))

    return render_template(
        "payments.html",
        title="Checkout",
        total=total,
        items=items,
        stripe_public_key=current_app.config["STRIPE_PUBLIC_KEY"]
    )


@payments_bp.route("/create-checkout-session", methods=["POST"])
def create_checkout_session():
    """Cria sessão de pagamento segura no Stripe."""
    stripe.api_key = current_app.config["STRIPE_SECRET_KEY"]

    total, items = compute_cart_total_and_items()
    if total <= 0:
        return redirect(url_for("cart.view_cart"))

    # Convert total to cents(Stripe works with cents)
    amount_cents = int(total * 100)

    # Create Stripe checkout session
    checkout_session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            "price_data": {
                "currency": "usd",
                "product_data": {
                    "name": "Cart Purchase",
                },
                "unit_amount": amount_cents,
            },
            "quantity": 1,
        }],
        mode="payment",
        success_url=url_for("payments.success", _external=True),
        cancel_url=url_for("payments.cancel", _external=True),
    )

    return redirect(checkout_session.url, code=303)


@payments_bp.route("/success")
def success():
    """Handle successful payment and create subscriptions/payments."""
    cart = session.get("cart", {})
    user_data = session.get("user")

    if user_data:
        user_id = user_data["id"]
        # For each item in the cart create a subscription and payment record
        for pid_str, qty in cart.items():
            try:
                pid = int(pid_str)
            except ValueError:
                continue

            product = Product.query.get(pid)
            if not product:
                continue

            subscription = Subscription(user_id=user_id, product_id=product.id, status="active")
            db.session.add(subscription)
            db.session.flush()  # ensure subscription.id is available

            payment = Payment(subscription_id=subscription.id,
                              amount=product.price * qty,
                              status="success")
            db.session.add(payment)

        db.session.commit()
    session["cart"] = {}
    return render_template("payment_result.html",
                           message="Payment Successful!",
                           status="success",
                           color="green")

@payments_bp.route("/cancel")
def cancel():
    return render_template("payment_result.html",
                           message="Payment Canceled!",
                           status="failed",
                           color="red")
