from utils.db import db

class Distrito(db.Model):
    __tablename__ = 'Distrito'
    
    id = db.Column(db.Integer, primary_key=True)
    Detalle = db.Column(db.String(30))