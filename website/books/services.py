from flask import send_file, request, jsonify, abort
from ..db import db
from ..library_ma import BookSchema
from ..models import Books
from sqlalchemy.exc import IntegrityError

book_schema = BookSchema()
books_schema = BookSchema(many=True)


def add_book_service():
    data = request.get_json()

    errors = book_schema.validate(data)
    if errors:
        return jsonify({"errors": errors}), 400

    try:
        new_book = Books(
            category_id=data.get('category_id'),
            title=data.get('title'),
            publish_year=data.get('publish_year'),
            author=data.get('author'),
            publisher=data.get('publisher'),
            summary=data.get('summary'),
            cover=data.get('cover'),
            file_path=data.get('file_path')
        )

        db.session.add(new_book)
        db.session.commit()
        return book_schema.jsonify(new_book), 201

    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Book with this title already exists"}), 409
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500


def get_book_by_id_service(id):
    book = Books.query.get(id)
    if not book:
        abort(404, description="Book not found")
    return book_schema.jsonify(book)


def get_all_books_service():
    book_list = Books.query.all()
    return books_schema.jsonify(book_list) if book_list else jsonify({"message": "Empty book list"}), 200


def get_pdf_service(book_id: int):
    book = Books.query.get(book_id)
    if not book:
        abort(404, description="Book not found")

    pdf_path = book.file_path
    if not pdf_path:
        return jsonify({"message": "PDF file not found for this book"}), 404

    try:
        return send_file(pdf_path, as_attachment=False)
    except Exception as e:
        return jsonify({"error": "Failed to send the PDF file", "details": str(e)}), 500


def update_book_service(id: int):
    book = Books.query.get(id)
    if not book:
        abort(404, description="Book not found")

    data = request.get_json()

    errors = book_schema.validate(data)
    if errors:
        return jsonify({"errors": errors}), 400

    try:
        for key, value in data.items():
            if getattr(book, key) != value:
                setattr(book, key, value)

        db.session.add(book)
        db.session.commit()
        return jsonify({"message": "Book updated successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500


def delete_book_service(id: int):
    book = Books.query.get(id)
    if not book:
        abort(404, description="Book not found")

    try:
        db.session.delete(book)
        db.session.commit()
        return jsonify({"message": "Book deleted successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500
