from models.roleModel import Roles, Permission
from extensions import db

def get_all_role():
    roles = Roles.query.order_by(Roles.id.asc()).all()
    return [serialize_role(role) for role in roles], 200

def get_role_by_id(role_id):
    roles = Roles.query.get(role_id)

    if not roles:
        return {"message": "Role not found"}, 404
    
    return serialize_role(roles), 200

def create_role(data):
    new_role = Roles(name = data['name'], description = data['description'])

    if Roles.query.filter_by(name=data['name']).first():
        return {"mistake": "The name of this role is already in use"}, 400

    db.session.add(new_role)
    db.session.commit()
    return serialize_role(new_role), {"message": "Role successfully created"}, 200

def update_role(role_id, data):
    roles = Roles.query.get(role_id)

    if not roles:
        return {"message": "Role not found"}, 404

    existing_role = Roles.query.filter(
        Roles.name == data['name'],
        Roles.id != role_id
    ).first()

    if existing_role:
        return {"mistake": "The name of this role is already in use by other rol"}, 400

    roles.description = data['description']
    roles.name = data['name']
    db.session.commit()
    return serialize_role(roles), {"message": "Role successfully update"} 

def delete_role(role_id):
    roles = Roles.query.get(role_id)

    if not roles:
        return {"message": "Role not found"}, 404
    
    db.session.delete(roles)
    db.session.commit()
    return {"message": "Role successfullt deleted"}, 200

def assign_permissions(role_id, data):
    role = Roles.query.get(role_id)
    if not role:
        return {"message": "Role not found"}, 404
    for perm_name in data.get('permissions', []):
        perm = Permission.query.filter_by(name=perm_name).first()
        if not perm:
            perm = Permission(name=perm_name, description='')
            db.session.add(perm)
            db.session.flush()
        if perm not in role.permissions:
            role.permissions.append(perm)
    db.session.commit()
    return serialize_role(role), 200

def remove_permissions(role_id, data):
    role = Roles.query.get(role_id)
    if not role:
        return {"message": "Role not found"}, 404
    for perm_name in data.get('permissions', []):
        perm = Permission.query.filter_by(name=perm_name).first()
        if perm and perm in role.permissions:
            role.permissions.remove(perm)
    db.session.commit()
    return serialize_role(role), 200

def serialize_role(roles):
    return{
        "id": roles.id,
        "name": roles.name,
        "description": roles.description,
        "permissions": [p.name for p in roles.permissions]
    }