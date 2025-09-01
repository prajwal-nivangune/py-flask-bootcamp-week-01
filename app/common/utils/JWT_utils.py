from datetime import timedelta

from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity

from app.common.models.user import User


def generate_token(identity, role):
    access_token = create_access_token(
        identity=str(identity), additional_claims={"role": role}, expires_delta=timedelta(hours=1)
    )

    refresh_token = create_refresh_token(
        identity=str(identity), additional_claims={"role": role}, expires_delta=timedelta(days=30)
    )

    return access_token, refresh_token


def get_current_user():
    user_id = get_jwt_identity()
    return User.query.filter_by(id=user_id).first()
