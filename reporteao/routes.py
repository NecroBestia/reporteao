from flask import Blueprint, request
from argon2 import PasswordHasher
from .email import enviar_correo
from . import db, config

bp = Blueprint("routes", __name__)
conf = config.cargar_configuracion('config.toml')
ph = PasswordHasher()

@bp.route('/')
def inicio():
    reportes = db.listar_reportes(1)
    # TODO(NecroBestia): Agregar vista principal
    return reportes

@bp.route('/login')
def login():
    return "TODO"

@bp.route('/register', methods = ['POST', 'GET'])
def registrar():
    if request.method == 'POST':
        nombre = str(request.form['nombre'])
        email = str(request.form['email']) + '@usach.cl'
        clave = ph.hash(str(request.form['clave']))
        db.crear_usuario(nombre, email, clave, -1)
        
        enviar_correo(email, "PLACEHOLDER", conf)
        return "Cuenta creada exitosamente"
    else:
        # TODO(NecroBestia): Agregar formulario de registro
        return "TODO"

@bp.route('/add')
def agregar_reporte():
    return "TODO"

@bp.route('/like')
def apoyar_reporte():
    return "TODO"

@bp.route('/solve')
def resolver_reporte():
    return "TODO"

@bp.route('/delete')
def eliminar_reporte():
    return "TODO"

@bp.route('/verify')
def verificar():
    return "TODO"
