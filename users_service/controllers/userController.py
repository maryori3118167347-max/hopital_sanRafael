from models.usersModel import User_SR
from extensions import db
import requests

ROL_SERVICE_URL = "http://localhost:5005/roles"

def get_roles_data(rol_id):
    try:
        response = requests.get(f"{ROL_SERVICE_URL}/{rol_id}")
        if response.status_code ==  200:
            return response.json()
        else:
            return {"mistake": "The role information could not be obtained"}, 404
    except requests.exceptions.RequestException as e:
        return {"mistake": f"Error connecting to the role service: {str(e)}"}, 500    

def validate_role(rol_id):
    try:
        response = requests.get(f"{ROL_SERVICE_URL}/{rol_id}")

        if response.status_code == 200:
            return True
        
        if response.status_code == 404:
            return False
        
        return False
    except requests.exceptions.RequestException:
        return None

def get_all_users():
    users = User_SR.query.order_by(User_SR.id.asc()).all()
    return [serialize_user(user) for user in users], 200

def get_user_by_id(user_id): 
    user = User_SR.query.get(user_id)

    if not user:
        return{"message": "User not found"}, 404
    return serialize_user(user), 200

def create_user(data):
    rol_id = data.get("rol_id")
    validation = validate_role(rol_id)

    if validation is None:
        return {"mistake": "Rol service unavailable"}, 500
    
    if not validation:
        return {"error": "The user cannot be created because the role does not exist."}
    
    new_user = User_SR(
        name=data['name'],
        email = data['email'],
        password = data['password'],
        state = data['state'],
        rol_id = rol_id
    )
    db.session.add(new_user)
    db.session.commit()
    return serialize_user(new_user), {"message": "User successfully created"}, 200


def update_user(user_id, data):
    user = User_SR.query.get(user_id)

    if not user:
        return {"message": "User not found"}, 404
    
    rol_id = data.get("rol_id")

    if rol_id:
        validation = validate_role(rol_id)

        if validation is None:
            return {"mistake": "Rol service unavilable"}, 500
        
        if not validation:
            return {"error": "The role does not exist"}, 400
        
        user.rol_id = rol_id
    user.name = data['name']
    user.email = data['email']
    user.password = data['password']
    user.state = data['state']
    db.session.commit()
    return serialize_user(user), {"message": "User successfully updated"}, 200

def delete_user(user_id):
    user = User_SR.query.get(user_id)

    if not user:
        return {"message": "User not found"}, 404
    
    db.session.delete(user)
    db.session.commit()
    return {"message": "User successfully deleted"}, 200

def serialize_user(user):
    return{
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "password": user.password,
        "state": user.state,
        "rol_id": user.rol_id
    }