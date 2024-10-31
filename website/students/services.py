from flask import request, jsonify
from ..db import db
from ..library_ma import StudentSchema
from ..models import Students

student_schema = StudentSchema()
students_schema = StudentSchema(many=True)


def add_student_service():
    data = request.get_json()

    errors = students_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    try:
        new_student = Students(
            fullname=data['fullname'],
            gender=data['gender'],
            username=data['username'],
            email=data['email'],
            password=data['password']
        )
        db.session.add(new_student)
        db.session.commit()

        return student_schema.jsonify(new_student), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


def get_all_students_service():
    all_students = Students.query.all()
    result = students_schema.dump(all_students)
    return jsonify(result)


def get_student_by_id_services(id):
    student = Students.query.get(id)
    if not student:
        return jsonify({"message": "Student not found"}), 404
    return student_schema.jsonify(student)


def update_student_service(id):
    student = Students.query.get(id)
    if not student:
        return jsonify({"message": "Student not found"}), 404

    data = request.get_json()

    errors = students_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    try:
        student.fullname = data['fullname']
        student.gender = data['gender']
        student.username = data['username']
        student.email = data['email']
        student.password = data['password']

        db.session.commit()

        return student_schema.jsonify(student), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


def delete_student_service(id):
    student = Students.query.get(id)
    if not student:
        return jsonify({"message": "Student not found"}), 404

    try:
        db.session.delete(student)
        db.session.commit()

        return jsonify({"message": "Student deleted successfully"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


def change_password_service(id):
    student = Students.query.get(id)
    if not student:
        return jsonify({"message": "Student not found"}), 404

    data = request.get_json()

    errors = students_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    try:
        student.password = data['password']
        confirm_password = data['confirm_password']

        if student.password != confirm_password:
            return jsonify({"error": "Passwords do not match."}), 400

        db.session.commit()

        return student_schema.jsonify(student), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
