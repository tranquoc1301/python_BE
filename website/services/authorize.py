from functools import wraps
from flask import request, jsonify, abort
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from ..models import Students


def role_required(required_role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            current_user_id = get_jwt_identity()
            student = Students.query.get(current_user_id)
            if not student:
                abort(401, description="Unauthorized user")
            if student.role != required_role:
                return jsonify({"message": "You do not have permission to access this resource"}), 403
            return func(*args, **kwargs)
        return wrapper
    return decorator
