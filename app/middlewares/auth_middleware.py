import jwt
from app import db
from flask import request, jsonify, current_app
from functools import wraps
from app.models.user import User

user_model = User(db)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]

        if not token:
            return jsonify({"message": "Token is missing!"}), 401

        try:
            data = jwt.decode(
                token, current_app.config["SECRET_KEY"], algorithms=["HS256"]
            )
            current_user = user_model.find_user_by_email(data["email"])
            if not current_user:
                raise RuntimeError("User not found")
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token has expired!"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Token is invalid!"}), 401

        if f.__code__.co_argcount == 0:
            return f()

        return f(current_user, *args, **kwargs)

    return decorated
