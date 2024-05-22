from flask import request, jsonify, current_app
from app.middlewares.auth_middleware import token_required
from app.models.user import User
from app import db, bcrypt
from datetime import datetime, timedelta
import jwt
from bson import ObjectId

user_model = User(db)


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
def create_user():
    data = request.get_json()
    if not all(key in data for key in ("name", "email", "phone_number", "age")):
        return jsonify({"message": "Missing required fields"}), 400
    
    # Check if the user already exists
    existing_user = db.users.find_one({"email": data["email"]})
    if existing_user:
        return jsonify({"message": "User already exists"}), 409

    user = {
        "name": data["name"],
        "email": data["email"],
        "phone_number": data["phone_number"],
        "age": data["age"],
    
    }
    user_model.create_user(user)
    return jsonify({"message": "User Created successfully"}), 201


@token_required
def get_all_users():
    users = user_model.get_all_users()
    users_json = []
    # Convert ObjectId to string
    for user in users:
        user["_id"] = str(user["_id"])
        users_json.append(user)
    return jsonify(users_json), 200


@token_required
def get_user_by_id():
    user_id = ObjectId(request.args.get("user_id"))
    user = user_model.get_user_by_id(user_id)
    if user:
        # Convert ObjectId field to string
        user["_id"] = str(user["_id"])
        return jsonify(user), 200
    return jsonify({"message": "User not found"}), 404

@token_required
def update_user():
    data = request.get_json()
    existing_user = db.users.find_one({"email": data["email"]})
    if not existing_user:
        return jsonify({"message": "User not found"}), 404

    user_model.update_user(data["email"], data)
    return jsonify({"message": "User updated successfully"}), 200


@token_required
def delete_user():
    user_id = ObjectId(request.args.get("user_id"))
    user_model.delete_user(user_id)
    return jsonify({"message": "User deleted successfully"}), 200
