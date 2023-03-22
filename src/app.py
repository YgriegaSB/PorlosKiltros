from select import select
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, login_user, logout_user, login_required
from werkzeug.security import  generate_password_hash
# conexion bd
from config import config

# Entities
from models.entities.User import User

app = Flask(__name__)

csrf = CSRFProtect()
db = MySQL(app)

# Redirigir raiz a home
@app.route('/')
def index():
    return redirect(url_for('home'))

################################################# Vista home ###########################################################
@app.route('/home')
def home():
    return render_template('auth/home.html')

################################################# Vista galeria ###########################################################
@app.route('/galeria')
def galeria():
    return render_template('auth/galeria.html')

################################################# Vista reserva ###########################################################
@app.route('/reserva')
def reserva():
    return render_template('auth/reserva.html')

@app.route('/reservar', methods=['GET', 'POST'])
def reservar():
    if request.method == 'POST':
        servicio = request.form['servicio']
        fecha = request.form['fecha']
        hora = request.form['hora']
        tutor = request.form['tutor']
        apellido = request.form['apellido']
        email = request.form['email']
        telefono = request.form['telefono']
        especie = request.form['especie']
        nombre = request.form['nombre']
        cursor = db.connection.cursor()
        cursor.execute('INSERT INTO reservas (servicio, fecha, hora, nombrecl, apellidoP, email, telefono, especie, nombre) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)', (servicio, fecha, hora, tutor, apellido, email, telefono, especie, nombre))
        # commit sql sentence
        db.connection.commit()
        # message
        flash('Reserva realizada') 
        return redirect(url_for('reserva'))

def status_401(error):
    return redirect(url_for('login'))

def status_404(error):
    return "<h1> Lo sentimos, esta página no existe :( </h1>", 404

if __name__ == '__main__':
    app.config.from_object(config['development'])
    csrf.init_app(app)
    app.register_error_handler(401, status_401)
    app.register_error_handler(404, status_404)
    app.run()