from datetime import datetime
import uuid
from app.extensions.database import db

class GeneratedProject(db.Model):
    __tablename__ = 'generated_projects'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    generation_request = db.Column(db.JSON, nullable=False)
    project_data = db.Column(db.JSON, nullable=False)
    recommendation_score = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "project_data": self.project_data,
            "recommendation_score": self.recommendation_score,
            "created_at": self.created_at.isoformat()
        }
