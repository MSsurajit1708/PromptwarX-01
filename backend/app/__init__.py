import os
from flask import Flask, jsonify
from app.config.settings import config_by_name
from app.extensions.database import db
from app.extensions.cors import cors
from app.middleware.error_handler import register_error_handlers
from app.seed.seed_data import seed_database

def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv("FLASK_ENV", "development")

    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    # Initialize Extensions
    db.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": app.config["CORS_ORIGINS"]}})

    # Register Blueprints
    from app.routes.auth_routes import auth_bp
    from app.routes.profile_routes import profile_bp
    from app.routes.project_routes import project_bp
    from app.routes.roadmap_routes import roadmap_bp
    from app.routes.task_routes import task_bp
    from app.routes.mentor_routes import mentor_bp
    from app.routes.analysis_routes import analysis_bp
    from app.routes.documentation_routes import doc_bp
    from app.routes.viva_routes import viva_bp
    from app.routes.saved_project_routes import saved_bp
    from app.routes.notification_routes import notif_bp
    from app.routes.admin_routes import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(project_bp)
    app.register_blueprint(roadmap_bp)
    app.register_blueprint(task_bp)
    app.register_blueprint(mentor_bp)
    app.register_blueprint(analysis_bp)
    app.register_blueprint(doc_bp)
    app.register_blueprint(viva_bp)
    app.register_blueprint(saved_bp)
    app.register_blueprint(notif_bp)
    app.register_blueprint(admin_bp)

    # Error Handlers
    register_error_handlers(app)

    # Health Check
    @app.route('/health', methods=['GET'])
    def health_check():
        return jsonify({
            "status": "healthy",
            "database": "connected",
            "version": "1.0.0"
        }), 200

    # Auto Create DB tables & Seed
    with app.app_context():
        db.create_all()
        seed_database()

    return app
