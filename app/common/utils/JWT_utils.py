from flask_jwt_extended import create_access_token, get_jwt_identity
from app.common.models.user import User
from datetime import timedelta

def generate_token(identity, role):
    return create_access_token(
        identity= str(identity),
        additional_claims={"role": role},
        expires_delta=timedelta(hours=1)
    )

def get_current_user():
    user_id = get_jwt_identity()
    return User.query.filter_by(id=user_id).first()