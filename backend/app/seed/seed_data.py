from app.extensions.database import db
from app.models.user import User
from app.models.profile import Profile
from app.models.skill import Skill
from app.models.interest import Interest
from app.models.project import Project
from app.models.task import Task
from app.models.notification import Notification

def seed_database():
    if User.query.filter_by(email="student@projectmentor.ai").first():
        return # Already seeded

    print("[Seed] Seeding database with demo student, admin, skills & sample project...")

    # Create Skills
    skills_list = ["Python", "JavaScript", "React", "Flask", "PostgreSQL", "Scikit-learn", "Docker", "Git", "HTML/CSS"]
    skill_objs = []
    for s_name in skills_list:
        sk = Skill(name=s_name, category="Tech")
        db.session.add(sk)
        skill_objs.append(sk)

    # Create Interests
    interests_list = ["Artificial Intelligence", "Healthcare Tech", "Web Development", "Cloud Computing"]
    interest_objs = []
    for i_name in interests_list:
        it = Interest(name=i_name, category="Domain")
        db.session.add(it)
        interest_objs.append(it)

    db.session.flush()

    # Create Demo Student
    student = User(name="Demo Student", email="student@projectmentor.ai", role="student")
    student.set_password("Student@123")
    db.session.add(student)

    # Create Demo Admin
    admin = User(name="Platform Admin", email="admin@projectmentor.ai", role="admin")
    admin.set_password("Admin@123")
    db.session.add(admin)

    db.session.flush()

    # Student Profile
    profile = Profile(
        user_id=student.id,
        college="Institute of Technology",
        degree="B.Tech",
        branch="AI & Machine Learning",
        semester=7,
        specialization="Data Science",
        academic_year="2026",
        experience_level="Intermediate",
        career_goal="AI/ML Engineer",
        project_preference="Individual",
        available_time="8 weeks",
        team_size="1"
    )
    profile.skills = skill_objs[:5]
    profile.interests = interest_objs[:2]
    db.session.add(profile)

    # Demo Project
    demo_proj = Project(
        owner_id=student.id,
        title="AI-Powered Student Performance Prediction System",
        description="Predictive web application that identifies students needing academic assistance.",
        problem_statement="Educational institutions lack early warning detection systems.",
        proposed_solution="Machine learning predictive model integrated with real-time student analytics portal.",
        domain="Healthcare & EduTech",
        difficulty="Intermediate",
        duration="8 weeks",
        overall_score=89.5,
        technologies=["Python", "Flask", "React", "Scikit-learn", "PostgreSQL"],
        target_users=["Students", "Academic Advisors", "Faculty"]
    )
    db.session.add(demo_proj)
    db.session.flush()

    # Tasks for demo project
    t1 = Task(project_id=demo_proj.id, title="Formulate Problem Statement & Objectives", status="COMPLETED", priority="HIGH")
    t2 = Task(project_id=demo_proj.id, title="Build Flask Backend REST API", status="IN_PROGRESS", priority="HIGH")
    t3 = Task(project_id=demo_proj.id, title="Train Scikit-learn Classifier Model", status="NOT_STARTED", priority="MEDIUM")
    db.session.add_all([t1, t2, t3])

    # Notification
    n1 = Notification(user_id=student.id, title="Welcome to ProjectMentor AI", message="Your demo student account is ready. Explore your personalized projects!", type="SYSTEM")
    db.session.add(n1)

    db.session.commit()
    print("[Seed] Seeding completed successfully.")
