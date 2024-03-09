from utils.db import db

class Cine(db.Model):
    __tablename__='Cine'
    
    id=db.Column(db.Integer, primary_key=True)
    RazonSocial=db.Column(db.String(30))
    Salas=db.Column(db.Integer)
    idDistrito=db.Column(db.Integer, db.ForeignKey('Distrito.id'))
    Direccion=db.Column(db.String(100))
    Telefonos=db.Column(db.String(20))

class CineTarifa(db.Model):
    __tablename__='CineTarifa'
    
    #id=db.Column(db.Integer, primary_key=True)
    idCine=db.Column(db.Integer, db.ForeignKey('Cine.id'), primary_key=True)
    DiasSemana=db.Column(db.String(30), primary_key=True)
    Precio=db.Column(db.Float)

class CinePelicula(db.Model):
    __tablename__='CinePelicula'
    
    idCine=db.Column(db.Integer, db.ForeignKey('Cine.id'), primary_key=True)
    idPelicula=db.Column(db.Integer, db.ForeignKey('Pelicula.id'), primary_key=True)
    Sala=db.Column(db.Integer)
    Horarios=db.Column(db.String(30))