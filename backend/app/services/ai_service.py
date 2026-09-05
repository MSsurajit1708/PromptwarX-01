import os
import json
import requests
from app.ai.parser import AIParser
from app.ai.prompts.project_prompt import build_project_generation_prompt
from app.ai.prompts.feature_prompt import build_feature_generation_prompt
from app.ai.prompts.roadmap_prompt import build_roadmap_prompt
from app.ai.prompts.architecture_prompt import build_architecture_prompt
from app.ai.prompts.database_prompt import build_database_prompt
from app.ai.prompts.analysis_prompt import build_analysis_prompt
from app.ai.prompts.mentor_prompt import build_mentor_prompt
from app.ai.prompts.documentation_prompt import build_documentation_prompt
from app.ai.prompts.viva_prompt import build_viva_prompt
from app.ai.prompts.career_prompt import build_career_prompt

class AIService:
    @staticmethod
    def _call_llm(prompt, system_instruction=""):
        api_key = os.getenv("AI_API_KEY") or os.getenv("GEMINI_API_KEY")
        if not api_key:
            return None
        
        model_name = os.getenv("AI_MODEL", "gemini-1.5-flash")
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
        headers = {"Content-Type": "application/json"}
        payload = {
            "contents": [{"parts": [{"text": f"{system_instruction}\n\n{prompt}"}]}],
            "generationConfig": {"response_mime_type": "application/json"}
        }

        try:
            resp = requests.post(url, json=payload, headers=headers, timeout=12)
            if resp.status_code == 200:
                data = resp.json()
                text = data['candidates'][0]['content']['parts'][0]['text']
                return AIParser.parse_json(text)
        except Exception as e:
            print(f"[AIService Warning] LLM call failed or timed out: {e}")
        return None

    @classmethod
    def generate_projects(cls, profile_data):
        prompt = build_project_generation_prompt(profile_data)
        llm_res = cls._call_llm(prompt, "You are ProjectMentor AI. Return a JSON array of projects.")
        if llm_res and isinstance(llm_res, list):
            return llm_res

        skills = profile_data.get("skills", ["Python", "JavaScript"])
        branch = profile_data.get("branch", "Computer Science & Engineering")
        
        return [
            {
                "title": "AI-Powered Patient Health Risk Assessment System",
                "description": "An intelligent predictive health monitoring web app that analyzes vital parameters to detect early risk markers.",
                "problem_statement": "Preventative healthcare lacks real-time risk assessment tools for non-clinical settings.",
                "solution": "Integrate Random Forest & XGBoost predictive models with a React dashboard and Flask REST API.",
                "domain": "Healthcare Tech",
                "difficulty": "Intermediate",
                "duration": "8 weeks",
                "target_users": ["Patients", "General Practitioners", "Health Counselors"],
                "technologies": ["Python", "Flask", "Scikit-learn", "React", "PostgreSQL"],
                "core_features": ["User Registration & Medical Vitals Form", "Real-time Risk Score Calculation", "Interactive Health Analytics Dashboard"],
                "advanced_features": ["Automated Doctor Appointment Scheduling", "PDF Medical Report Generator", "Wearable API Integration"],
                "innovation_score": 88,
                "feasibility_score": 92,
                "career_relevance_score": 95,
                "reason_for_recommendation": f"Matches your branch ({branch}) and skills in {', '.join(skills[:3])}."
            },
            {
                "title": "Smart Campus Placement & Skill Gap Analyzer",
                "description": "A web application that maps student academic skills against industry job descriptions to highlight skill gaps.",
                "problem_statement": "Students struggle to identify missing skills required for placement drives.",
                "solution": "Use NLP TF-IDF cosine similarity to match student resumes with live tech job descriptions.",
                "domain": "EduTech",
                "difficulty": "Intermediate",
                "duration": "6 weeks",
                "target_users": ["College Students", "Placement Officers", "Campus Recruiters"],
                "technologies": ["Python", "Flask", "React", "PostgreSQL", "Pandas"],
                "core_features": ["Resume Parsing & Skill Extraction", "Job Description Similarity Matching", "Personalized Skill Learning Checklist"],
                "advanced_features": ["Mock Technical Quiz Generator", "Peer Resume Comparison Engine", "Interview Preparation Assistant"],
                "innovation_score": 84,
                "feasibility_score": 94,
                "career_relevance_score": 96,
                "reason_for_recommendation": "Highly relevant for final-year placement prep and software engineering roles."
            },
            {
                "title": "Distributed Task Scheduler & Workload Monitor",
                "description": "A lightweight distributed backend service that queues, monitors, and executes background asynchronous jobs.",
                "problem_statement": "Small-scale startups need simple, resilient task queues without high Redis/Celery operational overhead.",
                "solution": "Build custom HTTP worker pools with SQLite/PostgreSQL transaction locks and clean web UI dashboard.",
                "domain": "Cloud & Systems",
                "difficulty": "Hard",
                "duration": "8-10 weeks",
                "target_users": ["Backend Developers", "DevOps Engineers"],
                "technologies": ["Python", "Flask", "PostgreSQL", "Docker", "React"],
                "core_features": ["Job Queue API", "Worker Pool Node Registration", "Real-time Metrics Dashboard"],
                "advanced_features": ["Automatic Retry Exponential Backoff", "Slack Alert Webhook Integration", "Worker Heartbeat Monitor"],
                "innovation_score": 90,
                "feasibility_score": 86,
                "career_relevance_score": 92,
                "reason_for_recommendation": "Demonstrates deep backend architecture, queue management, and systems design skills."
            }
        ]

    @classmethod
    def generate_features(cls, title, description):
        prompt = build_feature_generation_prompt(title, description)
        llm_res = cls._call_llm(prompt)
        if llm_res and isinstance(llm_res, dict):
            return llm_res
        return {
            "mvp": ["Secure User Authentication", "Core Data Ingest Pipeline", "Interactive Dashboard Widget"],
            "intermediate": ["Filtered Search & Sort", "Export Analytics to CSV/PDF", "Role-based Access Control"],
            "advanced": ["Predictive ML Forecast Module", "Webhook Alert Integration", "Real-time WebSocket Updates"],
            "future": ["Mobile App Companion", "Multi-tenant Enterprise Support", "Federated Learning Sync"]
        }

    @classmethod
    def generate_technologies(cls, title, description):
        return {
            "frontend": [{"name": "React / Next.js", "category": "UI Framework", "reason": "Fast responsive rendering and component modularity.", "required": True}],
            "backend": [{"name": "Python + Flask", "category": "REST API", "reason": "Rapid endpoint development and seamless AI/ML library support.", "required": True}],
            "database": [{"name": "PostgreSQL", "category": "Relational DB", "reason": "ACID compliance, schema validation, and relational integrity.", "required": True}],
            "aiml": [{"name": "Scikit-learn / Google Gemini", "category": "Machine Learning", "reason": "Classification, NLP extraction, and generative AI advice.", "required": True}],
            "devops": [{"name": "Docker & Gunicorn", "category": "Deployment", "reason": "Containerization and production WSGI concurrency.", "required": False}]
        }

    @classmethod
    def generate_architecture(cls, title, technologies):
        return {
            "architecture_type": "Modular 3-Tier Client-Server Monolith with AI Service Integration",
            "components": ["React SPA Frontend", "Flask REST API Gateway", "Authentication & Business Logic Layer", "AI/ML Service Pipeline", "PostgreSQL Relational DB"],
            "data_flow": "User -> React UI -> HTTPS -> Flask Controller -> Business Logic -> AI Model / DB -> JSON Response",
            "communication_flow": "RESTful JSON APIs over HTTPS with JWT Bearer Token Authorization",
            "explanation": "Decoupled architecture separating presentation from data storage and LLM inference.",
            "scalability_considerations": "Stateless REST API allows horizontal scaling behind Nginx/Gunicorn load balancers."
        }

    @classmethod
    def generate_database_design(cls, title, description):
        return {
            "database_type": "PostgreSQL (Relational)",
            "tables": [
                {"name": "users", "fields": ["id (UUID, PK)", "name (VARCHAR)", "email (VARCHAR, UNIQUE)", "password_hash (VARCHAR)", "created_at (TIMESTAMP)"]},
                {"name": "projects", "fields": ["id (UUID, PK)", "owner_id (UUID, FK -> users.id)", "title (VARCHAR)", "description (TEXT)", "status (VARCHAR)", "created_at (TIMESTAMP)"]},
                {"name": "tasks", "fields": ["id (UUID, PK)", "project_id (UUID, FK -> projects.id)", "title (VARCHAR)", "status (VARCHAR)", "priority (VARCHAR)"]}
            ],
            "relationships": ["User 1 -> N Projects", "Project 1 -> N Tasks", "Project 1 -> N Roadmaps"],
            "index_recommendations": ["CREATE INDEX idx_users_email ON users(email);", "CREATE INDEX idx_projects_owner ON projects(owner_id);"]
        }

    @classmethod
    def generate_roadmap(cls, project_title, description):
        prompt = build_roadmap_prompt(project_title, description)
        llm_res = cls._call_llm(prompt)
        if llm_res and isinstance(llm_res, list):
            return llm_res
        return [
            {"phase_name": "Phase 1 — Research & Requirement Gathering", "phase_order": 1, "description": "Define scope, map target users, conduct literature review."},
            {"phase_name": "Phase 2 — System Architecture & Database Design", "phase_order": 2, "description": "Create ER-Diagrams, API contracts, and component layout."},
            {"phase_name": "Phase 3 — Core Backend & API Development", "phase_order": 3, "description": "Build Flask routes, ORM models, and authentication logic."},
            {"phase_name": "Phase 4 — Frontend UI/UX Integration", "phase_order": 4, "description": "Connect React UI screens with backend REST API endpoints."},
            {"phase_name": "Phase 5 — AI/ML Model Integration & Testing", "phase_order": 5, "description": "Train, evaluate, and embed predictive models into business logic."},
            {"phase_name": "Phase 6 — Testing, Security Audit & Deployment", "phase_order": 6, "description": "Run pytest suite, set up Docker container, deploy live preview."}
        ]

    @classmethod
    def chat_mentor(cls, project_title, user_message, history=[]):
        prompt = build_mentor_prompt(project_title, user_message, project_title, history)
        llm_res = cls._call_llm(prompt)
        if llm_res and isinstance(llm_res, str):
            return llm_res
        return f"Regarding '{project_title}': To solve ('{user_message}'), I recommend: 1) Verify your database model schemas, 2) Test the REST API endpoint using cURL/Postman, and 3) Connect your React component state to handle loading and error states cleanly."

    @classmethod
    def analyze_project(cls, project_dict):
        prompt = build_analysis_prompt(project_dict)
        llm_res = cls._call_llm(prompt)
        if llm_res and isinstance(llm_res, dict):
            return llm_res
        return {
            "strengths": ["Clear problem statement", "Practical technology choices", "High career relevance"],
            "weaknesses": ["Needs automated integration test coverage", "Requires rate-limiting on API endpoints"],
            "missing_features": ["User notification digest", "Export report to PDF"],
            "technical_improvements": ["Implement Redis caching for frequent queries", "Use Docker for consistent deployments"],
            "security_improvements": ["Add CSRF protection", "Sanitize all user inputs before SQL execution"],
            "scalability_improvements": ["Decouple worker task execution", "Set up database connection pooling"],
            "uiux_improvements": ["Add loading skeleton screens", "Improve mobile responsiveness"],
            "overall_score": 85.0
        }

    @classmethod
    def generate_viva_questions(cls, project_title):
        prompt = build_viva_prompt(project_title)
        llm_res = cls._call_llm(prompt)
        if llm_res and isinstance(llm_res, list):
            return llm_res
        return [
            {"category": "Basic", "difficulty": "Easy", "question": f"What inspired you to build {project_title}?", "suggested_answer": "The primary goal was solving real-world inefficiencies through an automated digital system."},
            {"category": "Technical", "difficulty": "Medium", "question": "How did you manage authentication and state in your application?", "suggested_answer": "We implemented stateless JWT tokens stored securely and validated on protected backend endpoints."},
            {"category": "Database", "difficulty": "Medium", "question": "Why did you choose PostgreSQL over a NoSQL database?", "suggested_answer": "PostgreSQL provides strict schema constraints, foreign key referential integrity, and efficient relational querying."}
        ]

    @classmethod
    def generate_documentation_outline(cls, project_title):
        prompt = build_documentation_prompt(project_title)
        llm_res = cls._call_llm(prompt)
        if llm_res and isinstance(llm_res, list):
            return llm_res
        return [
            {"section": "1. Abstract", "content": f"This project presents {project_title}, designed to address critical industry challenges."},
            {"section": "2. Introduction & Problem Statement", "content": "Detailed overview of background context, objective, and proposed methodology."},
            {"section": "3. System Architecture & Database Design", "content": "Comprehensive breakdown of components, data flow, ER-diagrams, and API schemas."},
            {"section": "4. Implementation & Testing Results", "content": "Code structure details, unit testing results, and system performance benchmarks."}
        ]

    @classmethod
    def analyze_career_value(cls, title, technologies):
        return {
            "skills_demonstrated": ["REST API Architecture", "Database Modeling", "Applied AI/ML Engineering", "JWT Authentication"],
            "technologies_learned": technologies,
            "resume_bullets": [
                f"Architected and deployed {title}, an end-to-end full-stack platform using {', '.join(technologies[:3])}.",
                "Implemented deterministic scoring algorithms and integrated Google Gemini LLMs for automated technical workflows.",
                "Built secure JWT authorization pipelines with relational data persistence in PostgreSQL."
            ],
            "github_readme_pitch": f"### {title}\nAn intelligent, production-ready fullstack web platform for academic and career project acceleration.",
            "interview_talking_points": [
                "How I handled AI prompt engineering and structured JSON validation.",
                "How I designed the database schema to ensure referential integrity and fast queries.",
                "Challenges faced in testing, authentication, and cloud deployment."
            ]
        }
