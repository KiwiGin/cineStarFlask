from utils.db import db

class Genero(db.Model):
    __tablename__='Genero'
    
    id=db.Column(db.Integer, primary_key=True)
    Detalle=db.Column(db.String(30))