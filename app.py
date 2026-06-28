from flask import Flask, request, jsonify
from database import (
    create_tables,
    create_user,
    get_user_by_email,
    hash_password
)

app = Flask(__name__)

# 🟢 Make sure database is created on startup
create_tables()


# 
#  REGISTER ROUTE
# 
@app.route("/register", methods=["POST"])
def register():
    try:
        data = request.json

        name = data.get("name")
        email = data.get("email")
        password = data.get("password")

        if not name or not email or not password:
            return jsonify({"error": "Missing fields"}), 400

        # check if user already exists
        existing_user = get_user_by_email(email)
        if existing_user:
            return jsonify({"error": "User already exists"}), 409

        # create user
        create_user(name, email, password)

        return jsonify({"message": "User created successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


#
# LOGIN ROUTE
#
@app.route("/login", methods=["POST"])
def login():
    try:
        data = request.json

        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify({"error": "Missing fields"}), 400

        user = get_user_by_email(email)

        if not user:
            return jsonify({"error": "User not found"}), 404

        # check password (hashed comparison)
        if user["password"] != hash_password(password):
            return jsonify({"error": "Invalid password"}), 401

        return jsonify({
            "message": "Login successful",
            "user": {
                "id": user["id"],
                "name": user["name"],
                "email": user["email"]
            }
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 
#  TEST ROUTE
#
@app.route("/")
def home():
    return jsonify({"message": "Firewall One backend is running"})


#
#  RUN SERVER
# 
if __name__ == "__main__":
    app.run(debug=True)
