from flask import Blueprint, g
from app.extensions.database import db
from app.models.project import Project
from app.services.ai_service import AIService
from app.utils.helpers import success_response, error_response
from app.middleware.auth_middleware import jwt_required

viva_bp = Blueprint('viva', __name__, url_prefix='/api/v1/projects')

@viva_bp.route('/<project_id>/viva/generate', methods=['POST'])
@jwt_required
def generate_viva_prep(project_id):
    project = db.session.get(Project, project_id)
    if not project or project.owner_id != g.current_user.id:
        return error_response("NOT_FOUND", "Project not found", 404)

    questions = AIService.generate_viva_questions(project.title)
    return success_response({"questions": questions}, "Viva preparation questions generated")
