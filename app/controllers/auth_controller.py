from flask import request, jsonify, current_app
import jwt
from app import bcrypt, db
from app.models.user import User
from app.utils.email import send_email
from app.middlewares.auth_middleware import token_required
import uuid
from datetime import datetime, timedelta

user_model = User(db)

# In-memory blocklist for demo purposes, ideally this should be persisted
BLOCKLIST = set()


def register():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
    user = {"email": email, "password": hashed_password}

    user_model.create_user(user)
    return jsonify({"message": "User registered successfully"}), 201


def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = user_model.find_user_by_email(email)
    if user and bcrypt.check_password_hash(user["password"], password):
        access_token = jwt.encode(
            {"email": email, "exp": datetime.utcnow() + timedelta(minutes=30)},
            current_app.config["SECRET_KEY"],
            algorithm="HS256",
        )
        refresh_token = jwt.encode(
            {"email": email, "exp": datetime.utcnow() + timedelta(days=7)},
            current_app.config["SECRET_KEY"],
            algorithm="HS256",
        )
        return jsonify(access_token=access_token, refresh_token=refresh_token), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401


@token_required
def logout():
    token = request.headers["Authorization"].split(" ")[1]
    BLOCKLIST.add(token)
    return jsonify({"message": "Successfully logged out"}), 200


def refresh():
    token = request.headers["Authorization"].split(" ")[1]
    try:
        data = jwt.decode(
            token,
            current_app.config["SECRET_KEY"],
            algorithms=["HS256"],
            options={"verify_exp": False},
        )
        if token in BLOCKLIST:
            raise jwt.InvalidTokenError
        access_token = jwt.encode(
            {"email": data["email"], "exp": datetime.utcnow() + timedelta(minutes=30)},
            current_app.config["SECRET_KEY"],
            algorithm="HS256",
        )
        return jsonify(access_token=access_token), 200
    except jwt.ExpiredSignatureError:
        return jsonify({"message": "Token has expired!"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"message": "Token is invalid!"}), 401


# In-memory store for password reset tokens (for demo purposes)
RESET_TOKENS = {}


def request_password_reset():
    data = request.get_json()
    email = data.get("email")

    user = user_model.find_user_by_email(email)
    if user:
        reset_token = str(uuid.uuid4())
        RESET_TOKENS[reset_token] = email
        reset_url = f"http://your-domain.com/reset-password?token={reset_token}"
        send_email(
            "Password Reset Request",
            "no-reply@your-domain.com",
            email,
            f"Click the link to reset your password: {reset_url}",
        )
        return jsonify({"message": "Password reset link sent"}), 200
    else:
        return jsonify({"message": "Email not found"}), 404


def reset_password():
    data = request.get_json()
    reset_token = data.get("token")
    new_password = data.get("new_password")

    email = RESET_TOKENS.get(reset_token)
    if email:
        hashed_password = bcrypt.generate_password_hash(new_password).decode("utf-8")
        user_model.update_user(email, {"password": hashed_password})
        del RESET_TOKENS[reset_token]
        return jsonify({"message": "Password updated successfully"}), 200
    else:
        return jsonify({"message": "Invalid or expired token"}), 400
