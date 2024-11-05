from flask import Blueprint
from .services import *

comments = Blueprint('comments', __name__)


@comments.route('/comments', methods=['GET'])
def get_all_comments():
    return get_all_comments_service()


@comments.route('/comments/<int:id>', methods=['GET'])
def get_comment(id):
    return get_comment_service(id)


@comments.route('/comments', methods=['POST'])
def add_comment():
    return add_comment_service()


@comments.route('/comments/<int:id>', methods=['PUT'])
def update_comment(id):
    return update_comment_service(id)

@comments.route('/comments/<int:id>', methods=['DELETE'])
def delete_comment(id):
    return delete_comment_service(id)


