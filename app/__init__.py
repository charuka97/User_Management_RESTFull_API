from flask import Flask
from flask_bcrypt import Bcrypt
from pymongo import MongoClient
import urllib.parse

app = Flask(__name__)
app.config.from_object("app.config.config.Config")

bcrypt = Bcrypt(app)

# Parse MongoDB URI and escape username and password
parsed_uri = urllib.parse.urlparse(app.config["MONGO_URI"])
escaped_username = urllib.parse.quote_plus(parsed_uri.username or "")
escaped_password = urllib.parse.quote_plus(parsed_uri.password or "")
escaped_uri = (
    f"{parsed_uri.scheme}://{escaped_username}:{escaped_password}@"
    f"{parsed_uri.hostname}/{parsed_uri.path.lstrip('/')}"
)

client = MongoClient(escaped_uri)
db = client[app.config["MONGO_DBNAME"]]

from app.routes import auth_routes, user_routes

app.register_blueprint(auth_routes.auth_bp)
app.register_blueprint(user_routes.user_bp)
