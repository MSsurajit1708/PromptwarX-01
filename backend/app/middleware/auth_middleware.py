from functools import wraps
from flask import request, current_app, g
import jwt
from app.extensions.database import db
from app.models.user import User
from app.utils.helpers import error_response

def jwt_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return error_response("UNAUTHORIZED", "Missing or invalid authorization token", 401)
        
        token = auth_header.split(" ")[1]
        try:
            payload = jwt.decode(token, current_app.config["JWT_SECRET_KEY"], algorithms=["HS256"])
            user = db.session.get(User, payload.get("user_id"))
            if not user or not user.is_active:
                return error_response("UNAUTHORIZED", "User account inactive or non-existent", 401)
            g.current_user = user
        except jwt.ExpiredSignatureError:
            return error_response("TOKEN_EXPIRED", "Token has expired. Please login again.", 401)
        except jwt.InvalidTokenError:
            return error_response("INVALID_TOKEN", "Invalid authentication token", 401)

        return f(*args, **kwargs)
    return decorated

def admin_required(f):
    @wraps(f)
    @jwt_required
    def decorated(*args, **kwargs):
        if g.current_user.role != 'admin':
            return error_response("FORBIDDEN", "Admin privilege required for this resource", 403)
        return f(*args, **kwargs)
    return decorated
