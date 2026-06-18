from flask import Flask, jsonify, request
from flask_cors import CORS

from models import (
    get_users,
    get_user_by_id,
    add_user,
    update_user,
    delete_user,
    get_user_by_email
)

from utils.validators import is_valid_email

# 👇 ADD THIS (Blueprint import)
from routes.users import users_bp

app = Flask(__name__)
CORS(app)

# =========================
# REGISTER BLUEPRINT (ADDED)
# =========================
app.register_blueprint(users_bp)

# 🟢 Home route
@app.route("/")
def home():
    return jsonify({"message": "Server is running"})


# 🟢 Get all users
@app.route("/users", methods=["GET"])
def users():
    try:
        users = get_users()

        return jsonify([
            {"id": u["id"], "name": u["name"], "email": u["email"]}
            for u in users
        ])
    except Exception as e:
        return jsonify({"error": "Failed to fetch users"}), 500


# 🟢 Get user by ID
@app.route("/users/<int:user_id>", methods=["GET"])
def user_detail(user_id):

    try:
        user = get_user_by_id(user_id)

        if user is None:
            return jsonify({"error": "User not found"}), 404

        return jsonify({
            "id": user["id"],
            "name": user["name"],
            "email": user["email"]
        })

    except Exception:
        return jsonify({"error": "Server error"}), 500


# 🟢 Create user (POST)
@app.route("/users", methods=["POST"])
def create_user():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "JSON data required"}), 400

        name = data.get("name", "").strip()
        email = data.get("email", "").strip().lower()

        if not name or not email:
            return jsonify({"error": "Name and email required"}), 400

        if not is_valid_email(email):
            return jsonify({"error": "Invalid email format"}), 400

        existing_user = get_user_by_email(email)
        if existing_user:
            return jsonify({"error": "Email already exists"}), 400

        add_user(name, email)

        return jsonify({"message": "User created successfully"}), 201

    except Exception:
        return jsonify({"error": "Failed to create user"}), 500


# 🟢 Update user (PUT)
@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user_route(user_id):

    try:
        user = get_user_by_id(user_id)
        if user is None:
            return jsonify({"error": "User not found"}), 404

        data = request.get_json()

        if not data:
            return jsonify({"error": "JSON data required"}), 400

        name = data.get("name", "").strip()
        email = data.get("email", "").strip().lower()

        if not name or not email:
            return jsonify({"error": "Name and email required"}), 400

        if not is_valid_email(email):
            return jsonify({"error": "Invalid email format"}), 400

        existing_user = get_user_by_email(email)
        if existing_user and existing_user["id"] != user_id:
            return jsonify({"error": "Email already exists"}), 400

        update_user(user_id, name, email)

        return jsonify({"message": "User updated successfully"})

    except Exception:
        return jsonify({"error": "Failed to update user"}), 500


# 🟢 Delete user (DELETE)
@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user_route(user_id):

    try:
        user = get_user_by_id(user_id)

        if user is None:
            return jsonify({"error": "User not found"}), 404

        delete_user(user_id)

        return jsonify({"message": "User deleted successfully"})

    except Exception:
        return jsonify({"error": "Failed to delete user"}), 500


if __name__ == "__main__":
    app.run(debug=True)