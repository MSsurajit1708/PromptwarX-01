from datetime import datetime
import uuid
from app.extensions.database import db

class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = db.Column(db.String(36), db.ForeignKey('projects.id'), nullable=False)
    roadmap_id = db.Column(db.String(36), db.ForeignKey('roadmaps.id'), nullable=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    priority = db.Column(db.String(20), default='MEDIUM')
    status = db.Column(db.String(30), default='NOT_STARTED') # NOT_STARTED, IN_PROGRESS, COMPLETED, BLOCKED
    estimated_hours = db.Column(db.Integer, default=5)
    deadline = db.Column(db.DateTime, nullable=True)
    completed_at = db.Column(db.DateTime, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "project_id": self.project_id,
            "roadmap_id": self.roadmap_id,
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "status": self.status,
            "estimated_hours": self.estimated_hours,
            "deadline": self.deadline.isoformat() if self.deadline else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None
        }
