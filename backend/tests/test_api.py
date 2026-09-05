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

def test_user_registration_and_login(client):
    # Register
    reg_res = client.post('/api/v1/auth/register', json={
        "name": "Test Student",
        "email": "teststudent@example.com",
        "password": "Password123"
    })
    assert reg_res.status_code == 201
    reg_data = reg_res.get_json()
    assert reg_data['success'] is True
    token = reg_data['data']['token']

    # Me Endpoint
    me_res = client.get('/api/v1/auth/me', headers={"Authorization": f"Bearer {token}"})
    assert me_res.status_code == 200
    assert me_res.get_json()['data']['email'] == "teststudent@example.com"

    # Login
    login_res = client.post('/api/v1/auth/login', json={
        "email": "teststudent@example.com",
        "password": "Password123"
    })
    assert login_res.status_code == 200
    assert "token" in login_res.get_json()['data']

def test_project_generation(client):
    # Login as demo student
    login_res = client.post('/api/v1/auth/login', json={
        "email": "student@projectmentor.ai",
        "password": "Student@123"
    })
    token = login_res.get_json()['data']['token']

    # Generate projects
    gen_res = client.post('/api/v1/projects/generate', json={
        "skills": ["Python", "Flask", "React"],
        "interests": ["Healthcare Tech"],
        "branch": "Computer Science",
        "career_goal": "AI/ML Engineer"
    }, headers={"Authorization": f"Bearer {token}"})

    assert gen_res.status_code == 200
    projects = gen_res.get_json()['data']['projects']
    assert len(projects) > 0
    assert "title" in projects[0]
    assert "overall_score" in projects[0]
