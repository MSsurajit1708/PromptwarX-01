from app.services.ai_service import AIService

class VivaService:
    @staticmethod
    def generate(project):
        return AIService.generate_viva_questions(project.title)
