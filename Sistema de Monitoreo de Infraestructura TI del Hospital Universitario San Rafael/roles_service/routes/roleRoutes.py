from flask import Blueprint, request, jsonify
from controllers.roleController import *

role_bp = Blueprint('role_bp', __name__)

@role_bp.route('/roles', methods = ['GET'])
def get_roles_route():
    return jsonify(get_all_role())

@role_bp.route('/roles/<int:role_id>', methods = ['GET'])
def get_role_route(role_id):
    result, status = get_role_by_id(role_id)
    return jsonify(result), status

@role_bp.route('/roles', methods = ['POST'])
def create_role_route():
    data = request.get_json()

    if not data:
        return jsonify({"mistake": "Required JSON data"}), 400
    
    return jsonify(create_role(data))

@role_bp.route('/roles/<int:role_id>', methods = ['PUT'])
def update_role_route(role_id):
    data = request.get_json()

    if not data:
        return jsonify({"mistake": "Required JSON data"}), 400
    
    return jsonify(update_role(role_id, data)) 

@role_bp.route('/roles/<int:role_id>', methods = ['DELETE'])
def delete_role_route(role_id):
    return jsonify(delete_role(role_id))

@role_bp.route('/roles/<int:role_id>/permissions', methods=['POST'])
def assign_permissions_route(role_id):
    data = request.get_json()
    if not data:
        return jsonify({"mistake": "Required JSON data"}), 400
    
    return jsonify(assign_permissions(role_id, data))

def remove_permissions_route(role_id):
    data = request.get_json()
    if not data:
        return jsonify({"mistake": "Required JSON data"}), 400
    
    return jsonify(remove_permissions(role_id, data))