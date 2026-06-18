from flask import Blueprint, jsonify, request

from backend.models import (
    get_users,
    get_user_by_id,
    add_user,
    update_user,
    delete_user
)

from utils.validators import validate_contact_form

# =========================
# USERS ROUTE GROUP
# =========================
users_bp = Blueprint("users", __name__)


# 🟢 Home test route
@users_bp.route("/")
def home():
    return jsonify({
        "message": "User routes working!"
    })


# 🟢 Get all users
@users_bp.route("/users", methods=["GET"])
def get_users_route():

    users = get_users()

    return jsonify([
        {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"]
        }
        for user in users
    ])


# 🟢 Get user by ID
@users_bp.route("/users/<int:user_id>", methods=["GET"])
def get_user_route(user_id):

    user = get_user_by_id(user_id)

    if not user:
        return jsonify({
            "error": "User not found"
        }), 404

    return jsonify({
        "id": user["id"],
        "name": user["name"],
        "email": user["email"]
    })


# 🟢 Create user
@users_bp.route("/users", methods=["POST"])
def create_user():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "JSON data required"
        }), 400

    name = data.get("name", "").strip()
    email = data.get("email", "").strip().lower()

    if not name or not email:
        return jsonify({
            "error": "Name and email required"
        }), 400

    add_user(name, email)

    return jsonify({
        "message": "User created successfully"
    }), 201


# 🟡 Update user
@users_bp.route("/users/<int:user_id>", methods=["PUT"])
def update_user_route(user_id):

    user = get_user_by_id(user_id)

    if not user:
        return jsonify({
            "error": "User not found"
        }), 404

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "JSON data required"
        }), 400

    name = data.get("name", "").strip()
    email = data.get("email", "").strip().lower()

    if not name or not email:
        return jsonify({
            "error": "Name and email required"
        }), 400

    update_user(user_id, name, email)

    return jsonify({
        "message": "User updated successfully"
    })


# 🔴 Delete user
@users_bp.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user_route(user_id):

    user = get_user_by_id(user_id)

    if not user:
        return jsonify({
            "error": "User not found"
        }), 404

    delete_user(user_id)

    return jsonify({
        "message": "User deleted successfully"
    })


# 🟢 Contact form validation example
@users_bp.route("/contact", methods=["POST"])
def contact():

    data = request.get_json()

    result = validate_contact_form(data)

    if not result["valid"]:
        return jsonify({
            "success": False,
            "errors": result["errors"]
        }), 400

    return jsonify({
        "success": True,
        "message": "Contact form validated successfully"
    }), 200