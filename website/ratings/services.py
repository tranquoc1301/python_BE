from flask import request, jsonify, abort
from ..db import db
from ..library_ma import RatingSchema
from ..models import Rating
from sqlalchemy.exc import IntegrityError

rating_schema = RatingSchema()
ratings_schema = RatingSchema(many=True)


def add_rating_service():
    data = request.get_json()

    errors = rating_schema.validate(data)
    if errors:
        return jsonify({"errors": errors}), 400

    # Kiểm tra rating có trong khoảng 1-5
    rating_value = data.get('rating')
    if rating_value < 1 or rating_value > 5:
        return jsonify({"error": "Rating must be between 1 and 5."}), 400

    try:
        new_rating = Rating(
            book_id=data.get('book_id'),
            student_id=data.get('student_id'),
            rating=rating_value,
            comment=data.get('comment')
        )

        db.session.add(new_rating)
        db.session.commit()
        return jsonify(rating_schema.dump(new_rating)), 201

    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Rating for this book by this student already exists."}), 409
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500


def get_all_ratings_service(book_id: int):
    ratings = Rating.query.filter_by(book_id=book_id).all()
    return jsonify(ratings_schema.dump(ratings)), 200


def update_rating_service(book_id: int, student_id: str):
    rating = Rating.query.filter_by(
        book_id=book_id, student_id=student_id).first()
    if not rating:
        abort(404, description="Rating not found")

    data = request.get_json()

    errors = rating_schema.validate(data)
    if errors:
        return jsonify({"errors": errors}), 400

    # Cập nhật rating
    rating_value = data.get('rating')
    if rating_value and (rating_value < 1 or rating_value > 5):
        return jsonify({"error": "Rating must be between 1 and 5."}), 400

    try:
        if rating_value:
            rating.rating = rating_value
        if 'comment' in data:
            rating.comment = data['comment']

        db.session.commit()
        return jsonify(rating_schema.dump(rating)), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500


def delete_rating_service(book_id: int, student_id: str):
    rating = Rating.query.filter_by(
        book_id=book_id, student_id=student_id).first()
    if not rating:
        abort(404, description="Rating not found")

    try:
        db.session.delete(rating)
        db.session.commit()
        return jsonify({"message": "Rating deleted successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500
