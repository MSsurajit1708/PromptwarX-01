from app.extensions.database import db
from app.models.chat_message import ChatMessage
from app.services.ai_service import AIService

class MentorService:
    @staticmethod
    def handle_chat(user_id, project, message_text):
        user_msg = ChatMessage(user_id=user_id, project_id=project.id, role='user', content=message_text)
        db.session.add(user_msg)

        history = ChatMessage.query.filter_by(project_id=project.id).order_by(ChatMessage.created_at.desc()).limit(5).all()
        history_dicts = [h.to_dict() for h in reversed(history)]

        ai_reply = AIService.chat_mentor(project.title, message_text, history_dicts)
        assistant_msg = ChatMessage(user_id=user_id, project_id=project.id, role='assistant', content=ai_reply)
        db.session.add(assistant_msg)

        db.session.commit()
        return user_msg, assistant_msg
