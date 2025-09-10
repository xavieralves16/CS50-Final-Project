from flask import Blueprint, request, jsonify, render_template, redirect, url_for, session
from app.models import db, User

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

# ------------------------
# FRONTEND ROUTES
# ------------------------
@auth_bp.route("/login", methods=["GET"])
def login_page():
    """Render login page"""
    return render_template("login.html", title="Login")

@auth_bp.route("/register", methods=["GET"])
def register_page():
    """Render register page"""
    return render_template("register.html", title="Register")

# ------------------------
# API ROUTES
# ------------------------
@auth_bp.route("/login", methods=["POST"])
def login():
    """API endpoint for login"""
    data = request.get_json()
    user = User.query.filter_by(email=data["email"]).first()

    if user and user.password == data["password"]:  # ⚠️ sem hashing por enquanto
        # guardar utilizador na sessão (inclui is_admin)
        session["user"] = {
            "id": user.id,
            "name": user.username,
            "email": user.email,
            "is_admin": user.is_admin
        }
        return jsonify({"message": "Login successful!"}), 200
    
    return jsonify({"error": "Invalid credentials"}), 401

@auth_bp.route("/logout", methods=["GET"])
def logout():
    """Logout user and clear session"""
    session.pop("user", None)
    return redirect(url_for("auth.login_page"))

@auth_bp.route("/register", methods=["POST"])
def register():
    """API endpoint for register"""
    data = request.get_json()
    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "Email already registered"}), 400

    new_user = User(
        username=data["username"],
        email=data["email"],
        password=data["password"],  # ⚠️ mais tarde: fazer hashing
        is_admin=False              # nunca cria admins via formulário
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully!"}), 201