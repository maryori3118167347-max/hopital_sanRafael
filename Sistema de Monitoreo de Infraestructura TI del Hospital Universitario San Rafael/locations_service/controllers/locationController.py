from models.locationModel import Location
from extensions import db

def get_all_locations():
    locations = Location.query.order_by(Location.id.asc()).all()
    return [serialize_location(location) for location in locations], 200

def get_location_by_id(location_id):
    location = Location.query.get(location_id)

    if not location:
        return {"message": "Location not found"}, 404
    
    return serialize_location(location), 200

def create_location(data):
    new_location = Location(name=data['name'], floor=data['floor'], building=data['building'], description=data['description'])

    if Location.query.filter_by(name=data['name']).first():
        return {"message": "The name is already in use"}

    db.session.add(new_location)
    db.session.commit()
    return serialize_location(new_location), {"message": "Location successfully created"}, 200

def update_location(location_id, data):
    location = Location.query.get(location_id)

    if not location:
        return{"message": "Location not found"}, 404
    

    existing_location = Location.query.filter(
        Location.name == data['name'],
        Location.id != location_id
    ).first()

    if existing_location:
        return{"message": "The name is already in use for other location"}, 400
    
    location.description = data['description']
    location.building = data['building']
    location.floor = data['floor']
    location.name = data['name']
    db.session.commit()
    return serialize_location(location), {"message": "Location successfully update"}, 200

def delete_location(location_id):
    location = Location.query.get(location_id)

    if not location:
        return {"message":"Location not found"}, 404
    
    db.session.delete(location)
    db.session.commit()
    return{"message": "Location successfully delete"}, 200

def serialize_location(location):
    return{
        "id": location.id,
        "name": location.name,
        "floor": location.floor,
        "building": location.building,
        "description": location.description
    }