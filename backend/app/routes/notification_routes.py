from flask import Blueprint, g
from app.extensions.database import db
from app.models.notification import Notification
from app.utils.helpers import success_response
from app.middleware.auth_middleware import jwt_required

notif_bp = Blueprint('notification', __name__, url_prefix='/api/v1/notifications')

@notif_bp.route('', methods=['GET'])
@jwt_required
def get_notifications():
    notifications = Notification.query.filter_by(user_id=g.current_user.id).order_by(Notification.created_at.desc()).all()
    return success_response([n.to_dict() for n in notifications])

@notif_bp.route('/read-all', methods=['POST'])
@jwt_required
def mark_all_read():
    Notification.query.filter_by(user_id=g.current_user.id).update({"is_read": True})
    db.session.commit()
    return success_response(None, "All notifications marked as read")
