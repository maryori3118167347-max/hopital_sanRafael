from extensions import db

class Roles(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False, unique = True)
    description = db.Column(db.String(250), nullable = False)
    #Este sirve