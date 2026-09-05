from flask import Blueprint, request, g
from app.extensions.database import db
from app.models.project import Project
from app.models.saved_project import SavedProject
from app.utils.helpers import success_response, error_response
from app.middleware.auth_middleware import jwt_required

saved_bp = Blueprint('saved', __name__, url_prefix='/api/v1/projects')

@saved_bp.route('/<project_id>/save', methods=['POST'])
@jwt_required
def save_project(project_id):
    project = db.session.get(Project, project_id)
    if not project:
        return error_response("NOT_FOUND", "Project not found", 404)

    existing = SavedProject.query.filter_by(user_id=g.current_user.id, project_id=project.id).first()
    if existing:
        return error_response("DUPLICATE", "Project is already saved", 409)

    saved = SavedProject(user_id=g.current_user.id, project_id=project.id)
    db.session.add(saved)
    db.session.commit()
    return success_response(saved.to_dict(), "Project bookmarked", 201)

@saved_bp.route('/saved', methods=['GET'])
@jwt_required
def get_saved_projects():
    saved_list = SavedProject.query.filter_by(user_id=g.current_user.id).all()
    return success_response([s.to_dict() for s in saved_list])
