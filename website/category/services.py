from flask import request, jsonify, abort
from ..db import db
from ..library_ma import CategorySchema
from ..models import Category
from sqlalchemy.exc import IntegrityError

category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)


def add_category_service():
    data = request.get_json()

    errors = category_schema.validate(data)
    if errors:
        return jsonify({"errors": errors}), 400

    try:
        new_category = Category(
            category=data.get('category'),
            image=data.get('image')
        )
        db.session.add(new_category)
        db.session.commit()
        return category_schema.jsonify(new_category), 201

    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Category already exists"}), 409
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500


def get_all_categories_service():
    categories = Category.query.all()
    return jsonify(categories_schema.dump(categories)), 200


def get_category_by_id_service(id: int):
    category = Category.query.get(id)
    if not category:
        abort(404, description="Category not found")
    return category_schema.jsonify(category), 200


def update_category_service(id: int):
    category = Category.query.get(id)
    if not category:
        abort(404, description="Category not found")

    data = request.get_json()

    errors = category_schema.validate(data)
    if errors:
        return jsonify({"errors": errors}), 400

    try:

        for key, value in data.items():
            if getattr(category, key) != value:
                setattr(category, key, value)

        db.session.commit()

        return category_schema.jsonify(category), 200

    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Category update failed due to a database integrity issue"}), 409
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500


def delete_category_service(id: int):
    category = Category.query.get(id)
    if not category:
        abort(404, description="Category not found")

    try:
        db.session.delete(category)
        db.session.commit()
        return jsonify({"message": "Category deleted successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500
