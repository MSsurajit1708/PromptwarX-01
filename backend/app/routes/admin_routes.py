from flask import Blueprint, request
from app.models.user import User
from app.models.project import Project
from app.utils.helpers import success_response
from app.middleware.auth_middleware import admin_required

admin_bp = Blueprint('admin', __name__, url_prefix='/api/v1/admin')

@admin_bp.route('/users', methods=['GET'])
@admin_required
def get_all_users():
    users = User.query.all()
    return success_response([u.to_dict() for u in users])

@admin_bp.route('/analytics', methods=['GET'])
@admin_required
def get_analytics():
    total_users = User.query.count()
    total_projects = Project.query.count()
    return success_response({
        "total_users": total_users,
        "total_projects": total_projects,
        "active_students": User.query.filter_by(role='student').count(),
        "platform_status": "healthy"
    })
