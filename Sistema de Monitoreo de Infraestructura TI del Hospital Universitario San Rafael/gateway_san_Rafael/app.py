from flask import Flask, request, jsonify
import requests
from functools import wraps
import jwt

app = Flask(__name__)

"""
USER_URL = 'http://localhost:5004/users'
ROLE_URL = 'http://localhost:5005/roles'
LOCATION_URL = 'http://localhost:5001/locations'
DEVICE_URL = 'http://localhost:5002/devices'
AUTH_SR_URL = 'http://localhost:5003/auth'
"""
USER_URL = 'http://users_service:5004/users'
ROLE_URL = 'http://roles_service:5005/roles'
LOCATION_URL = 'http://locations_service:5001/locations'
DEVICE_URL = 'http://devices_service:5002/devices'
AUTH_SR_URL = 'http://auth_service:5003/auth'



SECRET_KEY = "super_secret_key"

app.json.sort_keys = False

def decode_request_token():
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return None, (jsonify({"mistake": "Token required"}), 401)
    try:
        token = auth_header.split(" ")[1]
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload, None
    except jwt.ExpiredSignatureError:
        return None, (jsonify({"mistake": "Token expired"}), 401)
    except jwt.InvalidTokenError:
        return None, (jsonify({"mistake": "Invalid token"}), 401)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        payload, error = decode_request_token()
        if error:
            return error
        request.user = payload
        return f(*args, **kwargs)
    return decorated

def require_permission(permission):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            payload, error = decode_request_token()
            if error:
                return error
            if permission not in payload.get("permissions", []):
                return jsonify({
                    "mistake": f"Access denied. Required permission: {permission}"
                }), 403
            request.user = payload
            return f(*args, **kwargs)
        return wrapper
    return decorator

# ── Auth (No token) ──────────────────────────────────────────
@app.route("/auth/register", methods=["POST"])
def register():
    response = requests.post(f"{AUTH_SR_URL}/register", json=request.json)
    return jsonify(response.json()), response.status_code

@app.route("/auth/login", methods = ["POST"])
def login():
    response = requests.post(f"{AUTH_SR_URL}/login", json=request.json)
    return jsonify(response.json()), response.status_code

# ── Devices ───────────────────────────────────────────────────
# devices:read  → Admin, Doctor, ICT Manager
# devices:write → Admin, ICT Manager
# devices:delete→ Admin, ICT Manager

@app.route("/devices", methods=["GET"])
@require_permission("devices:read")
def get_devices():
    response = requests.get(DEVICE_URL)
    return jsonify(response.json()), response.status_code

@app.route("/devices", methods=["POST"])
@require_permission("devices:write")
def create_device():
    response = requests.post(DEVICE_URL, json=request.json)
    return jsonify(response.json()), response.status_code

@app.route("/devices/<int:id>", methods=["GET"])
@require_permission("devices:read")
def get_device(id):
    response = requests.get(f"{DEVICE_URL}/{id}")
    return jsonify(response.json()), response.status_code

@app.route("/devices/<int:id>", methods=["PUT"])
@require_permission("devices:write")
def update_device(id):
    response = requests.put(f"{DEVICE_URL}/{id}", json=request.json)
    return jsonify(response.json()), response.status_code

@app.route("/devices/<int:id>", methods=["DELETE"])
@require_permission("devices:delete")
def delete_device(id):
    response = requests.delete(f"{DEVICE_URL}/{id}")
    return jsonify(response.json()), response.status_code
#───────────────────────────────────────────────────────────────────────
# ── Locations ─────────────────────────────────────────────────
# locations:read  → Admin, Doctor, ICT Manager
# locations:write → Admin, ICT Manager
# locations:delete→ Admin, ICT Manager
@app.route("/locations", methods=["GET"])
@require_permission("locations:read")
def get_locations():
    response = requests.get(LOCATION_URL)
    return jsonify(response.json()), response.status_code

