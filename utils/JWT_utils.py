from flask_jwt_extended import create_access_token
from datetime import timedelta

def generate_token(identity, role):
    return create_access_token(identity={"id": identity, "role": role}, expires_delta=timedelta(hours=1))
