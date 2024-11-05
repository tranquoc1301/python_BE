from flask import Blueprint
from .services import *

favorites = Blueprint('favorites', __name__)


@favorites.route('/favorites', methods=['GET'])
def get_all_favorite_books(student_id: str):
    return get_all_favorites_books_by_student_id_service(student_id)


@favorites.route('/favorites/<int:id>', methods=['GET'])
def get_favorite_by_id(id):
    return get_favorite_by_student_id_service(id)


@favorites.route('/favorites', methods=['POST'])
def add_favorite():
    return add_favorite_service()


@favorites.route('/favorite/<int:book_id>/<string:student_id>', methods=['DELETE'])
def delete_favorite_book_service(book_id, student_id):
    return delete_favorite_book_service(book_id, student_id)
