from datetime import datetime, timezone
import jwt
from flask import current_app
from app.extensions.database import db
from app.models.user import User
from app.models.profile import Profile

class AuthService:
    @staticmethod
    def generate_tokens(user_id):
        now = datetime.now(timezone.utc)
        access_payload = {
            "user_id": user_id,
            "type": "access",
            "exp": now + current_app.config["JWT_ACCESS_TOKEN_EXPIRES"]
        }
        refresh_payload = {
            "user_id": user_id,
            "type": "refresh",
            "exp": now + current_app.config.get("JWT_REFRESH_TOKEN_EXPIRES", current_app.config["JWT_ACCESS_TOKEN_EXPIRES"] * 7)
        }
        access_token = jwt.encode(access_payload, current_app.config["JWT_SECRET_KEY"], algorithm="HS256")
        refresh_token = jwt.encode(refresh_payload, current_app.config["JWT_SECRET_KEY"], algorithm="HS256")
        return access_token, refresh_token

    @classmethod
    def register_user(cls, name, email, password):
        user = User(name=name, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.flush()

        profile = Profile(user_id=user.id)
        db.session.add(profile)
        db.session.commit()

        access_token, refresh_token = cls.generate_tokens(user.id)
        return user, access_token, refresh_token

    @classmethod
    def authenticate_user(cls, email, password):
        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(password):
            return None, None, None
        user.last_login = datetime.now(timezone.utc)
        db.session.commit()
        access_token, refresh_token = cls.generate_tokens(user.id)
        return user, access_token, refresh_token
