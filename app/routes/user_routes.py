from flask import Blueprint
from app.controllers import user_controller
from app.middlewares.auth_middleware import token_required

user_bp = Blueprint("user_bp", __name__)

user_bp.route("/login", methods=["POST"])(user_controller.login)

user_bp.route("/users/create", methods=["POST"])(
    token_required(user_controller.create_user)
)
user_bp.route("/users", methods=["GET"])(token_required(user_controller.get_all_users))
user_bp.route("/users/get_by_id", methods=["GET"])(
    token_required(user_controller.get_user_by_id)
)
user_bp.route("/users/update", methods=["PUT"])(
    token_required(user_controller.update_user)
)
user_bp.route("/users/delete", methods=["DELETE"])(
    token_required(user_controller.delete_user)
)
