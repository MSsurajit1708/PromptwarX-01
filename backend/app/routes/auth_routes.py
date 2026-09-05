from datetime import datetime
from flask import Blueprint, request, current_app, g
import jwt
from app.extensions.database import db
from app.models.user import User
from app.models.profile import Profile
from app.utils.helpers import success_response, error_response
from app.middleware.auth_middleware import jwt_required

auth_bp = Blueprint('auth', __name__, url_prefix='/api/v1/auth')

def _generate_token(user_id):
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + current_app.config["JWT_ACCESS_TOKEN_EXPIRES"]
    }
    return jwt.encode(payload, current_app.config["JWT_SECRET_KEY"], algorithm="HS256")

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    name = data.get('name')
    email = data.get('email', '').strip().lower()
    password = data.get('password')

    if not name or not email or not password:
        return error_response("VALIDATION_ERROR", "Name, email, and password are required.", 400)

    if User.query.filter_by(email=email).first():
        return error_response("DUPLICATE_EMAIL", "An account with this email already exists.", 409)

    user = User(name=name, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.flush()

    # Create associated empty profile
    profile = Profile(user_id=user.id)
    db.session.add(profile)
    db.session.commit()

    token = _generate_token(user.id)
    return success_response({
        "user": user.to_dict(),
        "token": token
    }, "User registered successfully", 201)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    email = data.get('email', '').strip().lower()
    password = data.get('password')

    if not email or not password:
        return error_response("VALIDATION_ERROR", "Email and password are required.", 400)

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return error_response("INVALID_CREDENTIALS", "Invalid email or password", 401)

    user.last_login = datetime.utcnow()
    db.session.commit()

    token = _generate_token(user.id)
    return success_response({
        "user": user.to_dict(),
        "token": token
    }, "Login successful")

@auth_bp.route('/me', methods=['GET'])
@jwt_required
def get_me():
    return success_response(g.current_user.to_dict())
