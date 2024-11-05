from flask import request, jsonify, abort
from ..db import db
from ..library_ma import CommentSchema
from ..models import Comments

comment_schema = CommentSchema()
comments_schema = CommentSchema(many=True)


def add_comment_service():
    data = request.get_json()

    errors = comment_schema.validate(data)
    if errors:
        return jsonify({"errors": errors}), 400

    try:
        new_comment = Comments(
            book_id=data.get('book_id'),
            student_id=data.get('student_id'),
            content=data.get('content')
        )

        db.session.add(new_comment)
        db.session.commit()
        return comment_schema.jsonify(new_comment), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500


def get_all_comments_service():
    comments = Comments.query.all()
    return comments_schema.jsonify(comments) if comments else jsonify({"message": "Empty comment list"}), 200


def get_comment_service(id):
    comment = Comments.query.get(id)
    if not comment:
        abort(404, description="Comment not found")
    return comment_schema.jsonify(comment)


def update_comment_service(id):
    comment = Comments.query.get(id)
    if not comment:
        abort(404, description="Comment not found")

    data = request.get_json()

    errors = comment_schema.validate(data)
    if errors:
        return jsonify({"errors": errors}), 400

    try:
        for key, value in data.items():
            if getattr(comment, key) != value:
                setattr(comment, key, value)

        db.session.add(comment)
        db.session.commit()
        return comment_schema.jsonify(comment), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500


def delete_comment_service(id):
    comment = Comments.query.get(id)
    if not comment:
        abort(404, description="Comment not found")

    try:
        db.session.delete(comment)
        db.session.commit()
        return jsonify({"message": "Comment deleted successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500