@app.route("/locations", methods=["POST"])
@require_permission("locations:write")
def create_location():
    response = requests.post(LOCATION_URL, json=request.json)
    return jsonify(response.json()), response.status_code

@app.route("/locations/<int:id>", methods=["GET"])
@require_permission("locations:read")
def get_location(id):
    response = requests.get(f"{LOCATION_URL}/{id}")
    return jsonify(response.json()), response.status_code

@app.route("/locations/<int:id>", methods=["PUT"])
@require_permission("locations:write")
def update_location(id):
    response = requests.put(f"{LOCATION_URL}/{id}", json=request.json)
    return jsonify(response.json()), response.status_code

@app.route("/locations/<int:id>", methods=["DELETE"])
@require_permission("locations:delete")
def delete_location(id):
    response = requests.delete(f"{LOCATION_URL}/{id}")
    return jsonify(response.json()), response.status_code
#───────────────────────────────────────────────────────────────────────
# ── Users ─────────────────────────────────────────────────────
# users:read  → Admin, Doctor
# users:write → Admin
# users:delete→ Admin
@app.route("/users", methods=["GET"])
@require_permission("users:read")
def get_users():
    response = requests.get(USER_URL)
    return jsonify(response.json()), response.status_code

@app.route("/users", methods=["POST"])
@require_permission("users:write")
def create_user():
    response = requests.post(USER_URL, json=request.json)
    return jsonify(response.json()), response.status_code

@app.route("/users/<int:id>", methods=["GET"])
@require_permission("users:read")
def get_user(id):
    response = requests.get(f"{USER_URL}/{id}")
    return jsonify(response.json()), response.status_code

@app.route("/users/<int:id>", methods=["PUT"])
@require_permission("users:write")
def update_user(id):
    response = requests.put(f"{USER_URL}/{id}", json=request.json)
    return jsonify(response.json()), response.status_code

@app.route("/users/<int:id>", methods=["DELETE"])
@require_permission("users:delete")
def delete_user(id):
    response = requests.delete(f"{USER_URL}/{id}")
    return jsonify(response.json()), response.status_code
#───────────────────────────────────────────────────────────────────────
# ── Roles ─────────────────────────────────────────────────────
# Everything: Admin only
@app.route("/roles", methods=["GET"])
@require_permission("roles:read")
def get_roles():
    response = requests.get(ROLE_URL)
    return jsonify(response.json()), response.status_code

@app.route("/roles", methods=["POST"])
@require_permission("roles:write")
def create_role():
    response = requests.post(ROLE_URL, json=request.json)
    return jsonify(response.json()), response.status_code

@app.route("/roles/<int:id>", methods=["GET"])
@require_permission("roles:read")
def get_role(id):
    response = requests.get(f"{ROLE_URL}/{id}")
    return jsonify(response.json()), response.status_code

@app.route("/roles/<int:id>", methods=["PUT"])
@require_permission("roles:write")
def update_role(id):
    response = requests.put(f"{ROLE_URL}/{id}", json=request.json)
    return jsonify(response.json()), response.status_code

@app.route("/roles/<int:id>", methods=["DELETE"])
@require_permission("roles:write")
def delete_role(id):
    response = requests.delete(f"{ROLE_URL}/{id}")
    return jsonify(response.json()), response.status_code

@app.route("/roles/<int:id>/permissions", methods=["POST"])
@require_permission("roles:write")
def assign_role_permissions(id):
    response = requests.post(f"{ROLE_URL}/{id}/permissions", json=request.json)
    return jsonify(response.json()), response.status_code

@app.route("/roles/<int:id>/permissions", methods=["DELETE"])
@require_permission("roles:write")
def remove_role_permissions(id):
    response = requests.delete(f"{ROLE_URL}/{id}/permissions", json=request.json)
    return jsonify(response.json()), response.status_code
#Main
if __name__ == "__main__":
    #app.run(port=5000, debug=True)
    app.run(host='0.0.0.0', port=5000)