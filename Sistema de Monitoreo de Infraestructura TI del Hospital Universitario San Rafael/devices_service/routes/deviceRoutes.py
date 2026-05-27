from flask import Blueprint, request, jsonify
from controllers.deviceController import *

device_bp = Blueprint('device_bp', __name__)
@device_bp.route('/devices', methods=['GET'])
def get_devices_route():
    return jsonify(get_all_devices())

@device_bp.route('/devices/<int:device_id>', methods=['GET'])
def get_device_route(device_id):
    return jsonify(get_device_by_id(device_id))

@device_bp.route('/devices', methods=['POST'])
def create_device_route():
    data = request.get_json()

    if not data:
        return jsonify({"mistake": "Required JSON data"}), 400
    
    return jsonify(create_device(data))

@device_bp.route('/devices/<int:device_id>', methods=['PUT'])
def update_device_route(device_id):
    data = request.get_json()

    if not data:
        return jsonify({"mistake", "Required JSON data"}), 400
    
    return jsonify(update_device(device_id, data))

@device_bp.route('/devices/<int:device_id>', methods=['DELETE'])
def delete_device_route(device_id):
    return jsonify(delete_device(device_id))