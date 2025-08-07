from flask import Flask
from flask_jwt_extended import JWTManager
from models import db
from config import Config
from routes.auth_routes import auth_bp
from routes.admin_routes import admin_bp
app = Flask(__name__)
app.config.from_object(Config)
jwt = JWTManager(app)

db.init_app(app)

with app.app_context():
    db.create_all()

app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)


@app.route("/")
def index():
    return "RBAC Assignment"

if __name__ == '__main__':
    app.run(debug=True)