import uuid
from app.extensions.database import db

class Roadmap(db.Model):
    __tablename__ = 'roadmaps'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = db.Column(db.String(36), db.ForeignKey('projects.id'), nullable=False)
    phase_name = db.Column(db.String(100), nullable=False)
    phase_order = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=True)

    tasks = db.relationship('Task', backref='roadmap', cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "project_id": self.project_id,
            "phase_name": self.phase_name,
            "phase_order": self.phase_order,
            "description": self.description,
            "tasks": [t.to_dict() for t in self.tasks]
        }
