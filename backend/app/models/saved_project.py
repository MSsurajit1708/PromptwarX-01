from datetime import datetime
import uuid
from app.extensions.database import db

class SavedProject(db.Model):
    __tablename__ = 'saved_projects'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    project_id = db.Column(db.String(36), db.ForeignKey('projects.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    project = db.relationship('Project')

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "project_id": self.project_id,
            "project": self.project.to_dict() if self.project else None,
            "created_at": self.created_at.isoformat()
        }
