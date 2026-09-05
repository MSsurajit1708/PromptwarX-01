from app.extensions.database import db
from app.models.roadmap import Roadmap
from app.models.task import Task
from app.services.ai_service import AIService

class RoadmapService:
    @staticmethod
    def generate_for_project(project):
        phases = AIService.generate_roadmap(project.title, project.description)
        Roadmap.query.filter_by(project_id=project.id).delete()
        Task.query.filter_by(project_id=project.id).delete()

        created = []
        for phase_data in phases:
            rm = Roadmap(
                project_id=project.id,
                phase_name=phase_data["phase_name"],
                phase_order=phase_data["phase_order"],
                description=phase_data.get("description")
            )
            db.session.add(rm)
            db.session.flush()

            t1 = Task(project_id=project.id, roadmap_id=rm.id, title=f"{rm.phase_name} - Requirements & Setup", priority="HIGH")
            t2 = Task(project_id=project.id, roadmap_id=rm.id, title=f"{rm.phase_name} - Core Implementation", priority="MEDIUM")
            db.session.add_all([t1, t2])
            created.append(rm)

        db.session.commit()
        return created

cat << 'EOF' > backend/app/services/mentor_service.py
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

cat << 'EOF' > backend/app/services/analysis_service.py
from app.extensions.database import db
from app.models.project_analysis import ProjectAnalysis
from app.services.ai_service import AIService

class AnalysisService:
    @staticmethod
    def analyze(project):
        data = AIService.analyze_project(project.to_dict())
        analysis = ProjectAnalysis(
            project_id=project.id,
            strengths=data.get("strengths"),
            weaknesses=data.get("weaknesses"),
            missing_features=data.get("missing_features"),
            technical_improvements=data.get("technical_improvements"),
            security_improvements=data.get("security_improvements"),
            scalability_improvements=data.get("scalability_improvements"),
            uiux_improvements=data.get("uiux_improvements"),
            overall_score=data.get("overall_score", 85.0)
        )
        db.session.add(analysis)
        db.session.commit()
        return analysis

cat << 'EOF' > backend/app/services/documentation_service.py
from app.extensions.database import db
from app.models.documentation import Documentation
from app.services.ai_service import AIService

class DocumentationService:
    @staticmethod
    def generate(project):
        sections = AIService.generate_documentation_outline(project.title)
        Documentation.query.filter_by(project_id=project.id).delete()
        docs = []
        for s in sections:
            doc = Documentation(project_id=project.id, section=s["section"], content=s["content"])
            db.session.add(doc)
            docs.append(doc)
        db.session.commit()
        return docs

cat << 'EOF' > backend/app/services/viva_service.py
from app.services.ai_service import AIService

class VivaService:
    @staticmethod
    def generate(project):
        return AIService.generate_viva_questions(project.title)
