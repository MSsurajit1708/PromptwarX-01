import uuid
from app.extensions.database import db

class ProjectFeature(db.Model):
    __tablename__ = 'project_features'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = db.Column(db.String(36), db.ForeignKey('projects.id'), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(50), nullable=False, default='MVP') # MVP, INTERMEDIATE, ADVANCED, FUTURE
    priority = db.Column(db.String(20), default='MEDIUM')
    status = db.Column(db.String(20), default='PLANNED')

    def to_dict(self):
        return {
            "id": self.id,
            "project_id": self.project_id,
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "priority": self.priority,
            "status": self.status
        }
