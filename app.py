from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from utils.db import db
from models.Cine import Cine, CineTarifa, CinePelicula
from models.Pelicula import Pelicula
from models.Distrito import Distrito
from models.Genero import Genero
from flask_cors import CORS, cross_origin
from sqlalchemy.exc import OperationalError
from time import sleep
from sqlalchemy import text

app=Flask(__name__)
cors = CORS(app)
app.config['SQLALCHEMY_DATABASE_URI']='mysql://u584908256_cinestar:Senati2023%40@srv1101.hstgr.io/u584908256_cinestar'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db.init_app(app)

#funcion para recargar pagina si la conexion al server se va: OperationalError: (2006, 'Server has gone away')
def retry_database_operation(fn):
    def wrapper(*args, **kwargs):
        retries = 3
        while retries > 0:
            try:
                return fn(*args, **kwargs)
            except OperationalError as e:
                if 'Server has gone away' in str(e):
                    print("Reconnecting to the database...")
                    sleep(3)  # 3 segundos de espera antes de intentar DENUEVO
                    db.engine.dispose()  # cerrar conexion
                    retries -= 1
                else:
                    raise e
        raise Exception("Failed to reconnect to the database after multiple attempts")
    return wrapper


@app.route('/')
def index():
    return render_template('index.html')

@retry_database_operation
@app.route('/cines')
def getCines():
    cines = Cine.query.all()
    #for cin in cines:
    #print(cines)
    return render_template('cines.html', cines=cines)

@retry_database_operation
@app.route('/cines/<id>')
def getCine(id):
    print('ID DEL CINE '+id)
    cine = db.session.get(Cine, id)
    distrito = db.session.get(Distrito, id)
    #pelicula = db.session.get(Pelicula, id)
    tarifas = CineTarifa.query.filter_by(idCine=id).all()
    #peliculas = CinePelicula.query.filter_by(idCine=id).all()
    peliculas = db.session.execute(text("CALL sp_getCinePeliculas(:_idCine)"), {'_idCine': id}).fetchall()
    #for cin in cines:
    for tarifa in tarifas:
        print(tarifa.idCine, tarifa.DiasSemana, tarifa.Precio)

    print(peliculas)
    print(distrito)
    return render_template('cine.html', cine=cine, tarifas=tarifas, peliculas=peliculas, distrito=distrito)

@retry_database_operation
@app.route('/peliculas/<estado>')
def getPeliculas(estado):
    print(estado)
    id=0
    if estado=='cartelera':
        id=1
        peliculas = Pelicula.query.filter_by(idEstado=id).all()
    if estado=='estrenos':
        id=2
        peliculas = Pelicula.query.filter_by(idEstado=id).all()
    return render_template('peliculas.html', peliculas=peliculas)

@retry_database_operation
@app.route('/peliculas/<estado>/<idPelicula>')
def getPelicula(estado, idPelicula):
    if estado=='cartelera':
        pelicula = Pelicula.query.filter_by(id=idPelicula, idEstado=1).first()
    if estado=='estrenos':
        pelicula = Pelicula.query.filter_by(id=idPelicula, idEstado=2).first()
    generos_ids = [int(id) for id in pelicula.Generos.split(',')]
    generos = Genero.query.filter(Genero.id.in_(generos_ids)).all()
    return render_template('pelicula.html', pelicula=pelicula, generos=generos)

if __name__=='__main__':
    app.run(debug=True)