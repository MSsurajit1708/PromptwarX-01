import uuid
from app.extensions.database import db

class Interest(db.Model):
    __tablename__ = 'interests'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), unique=True, nullable=False)
    category = db.Column(db.String(50), nullable=True)

    def to_dict(self):
        return {"id": self.id, "name": self.name, "category": self.category}
