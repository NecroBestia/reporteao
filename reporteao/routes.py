from flask import Blueprint, request, session
from argon2 import PasswordHasher
from jinja2 import Environment, PackageLoader, select_autoescape
from .email import enviar_correo
from . import db, config, util

templateEnv = Environment(
    loader=PackageLoader('reporteao', '../templates'),
    autoescape=select_autoescape()
)
bp = Blueprint("routes", __name__)
conf = config.cargar_configuracion('config.toml')
ph = PasswordHasher()

@bp.route('/')
def inicio():
    reportes = db.listar_reportes(1)
    # TODO(NecroBestia): Agregar vista principal
    return reportes

@bp.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        # NOTA: Al hacer el formulario, este campo debería señalar de que el @usach.cl ya está presente.
        email = str(request.form['email']) + '@usach.cl'

        # Se busca el usuario en la base de datos
        usuario = db.conseguir_usuario(email)

        # Se verifica si existe el usuario
        if not usuario:
            return "Usuario no existe"

        # Se verifica si el usuario ya fue verificado o no
        if usuario[3] < 0:
            return "Usuario no está habilitado para iniciar sesión"
            
        # Se verifica si la contraseña es válida
        try:
            ph.verify(usuario[2], str(request.form['clave']))
        except argon2.exceptions.VerifyMismatchError:
            return "Contraseña inválida"
        
        # Se inicia sesión
        session['usuario'] = email
        return "Sesión iniciada"
    # TODO(NecroBestia): Formulario de login
    return "TODO"

@bp.route('/register', methods = ['POST', 'GET'])
def registrar():
    if request.method == 'POST':
        # Se consiguen los datos desde el formulario
        nombre = str(request.form['nombre'])
        email = str(request.form['email']) + '@usach.cl'
        clave = ph.hash(str(request.form['clave']))

        # Se crea el usuario
        db.crear_usuario(nombre, email, clave, -1)

        # Se crea el código de verificación
        codigo = util.uuid()
        db.crear_codigo(email, codigo, 0)

        # Se envía el código de verificación por email al usuario
        plantilla = templateEnv.get_template('email/verificacion.txt')
        correo = plantilla.render(uri=conf['web']['uri'], codigo=codigo)
        enviar_correo(email, 'Verifique su cuenta de ReportEAO', correo)

        return "Se ha enviado un enlace de verificación a su correo institucional. Haga click en él para terminar de crear su cuenta."
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
