from flask import Blueprint, request, g
from app.extensions.database import db
from app.models.project import Project
from app.models.generated_project import GeneratedProject
from app.models.profile import Profile
from app.services.ai_service import AIService
from app.utils.scoring import calculate_project_score
from app.utils.helpers import success_response, error_response
from app.middleware.auth_middleware import jwt_required

project_bp = Blueprint('project', __name__, url_prefix='/api/v1/projects')

@project_bp.route('/generate', methods=['POST'])
@jwt_required
def generate_projects():
    data = request.get_json() or {}
    profile = Profile.query.filter_by(user_id=g.current_user.id).first()
    profile_dict = profile.to_dict() if profile else {}

    # Merge explicit form payload with saved profile
    merged_profile = {
        "skills": data.get("skills") or [s["name"] for s in profile_dict.get("skills", [])],
        "interests": data.get("interests") or [i["name"] for i in profile_dict.get("interests", [])],
        "branch": data.get("branch") or profile_dict.get("branch", "Computer Science"),
        "careerGoal": data.get("career_goal") or profile_dict.get("career_goal", "Software Developer"),
        "experience": data.get("experience_level") or profile_dict.get("experience_level", "Intermediate"),
        "difficulty": data.get("difficulty", "Intermediate"),
        "duration": data.get("duration", "8 weeks")
    }

    raw_projects = AIService.generate_projects(merged_profile)
    scored_projects = []

    for proj in raw_projects:
        scores = calculate_project_score(proj, merged_profile)
        proj.update(scores)
        scored_projects.append(proj)

    # Sort descending by overall_score
    scored_projects.sort(key=lambda x: x.get("overall_score", 0), reverse=True)

    # Persist generation record
    gen_record = GeneratedProject(
        user_id=g.current_user.id,
        generation_request=merged_profile,
        project_data=scored_projects,
        recommendation_score=scored_projects[0]["overall_score"] if scored_projects else 0.0
    )
    db.session.add(gen_record)
    db.session.commit()

    return success_response({
        "projects": scored_projects,
        "generation_id": gen_record.id
    }, "Project recommendations generated successfully")

@project_bp.route('', methods=['GET'])
@jwt_required
def get_user_projects():
    projects = Project.query.filter_by(owner_id=g.current_user.id).all()
    return success_response([p.to_dict() for p in projects])

@project_bp.route('/<project_id>', methods=['GET'])
@jwt_required
def get_project_by_id(project_id):
    project = Project.query.get(project_id)
    if not project or project.owner_id != g.current_user.id:
        return error_response("NOT_FOUND", "Project not found or unauthorized", 404)
    return success_response(project.to_dict())

@project_bp.route('', methods=['POST'])
@jwt_required
def create_project():
    data = request.get_json() or {}
    title = data.get('title')
    description = data.get('description')
    if not title or not description:
        return error_response("VALIDATION_ERROR", "Title and description are required", 400)

    project = Project(
        owner_id=g.current_user.id,
        title=title,
        description=description,
        problem_statement=data.get('problem_statement'),
        proposed_solution=data.get('proposed_solution'),
        domain=data.get('domain', 'General'),
        difficulty=data.get('difficulty', 'Intermediate'),
        duration=data.get('duration', '8 weeks'),
        overall_score=data.get('overall_score', 85.0),
        technologies=data.get('technologies', []),
        target_users=data.get('target_users', [])
    )
    db.session.add(project)
    db.session.commit()
    return success_response(project.to_dict(), "Project selected and workspace created", 201)
