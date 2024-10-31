from flask import Blueprint
from .services import *

books = Blueprint("books", __name__)


@books.route('/books', methods=['POST'])
def create_book():
    return add_book_service()


@books.route('/books/<int:id>', methods=['GET'])
def get_book_by_id(id):
    return get_book_by_id_service(id)


@books.route('/books', methods=['GET'])
def get_all_books():
    return get_all_books_service()


@books.route('/books/<int:id>/read', methods=['GET'])
def read_book(id):
    return get_pdf_service(id)


@books.route('/books/<int:id>', methods=['PUT'])
def update_book(id):
    return update_book_service(id)


@books.route('/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    return delete_book_service(id)
