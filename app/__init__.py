from flask import Flask
from flask_jwt_extended import JWTManager
from app.config.db import db
from app.config.config import Config
from app.auth.auth_routes import auth_bp
from app.admin.admin_routes import admin_bp
from app.doctor.availability.availibility_routes import availability_bp
from app.member.book_appointment.appointment_routes import appointment_bp
from flask_migrate import Migrate


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    jwt = JWTManager(app)

    db.init_app(app)
    Migrate(app, db)

    # with app.app_context():
    #     db.create_all()  #db.py

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(availability_bp)
    app.register_blueprint(appointment_bp)

    @app.route("/")
    def index():
        return "RBAC Assignment"

    return app
