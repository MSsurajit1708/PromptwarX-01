from datetime import datetime
import uuid
from app.extensions.database import db

class ProjectAnalysis(db.Model):
    __tablename__ = 'project_analyses'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = db.Column(db.String(36), db.ForeignKey('projects.id'), nullable=False)
    strengths = db.Column(db.JSON, nullable=True)
    weaknesses = db.Column(db.JSON, nullable=True)
    missing_features = db.Column(db.JSON, nullable=True)
    technical_improvements = db.Column(db.JSON, nullable=True)
    security_improvements = db.Column(db.JSON, nullable=True)
    scalability_improvements = db.Column(db.JSON, nullable=True)
    uiux_improvements = db.Column(db.JSON, nullable=True)
    overall_score = db.Column(db.Float, default=75.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "project_id": self.project_id,
            "strengths": self.strengths or [],
            "weaknesses": self.weaknesses or [],
            "missing_features": self.missing_features or [],
            "technical_improvements": self.technical_improvements or [],
            "security_improvements": self.security_improvements or [],
            "scalability_improvements": self.scalability_improvements or [],
            "uiux_improvements": self.uiux_improvements or [],
            "overall_score": self.overall_score,
            "created_at": self.created_at.isoformat()
        }
