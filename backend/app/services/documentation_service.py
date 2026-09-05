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
