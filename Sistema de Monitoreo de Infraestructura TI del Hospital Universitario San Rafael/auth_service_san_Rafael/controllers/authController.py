from models.userModel import User
from extensions import db
from utils.jwt_handler import generate_token
from werkzeug.security import generate_password_hash, check_password_hash

def login(data):
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()

    if not user:
        return {"mistake": "User not found"}, 404

    if not check_password_hash(user.password, password):
        return {"mistake": "incorrect credentials"}, 401

    token = generate_token(user, rol_id=user.rol_id)

    return {
        "token": token,
        "user_id": user.id,
        "email":   user.email,
        "rol_id":  user.rol_id    
    }, 200

def register(data):
    email = data.get("email")
    password = data.get("password")
    rol_id   = data.get("rol_id")

    if User.query.filter_by(email=email).first():
        return {"mistake": "The user already exists"}, 400

    hashed_password = generate_password_hash(password)

    new_user = User(
        email=email,
        password=hashed_password,
        rol_id= rol_id
    )

    db.session.add(new_user)
    db.session.commit()

    return {"message": "User successfully created", "rol_id": rol_id}, 201