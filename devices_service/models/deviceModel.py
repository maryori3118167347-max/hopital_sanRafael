from extensions import db

class Device(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    state  = db.Column(db.Boolean, nullable =False)
    serial = db.Column(db.String(100), unique = True)
    description = db.Column(db.String(250), nullable=False)
    last_connection = db.Column(db.DateTime, nullable= False)
    location_id = db.Column(db.Integer, nullable=False)


