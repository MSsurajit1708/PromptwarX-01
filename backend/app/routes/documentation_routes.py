from flask import Blueprint, request, g
from app.extensions.database import db
from app.models.project import Project
from app.models.documentation import Documentation
from app.services.ai_service import AIService
from app.utils.helpers import success_response, error_response
from app.middleware.auth_middleware import jwt_required

doc_bp = Blueprint('documentation', __name__, url_prefix='/api/v1/projects')

@doc_bp.route('/<project_id>/documentation/generate', methods=['POST'])
@jwt_required
def generate_documentation(project_id):
    project = Project.query.get(project_id)
    if not project or project.owner_id != g.current_user.id:
        return error_response("NOT_FOUND", "Project not found", 404)

    sections = AIService.generate_documentation_outline(project.title)
    created_docs = []
    for s in sections:
        doc = Documentation(project_id=project.id, section=s["section"], content=s["content"])
        db.session.add(doc)
        created_docs.append(doc)

    db.session.commit()
    return success_response([d.to_dict() for d in created_docs], "Documentation outline generated")

@doc_bp.route('/<project_id>/documentation', methods=['GET'])
@jwt_required
def get_documentation(project_id):
    project = Project.query.get(project_id)
    if not project or project.owner_id != g.current_user.id:
        return error_response("NOT_FOUND", "Project not found", 404)
    docs = Documentation.query.filter_by(project_id=project.id).all()
    return success_response([d.to_dict() for d in docs])
