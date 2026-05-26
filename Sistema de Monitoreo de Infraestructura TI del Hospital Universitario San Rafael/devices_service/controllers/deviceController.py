from models.deviceModel import Device
from extensions import db
import requests

#LOCATION_SERVICE_URL = "http://localhost:5001/locations"
LOCATION_SERVICE_URL = "http://locations_service:5001/locations"


def get_location_data(location_id):
    try:
        response = requests.get(f"{LOCATION_SERVICE_URL}/{location_id}")
        if response.status_code == 200:
            return response.json()
        else:
            return{"mistake": "Location information could not be obtained"},404
    except requests.exceptions.RequestException as e:
        return {"mistake": f"Error connecting to the location service: {str(e)}"}, 500
    
def validate_location(location_id):
    try:
        response = requests.get(f"{LOCATION_SERVICE_URL}/{location_id}")

        if response.status_code == 200: 
            return True
        
        if response.status_code == 404:
            return False
        
        return False
    
    except requests.exceptions.RequestException:
        return None
    
def get_all_devices():
    devices = Device.query.order_by(Device.id.asc()).all()
    result = []

    for device in devices:
        location = get_location_data(device.location_id)

        result.append({
            "id": device.id,
            "name": device.name,
            "state": device.state,
            "serial": device.serial,
            "description": device.description,
            "last_connection": device.last_connection,
            "location": location
        })

    return result

def get_device_by_id(device_id):
    device = Device.query.get(device_id)

    if not device:
        return{"mistake": "Device not found"}, 404
    
    location = get_location_data(device.location_id)

    return{
        "id": device.id,
        "name": device.name,
        "state": device.state,
        "serial": device.serial,
        "description": device.description,
        "last_connection": device.last_connection,
        "location":location
    }

def create_device(data):
    location_id = data.get("location_id")

    validation = validate_location(location_id)

    if validation is None:
        return{"mistake": "Location service unavailable"}, 500
    
    if not validation:
        return {"mistake": "The device cannot be created because the client does not exist."}, 400
    
    new_device = Device(
        name=data['name'],
        state=data['state'],
        serial=data['serial'],
        description=data['description'],
        last_connection=data['last_connection'],
        location_id=location_id
    )

    db.session.add(new_device)
    db.session.commit()
    return serialize_device(new_device), {"message": "Device successfully created"}, 200

def update_device(device_id, data):
    device = Device.query.get(device_id)

    if not device:
        return{"message": "Device not found"}, 404
    
    location_id = data.get("location_id")

    if location_id:
        validation = validate_location(location_id) 
        
        if validation is None:
            return{"mistake": "Location service unavailable"}, 500
    
        if not validation:
            return{"mistake": "The location does not exist"}, 400
    
        device.location_id = location_id
    
    device.name = data['name']
    device.state = data['state']
    device.serial = data['serial']
    device.description = data['description']
    device.last_connection = data['last_connection']
    db.session.commit()
    return serialize_device(device), {"message": "Device successfully update"}, 200

def delete_device(device_id):
    device = Device.query.get(device_id)

    if not device:
        return {"message": "Device not found"}, 404
    
    db.session.delete(device)
    db.session.commit()
    return{"message": "Device successfully delete"}, 200

def serialize_device(device):
    return{
        "id": device.id,
        "name": device.name,
        "state": device.state,
        "serial": device.serial,
        "description": device.description,
        "last_connection": device.last_connection,
        "location_id": device.location_id
    }
