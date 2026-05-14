from flask import Flask, request, jsonify
import requests
from functools import wraps
import jwt

app = Flask(__name__)

USER_URL = 'http://localhost:5004/users'
ROLE_URL = 'http://localhost:5005/roles'
LOCATION_URL = 'http://localhost:5001/locations'
DEVICE_URL = 'http://localhost:5002/devices'
AUTH_SR_URL = 'http://localhost:5003/auth'

SECRET_KEY = "super_secret_key"

app.json.sort_keys = False

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        
        if not auth_header:
            return jsonify({"mistake": "Token required"}), 401
        try:
            token = auth_header.split(" ")[1]
            decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            request.user = decoded
        except jwt.ExpiredSignatureError:
            return jsonify({"mistake": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"mistake": "Invalid token"}), 401
        except Exception:
            return jsonify({"mistake": "Token error"}), 401
        
        return f(*args, **kwargs)
    return decorated

#Auth
@app.route("/auth/register", methods=["POST"])
def register():
    response = requests.post(f"{AUTH_SR_URL}/register", json=request.json)
    return jsonify(response.json()), response.status_code

@app.route("/auth/login", methods = ["POST"])
def login():
    response = requests.post(f"{AUTH_SR_URL}/login", json=request.json)
    return jsonify(response.json()), response.status_code

#Devices
@app.route("/devices", methods=["GET","POST"])
@token_required
def devices():
    if request.method == "GET":
        response = requests.get(DEVICE_URL)
        return jsonify(response.json()), response.status_code
    
    if request.method == "POST":
        response = requests.post(DEVICE_URL, json=request.json)
        return jsonify(response.json()), response.status_code
    
@app.route("/devices/<int:id>", methods=["GET","PUT","DELETE"])
@token_required
def device_detail(id):
    
    if request.method == "GET":
        response = requests.get(f"{DEVICE_URL}/{id}")
        
    elif request.method == "PUT":
        response = requests.put(f"{DEVICE_URL}/{id}", json=request.json)

    else:
        response = requests.delete(f"{DEVICE_URL}/{id}")
    return jsonify(response.json()), response.status_code

#Locations
@app.route("/locations", methods=["GET", "POST"])
@token_required
def locations():
    if request.method == "GET":
        response = requests.get(LOCATION_URL)
        return jsonify(response.json()), response.status_code
    
    if request.method == "POST":
        response = requests.post(LOCATION_URL, json=request.json)
        return jsonify(response.json()), response.status_code
    
@app.route("/locations/<int:id>", methods=["GET","PUT","DELETE"])
@token_required
def location_detail(id):
    if request.method == "GET":
        response = requests.get(f"{LOCATION_URL}/{id}")

    elif request.method == "PUT":
        response = requests.put(f"{LOCATION_URL}/{id}", json=request.json)
    
    else:
        response = requests.delete(f"{LOCATION_URL}/{id}")

    return jsonify(response.json()), response.status_code

#Users
@app.route("/users", methods=["GET","POST"])
@token_required
def users():

    if request.method == "GET":
        response = requests.get(USER_URL)
        return jsonify(response.json()), response.status_code

    
    if request.method == "POST":
        response = requests.post(USER_URL, json=request.json)
        return jsonify(response.json()), response.status_code
    
@app.route("/users/<int:id>", methods=["GET","PUT","DELETE"])
@token_required
def user_detail(id):
    
    if request.method == "GET":
        response = requests.get(f"{USER_URL}/{id}")

    elif request.method == "PUT":
        response = requests.put(f"{USER_URL}/{id}", json=request.json)

    else:
        response = requests.delete(f"{USER_URL}/{id}")
    return jsonify(response.json()), response.status_code

#Roles
@app.route("/roles", methods = ["GET", "POST"])
@token_required
def roles():
    if request.method == "GET":
        response = requests.get(ROLE_URL)
        return jsonify(response.json()), response.status_code
    
    if request.method == "POST":
        response = requests.post(ROLE_URL, json=request.json)
        return jsonify(response.json()), response.status_code
    
@app.route("/roles/<int:id>", methods = ["GET", "PUT", "DELETE"])
@token_required
def role_detail(id):
    if request.method == "GET":
        response = requests.get(f"{ROLE_URL}/{id}")
    
    elif request.method == "PUT":
        response = requests.put(f"{ROLE_URL}/{id}", json=request.json)
    
    else:
        response = requests.delete(f"{ROLE_URL}/{id}")
    return jsonify(response.json()), response.status_code

#Main
if __name__ == "__main__":
    app.run(port=5000, debug=True)