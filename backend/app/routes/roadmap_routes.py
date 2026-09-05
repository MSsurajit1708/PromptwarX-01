from flask import Blueprint, request, g
from app.extensions.database import db
from app.models.project import Project
from app.models.roadmap import Roadmap
from app.models.task import Task
from app.services.ai_service import AIService
from app.utils.helpers import success_response, error_response
from app.middleware.auth_middleware import jwt_required

roadmap_bp = Blueprint('roadmap', __name__, url_prefix='/api/v1/projects')

@roadmap_bp.route('/<project_id>/roadmap/generate', methods=['POST'])
@jwt_required
def generate_project_roadmap(project_id):
    project = Project.query.get(project_id)
    if not project or project.owner_id != g.current_user.id:
        return error_response("NOT_FOUND", "Project not found", 404)

    phases = AIService.generate_roadmap(project.title, project.description)

    # Clear existing roadmaps & tasks
    Roadmap.query.filter_by(project_id=project.id).delete()
    Task.query.filter_by(project_id=project.id).delete()

    created_roadmaps = []
    for phase_data in phases:
        rm = Roadmap(
            project_id=project.id,
            phase_name=phase_data["phase_name"],
            phase_order=phase_data["phase_order"],
            description=phase_data.get("description")
        )
        db.session.add(rm)
        db.session.flush()

        # Add 2 default tasks per phase
        t1 = Task(project_id=project.id, roadmap_id=rm.id, title=f"{rm.phase_name} - Setup & Prep", priority="HIGH")
        t2 = Task(project_id=project.id, roadmap_id=rm.id, title=f"{rm.phase_name} - Implementation", priority="MEDIUM")
        db.session.add_all([t1, t2])
        created_roadmaps.append(rm)

    db.session.commit()
    return success_response([rm.to_dict() for rm in created_roadmaps], "Roadmap generated successfully")

@roadmap_bp.route('/<project_id>/roadmap', methods=['GET'])
@jwt_required
def get_project_roadmap(project_id):
    project = Project.query.get(project_id)
    if not project or project.owner_id != g.current_user.id:
        return error_response("NOT_FOUND", "Project not found", 404)
    roadmaps = Roadmap.query.filter_by(project_id=project.id).order_by(Roadmap.phase_order.asc()).all()
    return success_response([rm.to_dict() for rm in roadmaps])
