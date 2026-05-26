from flask import Blueprint, request, jsonify
from controllers.locationController import *

location_bp = Blueprint('location_bp', __name__)

@location_bp.route('/locations', methods=['GET'])
def get_locations_route():
    return jsonify(get_all_locations())

@location_bp.route('/locations/<int:location_id>', methods=['GET'])
def get_location_route(location_id):
    result, status = get_location_by_id(location_id)
    return jsonify(result), status

@location_bp.route('/locations', methods=['POST'])
def create_location_route():
    data = request.get_json()

    if not data:
        return jsonify({"message": "Required JSON dates"}), 400
    
    return jsonify(create_location(data))

@location_bp.route('/locations/<int:location_id>', methods=['PUT'])
def update_location_route(location_id):
    data = request.get_json()

    if not data:
        return jsonify({"mistake": "Required JSON dates"}), 400
    
    return jsonify(update_location(location_id, data))

@location_bp.route('/locations/<int:location_id>', methods=['DELETE'])
def delete_location_route(location_id):
    return jsonify(delete_location(location_id))