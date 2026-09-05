import pytest
from app import create_app
from app.extensions.database import db

@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_health_check(client):
    res = client.get('/health')
    assert res.status_code == 200
    data = res.get_json()
    assert data['status'] == 'healthy'
    assert data['database'] == 'connected'

def test_user_registration_login_and_profile(client):
    # 1. Register User
    reg_res = client.post('/api/v1/auth/register', json={
        "name": "Audit Student",
        "email": "auditstudent@example.com",
        "password": "Password123"
    })
    assert reg_res.status_code == 201
    token = reg_res.get_json()['data']['token']

    # 2. Get Me
    me_res = client.get('/api/v1/auth/me', headers={"Authorization": f"Bearer {token}"})
    assert me_res.status_code == 200
    assert me_res.get_json()['data']['email'] == "auditstudent@example.com"

    # 3. Update Profile
    prof_res = client.put('/api/v1/profile', json={
        "college": "Parul University",
        "degree": "B.Tech",
        "branch": "AI & Machine Learning",
        "semester": 7,
        "skills": ["Python", "Flask", "React", "PostgreSQL"],
        "interests": ["Healthcare Tech", "AI/ML"],
        "career_goal": "AI/ML Engineer"
    }, headers={"Authorization": f"Bearer {token}"})
    assert prof_res.status_code == 200
    assert prof_res.get_json()['data']['branch'] == "AI & Machine Learning"

def test_complete_project_lifecycle(client):
    # Login Demo Student
    login_res = client.post('/api/v1/auth/login', json={
        "email": "student@projectmentor.ai",
        "password": "Student@123"
    })
    token = login_res.get_json()['data']['token']
    headers = {"Authorization": f"Bearer {token}"}

    # 1. Generate Recommendations
    gen_res = client.post('/api/v1/projects/generate', json={
        "skills": ["Python", "Flask", "React"],
        "interests": ["Healthcare Tech"],
        "branch": "Computer Science",
        "career_goal": "AI/ML Engineer"
    }, headers=headers)
    assert gen_res.status_code == 200
    projects = gen_res.get_json()['data']['projects']
    assert len(projects) > 0
    assert projects[0]['overall_score'] > 0

    # 2. Select / Create Project
    create_res = client.post('/api/v1/projects', json={
        "title": "AI Patient Risk Monitor",
        "description": "Real-time vitals monitoring web app.",
        "domain": "Healthcare",
        "difficulty": "Intermediate",
        "technologies": ["Python", "Flask", "React"]
    }, headers=headers)
    assert create_res.status_code == 201
    project_id = create_res.get_json()['data']['id']

    # 3. Generate Roadmap
    rm_res = client.post(f'/api/v1/projects/{project_id}/roadmap/generate', headers=headers)
    assert rm_res.status_code == 200
    roadmaps = rm_res.get_json()['data']
    assert len(roadmaps) > 0

    # 4. Tasks Management
    tasks_res = client.get(f'/api/v1/projects/{project_id}/tasks', headers=headers)
    assert tasks_res.status_code == 200
    tasks = tasks_res.get_json()['data']
    assert len(tasks) > 0

    task_id = tasks[0]['id']
    status_res = client.patch(f'/api/v1/tasks/{task_id}/status', json={"status": "COMPLETED"}, headers=headers)
    assert status_res.status_code == 200
    assert status_res.get_json()['data']['status'] == "COMPLETED"

    # 5. Mentor Chat
    chat_res = client.post(f'/api/v1/projects/{project_id}/mentor/chat', json={
        "message": "How do I structure the backend Flask app?"
    }, headers=headers)
    assert chat_res.status_code == 200
    assert "assistant_message" in chat_res.get_json()['data']

    # 6. Project Analysis & Viva Prep
    analyze_res = client.post(f'/api/v1/projects/{project_id}/analyze', headers=headers)
    assert analyze_res.status_code == 200
    assert analyze_res.get_json()['data']['overall_score'] > 0

    viva_res = client.post(f'/api/v1/projects/{project_id}/viva/generate', headers=headers)
    assert viva_res.status_code == 200
    assert len(viva_res.get_json()['data']['questions']) > 0

def test_admin_endpoints(client):
    # Login Admin
    login_res = client.post('/api/v1/auth/login', json={
        "email": "admin@projectmentor.ai",
        "password": "Admin@123"
    })
    token = login_res.get_json()['data']['token']
    headers = {"Authorization": f"Bearer {token}"}

    users_res = client.get('/api/v1/admin/users', headers=headers)
    assert users_res.status_code == 200
    assert len(users_res.get_json()['data']) >= 2

    analytics_res = client.get('/api/v1/admin/analytics', headers=headers)
    assert analytics_res.status_code == 200
    assert analytics_res.get_json()['data']['platform_status'] == 'healthy'
