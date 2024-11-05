from flask import Blueprint
from .services import *

category = Blueprint('category', __name__)


@category.route('/categories', methods=['GET'])
def get_all_categories():
    return get_all_categories_service()


@category.route('/categories/<int:id>', methods=['GET'])
def get_category_by_id(id):
    return get_category_by_id_service(id)


@category.route('/categories', methods=['POST'])
def add_category():
    return add_category_service()


@category.route('/categories/<int:id>', methods=['PUT'])
def update_category(id):
    return update_category_service(id)


@category.route('/categories/<int:id>', methods=['DELETE'])
def delete_category(id):
    return delete_category_service(id)
