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
