from flask import Blueprint, request, g
from app.extensions.database import db
from app.models.project import Project
from app.models.project_feature import ProjectFeature
from app.models.profile import Profile
from app.services.project_generation_service import ProjectGenerationService
from app.services.recommendation_service import RecommendationService
from app.services.ai_service import AIService
from app.schemas.project_schema import ProjectSchema
from app.utils.helpers import success_response, error_response
from app.middleware.auth_middleware import jwt_required

project_bp = Blueprint('project', __name__, url_prefix='/api/v1')

# 1. GENERATE
@project_bp.route('/projects/generate', methods=['POST'])
@jwt_required
def generate_projects():
    data = request.get_json() or {}
    profile = Profile.query.filter_by(user_id=g.current_user.id).first()
    profile_dict = profile.to_dict() if profile else {}

    scored_projects, gen_id = ProjectGenerationService.generate_and_score(
        user_id=g.current_user.id,
        profile_dict=profile_dict,
        overrides=data
    )

    return success_response({
        "projects": scored_projects,
        "generation_id": gen_id
    }, "Project recommendations generated successfully")

# 2. DISCOVER / SEARCH & FILTER
@project_bp.route('/projects/discover', methods=['GET'])
def discover_projects():
    page = request.args.get("page", 1, type=int)
    limit = request.args.get("limit", 20, type=int)
    filters = {
        "domain": request.args.get("domain"),
        "difficulty": request.args.get("difficulty"),
        "duration": request.args.get("duration")
    }
    result = RecommendationService.filter_projects(filters, page, limit)
    return success_response(result)

# 3. COMPARE
@project_bp.route('/projects/compare', methods=['POST'])
@jwt_required
def compare_projects():
    data = request.get_json() or {}
    projects = data.get("projects", [])
    if len(projects) < 2:
        return error_response("VALIDATION_ERROR", "Provide at least 2 projects to compare", 400)

    comparison_matrix = []
    for p in projects:
        comparison_matrix.append({
            "title": p.get("title", "Untitled"),
            "difficulty": p.get("difficulty", "Intermediate"),
            "duration": p.get("duration", "8 weeks"),
            "overall_score": p.get("overall_score", 85),
            "skill_match": p.get("skill_match", 80),
            "feasibility": p.get("feasibility", 90),
            "career_relevance": p.get("career_relevance", 92)
        })
    return success_response({"comparison": comparison_matrix})

# 4. CRUD
@project_bp.route('/projects', methods=['GET'])
@jwt_required
def get_user_projects():
    projects = Project.query.filter_by(owner_id=g.current_user.id).all()
    return success_response([p.to_dict() for p in projects])

@project_bp.route('/projects/<project_id>', methods=['GET'])
@jwt_required
def get_project_by_id(project_id):
    project = db.session.get(Project, project_id)
    if not project or project.owner_id != g.current_user.id:
        return error_response("NOT_FOUND", "Project not found or unauthorized", 404)
    return success_response(project.to_dict())

@project_bp.route('/projects', methods=['POST'])
@jwt_required
def create_project():
    data = request.get_json() or {}
    errors = ProjectSchema.validate_project(data)
    if errors:
        return error_response("VALIDATION_ERROR", "Invalid project data", 400, errors)

    project = Project(
        owner_id=g.current_user.id,
        title=data.get('title'),
        description=data.get('description'),
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

@project_bp.route('/projects/<project_id>', methods=['PUT'])
@jwt_required
def update_project(project_id):
    project = db.session.get(Project, project_id)
    if not project or project.owner_id != g.current_user.id:
        return error_response("NOT_FOUND", "Project not found", 404)

    data = request.get_json() or {}
    project.title = data.get('title', project.title)
    project.description = data.get('description', project.description)
    project.status = data.get('status', project.status)
    db.session.commit()
    return success_response(project.to_dict(), "Project updated successfully")

@project_bp.route('/projects/<project_id>', methods=['DELETE'])
@jwt_required
def delete_project(project_id):
    project = db.session.get(Project, project_id)
    if not project or project.owner_id != g.current_user.id:
        return error_response("NOT_FOUND", "Project not found", 404)
    db.session.delete(project)
    db.session.commit()
    return success_response(None, "Project deleted successfully")

# 5. FEATURE GENERATION & CRUD
@project_bp.route('/projects/<project_id>/features/generate', methods=['POST'])
@jwt_required
def generate_features(project_id):
    project = db.session.get(Project, project_id)
    if not project or project.owner_id != g.current_user.id:
        return error_response("NOT_FOUND", "Project not found", 404)

    features_dict = AIService.generate_features(project.title, project.description)
    ProjectFeature.query.filter_by(project_id=project.id).delete()
    created = []
    for cat, items in features_dict.items():
        for item in items:
            feat = ProjectFeature(project_id=project.id, name=item, category=cat.upper(), priority="HIGH" if cat == "mvp" else "MEDIUM")
            db.session.add(feat)
            created.append(feat)
    db.session.commit()
    return success_response([f.to_dict() for f in created], "Features generated successfully")

@project_bp.route('/projects/<project_id>/features', methods=['GET'])
@jwt_required
def get_features(project_id):
    project = db.session.get(Project, project_id)
    if not project or project.owner_id != g.current_user.id:
        return error_response("NOT_FOUND", "Project not found", 404)
    features = ProjectFeature.query.filter_by(project_id=project.id).all()
    return success_response([f.to_dict() for f in features])

# 6. TECH STACK, ARCHITECTURE, DATABASE DESIGN & CAREER
@project_bp.route('/projects/<project_id>/technologies/generate', methods=['POST'])
@jwt_required
def generate_tech_stack(project_id):
    project = db.session.get(Project, project_id)
    if not project or project.owner_id != g.current_user.id:
        return error_response("NOT_FOUND", "Project not found", 404)
    tech = AIService.generate_technologies(project.title, project.description)
    return success_response(tech)

@project_bp.route('/projects/<project_id>/architecture/generate', methods=['POST'])
@jwt_required
def generate_architecture(project_id):
    project = db.session.get(Project, project_id)
    if not project or project.owner_id != g.current_user.id:
        return error_response("NOT_FOUND", "Project not found", 404)
    arch = AIService.generate_architecture(project.title, project.technologies or ["Python", "React"])
    return success_response(arch)

@project_bp.route('/projects/<project_id>/database-design/generate', methods=['POST'])
@jwt_required
def generate_database_design(project_id):
    project = db.session.get(Project, project_id)
    if not project or project.owner_id != g.current_user.id:
        return error_response("NOT_FOUND", "Project not found", 404)
    db_design = AIService.generate_database_design(project.title, project.description)
    return success_response(db_design)

@project_bp.route('/projects/<project_id>/career-analysis', methods=['POST'])
@jwt_required
def generate_career_analysis(project_id):
    project = db.session.get(Project, project_id)
    if not project or project.owner_id != g.current_user.id:
        return error_response("NOT_FOUND", "Project not found", 404)
    analysis = AIService.analyze_career_value(project.title, project.technologies or ["Python", "React"])
    return success_response(analysis)
