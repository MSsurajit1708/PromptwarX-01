from datetime import datetime
from flask import Blueprint, request, g
from app.extensions.database import db
from app.models.project import Project
from app.models.task import Task
from app.utils.helpers import success_response, error_response
from app.middleware.auth_middleware import jwt_required

task_bp = Blueprint('task', __name__, url_prefix='/api/v1')

@task_bp.route('/projects/<project_id>/tasks', methods=['GET'])
@jwt_required
def get_tasks(project_id):
    project = Project.query.get(project_id)
    if not project or project.owner_id != g.current_user.id:
        return error_response("NOT_FOUND", "Project not found", 404)
    tasks = Task.query.filter_by(project_id=project.id).all()
    return success_response([t.to_dict() for t in tasks])

@task_bp.route('/projects/<project_id>/tasks', methods=['POST'])
@jwt_required
def create_task(project_id):
    project = Project.query.get(project_id)
    if not project or project.owner_id != g.current_user.id:
        return error_response("NOT_FOUND", "Project not found", 404)
    data = request.get_json() or {}
    title = data.get('title')
    if not title:
        return error_response("VALIDATION_ERROR", "Task title is required", 400)

    task = Task(
        project_id=project.id,
        roadmap_id=data.get('roadmap_id'),
        title=title,
        description=data.get('description'),
        priority=data.get('priority', 'MEDIUM'),
        status=data.get('status', 'NOT_STARTED'),
        estimated_hours=data.get('estimated_hours', 5)
    )
    db.session.add(task)
    db.session.commit()
    return success_response(task.to_dict(), "Task created successfully", 201)

@task_bp.route('/tasks/<task_id>/status', methods=['PATCH'])
@jwt_required
def update_task_status(task_id):
    task = Task.query.get(task_id)
    if not task or task.project.owner_id != g.current_user.id:
        return error_response("NOT_FOUND", "Task not found", 404)
    data = request.get_json() or {}
    new_status = data.get('status')
    if new_status not in ['NOT_STARTED', 'IN_PROGRESS', 'COMPLETED', 'BLOCKED']:
        return error_response("VALIDATION_ERROR", "Invalid task status", 400)

    task.status = new_status
    if new_status == 'COMPLETED':
        task.completed_at = datetime.utcnow()
    else:
        task.completed_at = None

    db.session.commit()
    return success_response(task.to_dict(), "Task status updated")
