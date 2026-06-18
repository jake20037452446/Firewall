from flask import Blueprint, request, jsonify
from utils.validators import validate_name, validate_email, validate_phone

# Create a route group (Blueprint)
users_bp = Blueprint("users", __name__)


# ================================
# GET ALL USERS (placeholder)
# ================================
@users_bp.route("/users", methods=["GET"])
def get_users():
    """
    Normally pulls users from database.
    Right now returns example data.
    """

    users = [
        {
            "id": 1,
            "name": "Demo User",
            "email": "demo@email.com"
        }
    ]

    return jsonify({
        "success": True,
        "users": users
    })


# ================================
# CREATE USER (basic example)
# ================================
@users_bp.route("/users", methods=["POST"])
def create_user():
    """
    Accepts JSON:
    {
        "name": "",
        "email": "",
        "phone": ""
    }
    """

    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    phone = data.get("phone")

    # ============================
    # VALIDATION (important part)
    # ============================
    if not validate_name(name):
        return jsonify({"success": False, "error": "Invalid name"}), 400

    if not validate_email(email):
        return jsonify({"success": False, "error": "Invalid email"}), 400

    if not validate_phone(phone):
        return jsonify({"success": False, "error": "Invalid phone"}), 400

    # ============================
    # SIMULATED DATABASE SAVE
    # ============================
    new_user = {
        "id": 2,
        "name": name,
        "email": email,
        "phone": phone
    }

    return jsonify({
        "success": True,
        "message": "User created successfully",
        "user": new_user
    }), 201