from app.services.ai_service import AIService
from app.services.scoring_service import ScoringService
from app.models.generated_project import GeneratedProject
from app.extensions.database import db

class ProjectGenerationService:
    @staticmethod
    def generate_and_score(user_id, profile_dict, overrides=None):
        overrides = overrides or {}
        merged_profile = {
            "skills": overrides.get("skills") or [s["name"] for s in profile_dict.get("skills", [])],
            "interests": overrides.get("interests") or [i["name"] for i in profile_dict.get("interests", [])],
            "branch": overrides.get("branch") or profile_dict.get("branch", "Computer Science & Engineering"),
            "careerGoal": overrides.get("career_goal") or profile_dict.get("career_goal", "Software Developer"),
            "experience": overrides.get("experience_level") or profile_dict.get("experience_level", "Intermediate"),
            "difficulty": overrides.get("difficulty", "Intermediate"),
            "duration": overrides.get("duration", "8 weeks")
        }

        raw_projects = AIService.generate_projects(merged_profile)
        scored_projects = []

        for proj in raw_projects:
            scores = ScoringService.calculate_project_score(proj, merged_profile)
            proj.update(scores)
            scored_projects.append(proj)

        scored_projects.sort(key=lambda x: x.get("overall_score", 0), reverse=True)

        gen_record = GeneratedProject(
            user_id=user_id,
            generation_request=merged_profile,
            project_data=scored_projects,
            recommendation_score=scored_projects[0]["overall_score"] if scored_projects else 0.0
        )
        db.session.add(gen_record)
        db.session.commit()

        return scored_projects, gen_record.id
