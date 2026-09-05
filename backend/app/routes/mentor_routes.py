from flask import Blueprint, request, g
from app.extensions.database import db
from app.models.project import Project
from app.models.chat_message import ChatMessage
from app.services.ai_service import AIService
from app.utils.helpers import success_response, error_response
from app.middleware.auth_middleware import jwt_required

mentor_bp = Blueprint('mentor', __name__, url_prefix='/api/v1/projects')

@mentor_bp.route('/<project_id>/mentor/chat', methods=['POST'])
@jwt_required
def chat_with_mentor(project_id):
    project = Project.query.get(project_id)
    if not project or project.owner_id != g.current_user.id:
        return error_response("NOT_FOUND", "Project not found", 404)

    data = request.get_json() or {}
    user_msg = data.get('message')
    if not user_msg:
        return error_response("VALIDATION_ERROR", "Message is required", 400)

    # Save user message
    user_chat = ChatMessage(user_id=g.current_user.id, project_id=project.id, role='user', content=user_msg)
    db.session.add(user_chat)

    # Fetch recent history (last 5 messages)
    history = ChatMessage.query.filter_by(project_id=project.id).order_by(ChatMessage.created_at.desc()).limit(5).all()
    history_dicts = [h.to_dict() for h in reversed(history)]

    # Generate AI mentor response
    ai_reply = AIService.chat_mentor(project.title, user_msg, history_dicts)
    assistant_chat = ChatMessage(user_id=g.current_user.id, project_id=project.id, role='assistant', content=ai_reply)
    db.session.add(assistant_chat)

    db.session.commit()
    return success_response({
        "user_message": user_chat.to_dict(),
        "assistant_message": assistant_chat.to_dict()
    })

@mentor_bp.route('/<project_id>/mentor/history', methods=['GET'])
@jwt_required
def get_chat_history(project_id):
    project = Project.query.get(project_id)
    if not project or project.owner_id != g.current_user.id:
        return error_response("NOT_FOUND", "Project not found", 404)
    messages = ChatMessage.query.filter_by(project_id=project.id).order_by(ChatMessage.created_at.asc()).all()
    return success_response([m.to_dict() for m in messages])
