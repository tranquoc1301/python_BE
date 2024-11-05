from flask import request, jsonify, abort
from ..db import db
from ..library_ma import FavoriteSchema
from ..models import Favorite
from sqlalchemy.exc import IntegrityError

favorite_schema = FavoriteSchema()
favorites_schema = FavoriteSchema(many=True)


def add_favorite_service():
    data = request.get_json()

    # Validate dữ liệu
    errors = favorite_schema.validate(data)
    if errors:
        return jsonify({"errors": errors}), 400

    try:
        new_favorite = Favorite(
            book_id=data.get('book_id'),
            student_id=data.get('student_id')
        )

        db.session.add(new_favorite)
        db.session.commit()
        return jsonify(favorite_schema.dump(new_favorite)), 201

    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Favorite with this book and student already exists"}), 409
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500


def get_all_favorites_books_by_student_id_service(student_id: str):
    favorites = Favorite.query.filter_by(student_id=student_id).all()
    if not favorites:
        abort(404, description="No favorite book found for this student")
    return jsonify(favorites_schema.dump(favorites)), 200


def get_favorite_by_student_id_service(student_id: str):
    favorites = Favorite.query.filter_by(student_id=student_id).all()
    if not favorites:
        abort(404, description="No favorite book found for this student")
    return jsonify(favorites_schema.dump(favorites)), 200


def delete_favorite_book_service(book_id: int, student_id: str):
    favorite = Favorite.query.filter_by(
        book_id=book_id, student_id=student_id).first()
    if not favorite:
        abort(404, description="Favorite not found")

    try:
        db.session.delete(favorite)
        db.session.commit()
        return jsonify({"message": "Favorite deleted successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500
