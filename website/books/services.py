from flask import send_file
from flask import request, jsonify
from ..db import db
from ..library_ma import BookSchema
from ..models import Books

book_schema = BookSchema()
books_schema = BookSchema(many=True)


def add_book_service():
    data = request.get_json()

    errors = book_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    try:
        new_book = Books(
            category_id=data.get('category_id'),
            title=data.get('title'),
            publish_year=data.get('publish_year'),
            author=data.get('author'),
            publisher=data.get('publisher'),
            summary=data.get('summary', None),
            cover=data.get('cover', None),
            file_path=data.get('file_path', None)
        )

        db.session.add(new_book)
        db.session.commit()

        return book_schema.jsonify(new_book), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


def get_book_by_id_service(id):
    book = Books.query.get(id)
    if not book:
        return jsonify({"message": "Book not found"}), 404
    return book_schema.jsonify(book)


def get_all_books_service():
    book_list = Books.query.all()
    if book_list:
        return books_schema.jsonify(book_list)
    else:
        return "Empty book list"


def get_pdf_service(book_id):
    # Fetch book details
    book = Books.query.get(book_id)
    if not book:
        return jsonify({"message": "Book not found"}), 404

    pdf_path = book.file_path
    if not pdf_path:
        return jsonify({"message": "PDF file not found for this book"}), 404

    try:
        # Serve the PDF file
        # as_attachment=False allows in-browser viewing
        return send_file(pdf_path, as_attachment=False)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def update_book_service(id):
    book = Books.query.get(id)
    if not book:
        return jsonify({"message": "Book not found"}), 404

    data = request.get_json()

    errors = book_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    try:
        book.category_id = data.get('category_id', book.category_id)
        book.title = data.get('title', book.title)
        book.publish_year = data.get('publish_year', book.publish_year)
        book.author = data.get('author', book.author)
        book.publisher = data.get('publisher', book.publisher)
        book.summary = data.get('summary', book.summary)
        book.cover = data.get('cover', book.cover)
        book.file_path = data.get('file_path', book.file_path)

        db.session.commit()
        return book_schema.jsonify(book), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


def delete_book_service(id):
    book = Books.query.get(id)
    if not book:
        return jsonify({"message": "Book not found"}), 404

    try:
        db.session.delete(book)
        db.session.commit()
        return jsonify({"message": "Book deleted successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
