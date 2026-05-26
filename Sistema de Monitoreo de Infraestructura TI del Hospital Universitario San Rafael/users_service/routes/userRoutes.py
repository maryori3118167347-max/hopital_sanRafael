from flask import Blueprint, request, jsonify
from controllers.userController import *

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/users', methods=['GET'])
def get_users_route():
    return jsonify(get_all_users())

@user_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user_route(user_id):
    return jsonify(get_user_by_id(user_id))

@user_bp.route('/users', methods=['POST'])
def create_user_route():
    data = request.get_json()

    if not data:
        return jsonify({"mistake": "Required JSON data"}), 400
    return jsonify(create_user(data))


@user_bp.route('/users/<int:user_id>', methods = ['PUT'])
def update_user_route(user_id):
    data = request.get_json()

    if not data:
        return jsonify({"mistake": "Required JSON data"}), 400
    return jsonify(update_user(user_id, data))

@user_bp.route('/users/<int:user_id>', methods = ['DELETE'])
def delete_user_route(user_id):
    return jsonify(delete_user(user_id))