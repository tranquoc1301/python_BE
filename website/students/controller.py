from flask import Blueprint
from .services import *

students = Blueprint('students', __name__)


@students.route('/students', methods=['POST'])
def add_student():
    return add_student_service()


@students.route('/students', methods=['GET'])
def get_all_students():
    return get_all_students_service()


@students.route('/students/<int:id>', methods=['GET'])
def get_student_by_id(id):
    return get_student_by_id_services(id)


@students.route('/students/<int:id>', methods=['PUT'])
def update_student(id):
    return update_student_service(id)


@students.route('/students/<int:id>', methods=['DELETE'])
def delete_student(id):
    return delete_student_service(id)


@students.route('/students/change-password/<int:id>', methods=['PUT'])
def change_password(id):
    return change_password_service(id)
