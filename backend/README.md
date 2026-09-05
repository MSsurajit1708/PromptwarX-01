# ProjectMentor AI - Flask REST API Backend

Production-ready, modular Flask REST API backend for **ProjectMentor AI**, providing student profile management, AI-driven project idea generation, scoring, roadmaps, interactive task tracking, AI mentor chatbot, quality analysis, viva preparation, and admin analytics.

## Tech Stack
* **Language:** Python 3.11+ / 3.14
* **Framework:** Flask 3.1
* **Database:** PostgreSQL (SQLAlchemy ORM, SQLite zero-config fallback)
* **Auth:** JWT (`PyJWT` / `Flask-JWT-Extended`) with Werkzeug password hashing
* **Testing:** Pytest
* **Server:** Gunicorn

## Quick Start (Local Run)

```bash
# 1. Navigate to backend directory
cd backend

# 2. Activate virtual environment
source venv/bin/activate  # on macOS/Linux

# 3. Set environment variables & start server
export PYTHONPATH=.
python3 run.py
```
The Flask API server will start on **http://127.0.0.1:5000** (or http://0.0.0.0:5000).

## Pre-seeded Demo Credentials
* **Demo Student:** `student@projectmentor.ai` / `Student@123`
* **Demo Admin:** `admin@projectmentor.ai` / `Admin@123`

## Running Automated Tests
```bash
PYTHONPATH=backend backend/venv/bin/pytest backend/tests
```

## Core API Endpoints

### 1. Health & Health Check
* `GET /health` -> `{"status": "healthy", "database": "connected"}`

### 2. Authentication
* `POST /api/v1/auth/register`
* `POST /api/v1/auth/login`
* `GET /api/v1/auth/me` (Protected)

### 3. Student Profile
* `GET /api/v1/profile` (Protected)
* `PUT /api/v1/profile` (Protected)

### 4. AI Project Generation & Scoring
* `POST /api/v1/projects/generate` (Protected)
* `GET /api/v1/projects` (Protected)
* `POST /api/v1/projects` (Select & Save project workspace)

### 5. Roadmaps & Tasks
* `POST /api/v1/projects/<id>/roadmap/generate` (Protected)
* `GET /api/v1/projects/<id>/tasks` (Protected)
* `PATCH /api/v1/tasks/<task_id>/status` (Protected)

### 6. AI Mentor Chat & Analysis
* `POST /api/v1/projects/<id>/mentor/chat` (Protected)
* `POST /api/v1/projects/<id>/analyze` (Protected)
* `POST /api/v1/projects/<id>/viva/generate` (Protected)

### 7. Admin & Analytics
* `GET /api/v1/admin/users` (Admin Only)
* `GET /api/v1/admin/analytics` (Admin Only)
