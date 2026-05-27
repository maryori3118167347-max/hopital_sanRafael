from extensions import db

class User_SR(db.Model):
    __tablename__ = "users_sr"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    email = db.Column(db.String(100), nullable = False, unique = True)
    password = db.Column(db.String(200), nullable = False)
    state = db.Column(db.Boolean, nullable = False)
    rol_id = db.Column(db.Integer, nullable = False)
