from datetime import datetime
import uuid
from app.extensions.database import db

class Project(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    owner_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    problem_statement = db.Column(db.Text, nullable=True)
    proposed_solution = db.Column(db.Text, nullable=True)
    domain = db.Column(db.String(100), nullable=True)
    difficulty = db.Column(db.String(50), nullable=True)
    duration = db.Column(db.String(50), nullable=True)
    status = db.Column(db.String(50), default='ACTIVE')
    overall_score = db.Column(db.Float, default=0.0)
    technologies = db.Column(db.JSON, nullable=True)
    target_users = db.Column(db.JSON, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    features = db.relationship('ProjectFeature', backref='project', cascade="all, delete-orphan")
    roadmaps = db.relationship('Roadmap', backref='project', cascade="all, delete-orphan")
    tasks = db.relationship('Task', backref='project', cascade="all, delete-orphan")
    chat_messages = db.relationship('ChatMessage', backref='project', cascade="all, delete-orphan")
    analyses = db.relationship('ProjectAnalysis', backref='project', cascade="all, delete-orphan")
    documentations = db.relationship('Documentation', backref='project', cascade="all, delete-orphan")

    def to_dict(self):
        completed = sum(1 for t in self.tasks if t.status == 'COMPLETED')
        total = len(self.tasks)
        progress = round((completed / total * 100), 1) if total > 0 else 0.0

        return {
            "id": self.id,
            "owner_id": self.owner_id,
            "title": self.title,
            "description": self.description,
            "problem_statement": self.problem_statement,
            "proposed_solution": self.proposed_solution,
            "domain": self.domain,
            "difficulty": self.difficulty,
            "duration": self.duration,
            "status": self.status,
            "overall_score": self.overall_score,
            "technologies": self.technologies or [],
            "target_users": self.target_users or [],
            "progress_percentage": progress,
            "completed_tasks": completed,
            "total_tasks": total,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
