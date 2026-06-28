from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    jwt_required,
    get_jwt_identity
)
import bcrypt
import datetime

from models import (
    get_users,
    get_user_by_id,
    add_user,
    get_user_by_email
)

app = Flask(__name__)

# 
#  CORE SECURITY CONFIG
#

app.config["JWT_SECRET_KEY"] = "CHANGE_THIS_TO_A_STRONG_SECRET_KEY"
jwt = JWTManager(app)

# Rate limiting (anti spam)
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["60 per minute"]
)

# Locked CORS (CHANGE THIS in production)
CORS(app, origins=["http://localhost:3000"])

# 
#  SIMPLE AUDIT LOG
# 
def log_event(event):
    print(f"[AUDIT] {datetime.datetime.now()} - {event}")


# 
#  HOME
# 
@app.route("/")
def home():
    return jsonify({"message": "Secure server running"})


# 
#  REGISTER (bcrypt)
# 
@app.route("/register", methods=["POST"])
@limiter.limit("10 per minute")
def register():
    data = request.get_json()

    name = data.get("name", "").strip()
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not name or not email or not password:
        return jsonify({"error": "Missing fields"}), 400

    if get_user_by_email(email):
        return jsonify({"error": "User already exists"}), 409

    # bcrypt hashing (REAL security)
    hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    add_user(name, email, hashed_pw)

    log_event(f"User registered: {email}")

    return jsonify({"message": "User created"}), 201


# 
# LOGIN (JWT TOKEN)
# 
@app.route("/login", methods=["POST"])
@limiter.limit("10 per minute")
def login():
    data = request.get_json()

    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    user = get_user_by_email(email)

    if not user:
        return jsonify({"error": "Invalid credentials"}), 401

    if not bcrypt.checkpw(password.encode(), user["password"].encode()):
        return jsonify({"error": "Invalid credentials"}), 401

    # create token
    token = create_access_token(
        identity={
            "id": user["id"],
            "email": user["email"]
        }
    )

    log_event(f"Login success: {email}")

    return jsonify({"token": token})


# 
#  PROTECTED ROUTE
#
@app.route("/me", methods=["GET"])
@jwt_required()
def me():
    user = get_jwt_identity()
    return jsonify(user)


# 
#  GET USERS (PROTECTED)
#
@app.route("/users", methods=["GET"])
@jwt_required()
def users():
    all_users = get_users()

    return jsonify([
        {
            "id": u["id"],
            "name": u["name"],
            "email": u["email"]
        }
        for u in all_users
    ])


# 
#  GET USER BY ID (PROTECTED)
@app.route("/users/<int:user_id>", methods=["GET"])
@jwt_required()
def user_detail(user_id):
    user = get_user_by_id(user_id)

    if not user:
        return jsonify({"error": "Not found"}), 404

    return jsonify({
        "id": user["id"],
        "name": user["name"],
        "email": user["email"]
    })


# 
# RUN SERVER
# 
if __name__ == "__main__":
    app.run(debug=True)
