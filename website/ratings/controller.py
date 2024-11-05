from flask import Blueprint
from .services import *

ratings = Blueprint('ratings', __name__)


@ratings.route('/ratings', methods=['POST'])
def add_rating():
    return add_rating_service()


@ratings.route('/ratings/<int:book_id>', methods=['GET'])
def get_all_ratings(book_id):
    return get_all_ratings_service(book_id)


@ratings.route('/ratings/<int:book_id>/<string:student_id>', methods=['PUT'])
def update_rating(book_id, student_id):
    return update_rating_service(book_id, student_id)


@ratings.route('/ratings/<int:book_id>/<string:student_id>', methods=['DELETE'])
def delete_rating(book_id, student_id):
    return delete_rating_service(book_id, student_id)
