from flask import Flask
from flask_jwt_extended import JWTManager
from app.config.db import db
from app.config.config import Config
from app.routes.auth_routes import auth_bp
from app.routes.admin_routes import admin_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    jwt = JWTManager(app)

    db.init_app(app)

    with app.app_context():
        db.create_all()  #db.py

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)

    @app.route("/")
    def index():
        return "RBAC Assignment"

    return app
