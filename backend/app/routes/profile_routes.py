from flask import Blueprint, request, g
from app.extensions.database import db
from app.models.profile import Profile
from app.models.skill import Skill
from app.models.interest import Interest
from app.utils.helpers import success_response, error_response
from app.middleware.auth_middleware import jwt_required

profile_bp = Blueprint('profile', __name__, url_prefix='/api/v1')

@profile_bp.route('/profile', methods=['GET'])
@jwt_required
def get_profile():
    profile = Profile.query.filter_by(user_id=g.current_user.id).first()
    if not profile:
        profile = Profile(user_id=g.current_user.id)
        db.session.add(profile)
        db.session.commit()
    return success_response(profile.to_dict())

@profile_bp.route('/profile', methods=['PUT'])
@jwt_required
def update_profile():
    data = request.get_json() or {}
    profile = Profile.query.filter_by(user_id=g.current_user.id).first()
    if not profile:
        profile = Profile(user_id=g.current_user.id)
        db.session.add(profile)

    profile.college = data.get('college', profile.college)
    profile.degree = data.get('degree', profile.degree)
    profile.branch = data.get('branch', profile.branch)
    profile.semester = data.get('semester', profile.semester)
    profile.specialization = data.get('specialization', profile.specialization)
    profile.academic_year = data.get('academic_year', profile.academic_year)
    profile.experience_level = data.get('experience_level', profile.experience_level)
    profile.career_goal = data.get('career_goal', profile.career_goal)
    profile.project_preference = data.get('project_preference', profile.project_preference)
    profile.available_time = data.get('available_time', profile.available_time)
    profile.team_size = data.get('team_size', profile.team_size)

    # Update skills
    skill_names = data.get('skills', [])
    if skill_names:
        skills = []
        for name in skill_names:
            skill = Skill.query.filter_by(name=name).first()
            if not skill:
                skill = Skill(name=name)
                db.session.add(skill)
            skills.append(skill)
        profile.skills = skills

    # Update interests
    interest_names = data.get('interests', [])
    if interest_names:
        interests = []
        for name in interest_names:
            interest = Interest.query.filter_by(name=name).first()
            if not interest:
                interest = Interest(name=name)
                db.session.add(interest)
            interests.append(interest)
        profile.interests = interests

    db.session.commit()
    return success_response(profile.to_dict(), "Profile updated successfully")
