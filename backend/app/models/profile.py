from datetime import datetime
import uuid
from app.extensions.database import db

profile_skills = db.Table('profile_skills',
    db.Column('profile_id', db.String(36), db.ForeignKey('profiles.id'), primary_key=True),
    db.Column('skill_id', db.String(36), db.ForeignKey('skills.id'), primary_key=True)
)

profile_interests = db.Table('profile_interests',
    db.Column('profile_id', db.String(36), db.ForeignKey('profiles.id'), primary_key=True),
    db.Column('interest_id', db.String(36), db.ForeignKey('interests.id'), primary_key=True)
)

class Profile(db.Model):
    __tablename__ = 'profiles'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False, unique=True)
    college = db.Column(db.String(150), nullable=True)
    degree = db.Column(db.String(100), nullable=True)
    branch = db.Column(db.String(100), nullable=True)
    semester = db.Column(db.Integer, nullable=True)
    specialization = db.Column(db.String(100), nullable=True)
    academic_year = db.Column(db.String(20), nullable=True)
    experience_level = db.Column(db.String(50), nullable=True)
    career_goal = db.Column(db.String(100), nullable=True)
    project_preference = db.Column(db.String(100), nullable=True)
    available_time = db.Column(db.String(50), nullable=True)
    team_size = db.Column(db.String(20), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    skills = db.relationship('Skill', secondary=profile_skills, backref='profiles')
    interests = db.relationship('Interest', secondary=profile_interests, backref='profiles')

    def calculate_completion(self):
        score = 0
        if self.college and self.degree: score += 20
        if self.branch and self.semester: score += 20
        if self.skills: score += 20
        if self.interests: score += 15
        if self.career_goal: score += 15
        if self.project_preference: score += 10
        return score

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "college": self.college,
            "degree": self.degree,
            "branch": self.branch,
            "semester": self.semester,
            "specialization": self.specialization,
            "academic_year": self.academic_year,
            "experience_level": self.experience_level,
            "career_goal": self.career_goal,
            "project_preference": self.project_preference,
            "available_time": self.available_time,
            "team_size": self.team_size,
            "completion_percentage": self.calculate_completion(),
            "skills": [s.to_dict() for s in self.skills],
            "interests": [i.to_dict() for i in self.interests]
        }
