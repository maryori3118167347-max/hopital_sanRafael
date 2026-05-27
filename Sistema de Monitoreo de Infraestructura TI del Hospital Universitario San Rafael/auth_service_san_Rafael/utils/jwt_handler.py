import jwt
import datetime
import requests
from config import SECRET_KEY

# SECRET_KEY = "supersecret"

ROLES_SERVICE_URL = "http://roles_service:5005"

def get_permissions_for_role(rol_id):
    try:
        response = requests.get(
            f"{ROLES_SERVICE_URL}/roles/{rol_id}",
            timeout=3
        )
        if response.status_code == 200:
            return response.json().get('permissions', [])
    except requests.exceptions.RequestException as e:
        print(f"[jwt_handler] The roles_service query could not be accessed: {e}")
    return []

def generate_token(user, rol_id=None):
    permissions = get_permissions_for_role(rol_id) if rol_id else []
    payload = {
        "user_id": user.id,
        "email": user.email,
        "rol_id": rol_id,
        "permissions": permissions,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }

    # token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    # return token
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def decode_token(token):
    return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])