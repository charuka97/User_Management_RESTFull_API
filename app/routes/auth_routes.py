from flask import Blueprint
from app.controllers import auth_controller
from app.middlewares.auth_middleware import token_required

auth_bp = Blueprint("auth_bp", __name__)

auth_bp.route("/register", methods=["POST"])(auth_controller.register)
auth_bp.route("/login", methods=["POST"])(auth_controller.login)
auth_bp.route("/logout", methods=["POST"])(token_required(auth_controller.logout))
auth_bp.route("/refresh", methods=["POST"])(auth_controller.refresh)
auth_bp.route("/request-password-reset", methods=["POST"])(
    auth_controller.request_password_reset
)
auth_bp.route("/reset-password", methods=["POST"])(auth_controller.reset_password)
