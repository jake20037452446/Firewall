from flask import Flask, jsonify, request
from flask_cors import CORS

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    jwt_required,
    get_jwt_identity,
    get_jwt
)

from flask_talisman import Talisman
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_smorest import Api

from dotenv import load_dotenv
from email_validator import validate_email, EmailNotValidError

import redis
import logging
import re

from pythonjsonlogger import jsonlogger

import os
import datetime
import bcrypt

from models import (
    get_users,
    get_user_by_id,
    add_user,
    get_user_by_email
)

from revoked_tokens import add_token, is_token_revoked


# Load environment variables
load_dotenv()


app = Flask(__name__)


# JWT settings
app.config["JWT_SECRET_KEY"] = os.getenv(
    "JWT_SECRET_KEY",
    "CHANGE_THIS_SECRET"
)

app.config["JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(
    hours=1
)


# Database settings
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
    "DATABASE_URL",
    "sqlite:///firewall_one.db"
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db = SQLAlchemy(app)

migrate = Migrate(
    app,
    db
)


api = Api(app)


# CORS settings
CORS(app)


# Security headers
Talisman(
    app,
    force_https=False
)


# JWT setup
jwt = JWTManager(app)


@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):

    jti = jwt_payload["jti"]

    return is_token_revoked(jti)



# Rate limiting
limiter = Limiter(
    get_remote_address,
    app=app,
    storage_uri="redis://localhost:6379",
    default_limits=[
        "200 per day",
        "50 per hour"
    ]
)


# Redis connection
redis_client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)



# Logging setup
logger = logging.getLogger()

handler = logging.StreamHandler()

formatter = jsonlogger.JsonFormatter()

handler.setFormatter(formatter)

logger.addHandler(handler)

logger.setLevel(logging.INFO)



def log_event(message):

    logger.info({
        "event": message,
        "time": str(datetime.datetime.now())
    })



# Email validation
def check_email(email):

    try:
        validate_email(email)
        return True

    except EmailNotValidError:
        return False



# Password validation
def check_password(password):

    return (
        len(password) >= 8
        and re.search("[A-Z]", password)
        and re.search("[0-9]", password)
    )



# JWT errors
@jwt.expired_token_loader
def expired_token(jwt_header, jwt_payload):

    return jsonify({
        "error": "Token expired"
    }), 401



@jwt.invalid_token_loader
def invalid_token(error):

    return jsonify({
        "error": "Invalid token"
    }), 401



# Error handlers
@app.errorhandler(404)
def not_found(error):

    return jsonify({
        "error": "Route not found"
    }), 404



@app.errorhandler(500)
def server_error(error):

    return jsonify({
        "error": "Internal server error"
    }), 500



# Home route
@app.route("/")
def home():

    return jsonify({
        "message": "Firewall One API Running",
        "status": "online"
    })



# Get users
@app.route("/users", methods=["GET"])
@limiter.limit("10 per minute")
def users():

    return jsonify(
        get_users()
    )



# Get user by ID
@app.route("/users/<int:user_id>", methods=["GET"])
@jwt_required()
def user(user_id):

    user = get_user_by_id(user_id)

    if user:

        return jsonify(user)

    return jsonify({
        "error": "User not found"
    }), 404



# Register user
@app.route("/register", methods=["POST"])
@limiter.limit("5 per minute")
def register():

    data = request.json

    email = data.get("email", "").lower()

    password = data.get("password", "")


    if not check_email(email):

        return jsonify({
            "error": "Invalid email"
        }), 400



    if not check_password(password):

        return jsonify({
            "error": "Password must be 8 characters"
        }), 400



    if get_user_by_email(email):

        return jsonify({
            "error": "User already exists"
        }), 409



    password_hash = bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    )


    user = add_user(
        email,
        password_hash.decode()
    )


    log_event(
        f"User registered {email}"
    )


    return jsonify({
        "message": "User created",
        "user": user
    }), 201



# Login
@app.route("/login", methods=["POST"])
@limiter.limit("5 per minute")
def login():

    data = request.json

    email = data.get("email")

    password = data.get("password")


    user = get_user_by_email(email)


    if not user:

        return jsonify({
            "error": "Invalid login"
        }), 401



    if bcrypt.checkpw(
        password.encode(),
        user["password"].encode()
    ):


        token = create_access_token(
            identity=user["id"]
        )


        log_event(
            f"Login {email}"
        )


        return jsonify({
            "access_token": token
        })


    return jsonify({
        "error": "Invalid login"
    }), 401



# Logout
@app.route("/logout", methods=["POST"])
@jwt_required()
def logout():

    token = get_jwt()

    add_token(token["jti"])

    return jsonify({
        "message": "Logged out"
    })



# Profile
@app.route("/profile")
@jwt_required()
def profile():

    user_id = get_jwt_identity()


    return jsonify({
        "user_id": user_id
    })



# Start server
if __name__ == "__main__":

    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000
    )
