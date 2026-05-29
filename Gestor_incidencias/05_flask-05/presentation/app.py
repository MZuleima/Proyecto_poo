#CAPA DE PRESENTACIÓN: Servidor Web Flask con Flash Messages y API REST
import logging
from flask import Flask, redirect, url_for, request, render_template, flash, jsonify
from application.servicios import ServiciosIncidencias
from infrastructure.repositorio_sqlite import RepositorioSQLite
from domain.excepciones import ErrorPersistencia

#CONFIGURACIÓN DEL SISTEMA
logging.basicConfig(
    filename='gestor_incidencias.log',
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

app = Flask(__name__)
app.secret_key = "super_clave_secreta_para_flash_messages" 

repo = RepositorioSQLite("incidencias.db")
servicios = ServiciosIncidencias(repo)

@app.before_request
def registrar_peticion():
    logging.info(f"Petición: {request.method} {request.path}")

#API REST MÍNIMA (JSON)

@app.route("/api/incidencias")
def api_listar_incidencias():
    incidencias = servicios.obtener_listado()
    return jsonify([i.to_dict() for i in incidencias])

@app.route("/api/incidencias/<int:id_inc>")
def api_detalle_incidencia(id_inc):
    try:
        inc = servicios.buscar_incidencia(id_inc)
        return jsonify(inc.to_dict())
    except ValueError as e:
        return jsonify({'error': str(e)}), 404

#RUTAS WEB (CON FLASH MESSAGES)

@app.route("/")
def bienvenida():
    return render_template("bienvenida.html")

@app.route("/incidencias")
def listar_incidencias():
    incidencias = servicios.obtener_listado()
    return render_template("incidencias.html", lista_incidencias=incidencias)

@app.route("/tecnicos")
def listar_tecnicos_web():
    return render_template("catalogos.html", titulo_seccion="Catálogo Maestro de Técnicos", elementos=servicios.listar_tecnicos())

@app.route("/salas")
def listar_salas_web():
    return render_template("catalogos.html", titulo_seccion="Catálogo Maestro de Salas", elementos=servicios.listar_salas())

@app.route("/ayuda")
def mostrar_ayuda():
    reglas = [r for r in app.url_map.iter_rules() if r.endpoint != 'static']
    return render_template("ayuda.html", mapa_rutas=reglas)

@app.route("/incidencias/nueva", methods=['GET', 'POST'])
def crear_incidencia_web():
    if request.method == 'GET':
        return render_template("crear_incidencia.html", tecnicos=servicios.listar_tecnicos(), salas=servicios.listar_salas(), valores={})

    id_inc_raw = request.form.get("id_inc")
    try:
        servicios.nueva_incidencia(int(id_inc_raw), int(request.form.get("id_tecnico")), int(request.form.get("id_sala")), request.form.get("descripcion"))
        flash("Incidencia registrada correctamente.", "exito")
        return redirect(url_for("listar_incidencias"))
    except Exception as e:
        return render_template("crear_incidencia.html", tecnicos=servicios.listar_tecnicos(), salas=servicios.listar_salas(), valores=request.form, error=str(e)), 400

@app.route("/incidencias/<int:id_inc>/resolver", methods=['GET', 'POST'])
def resolver_incidencia_web(id_inc):
    inc = servicios.buscar_incidencia(id_inc)
    if request.method == 'GET':
        return render_template("resolver_incidencia.html", inc=inc, valores={})
    
    try:
        servicios.resolver(inc, request.form.get("resolucion"))
        flash(f"Incidencia #{id_inc} solventada con éxito.", "exito")
        return redirect(url_for("listar_incidencias"))
    except ValueError as e:
        return render_template("resolver_incidencia.html", inc=inc, valores=request.form, error=str(e)), 409

#ACCIONES SOLO-POST Y ERRORES

@app.route("/incidencias/<int:id_inc>/documento", methods=['POST'])
def obtener_documento_post(id_inc):
    inc = servicios.buscar_incidencia(id_inc)
    flash("Documento técnico generado.", "info")
    return servicios.generar_documento(inc)

@app.errorhandler(404)
def error_no_encontrado(e):
    return render_template("error.html", codigo=404, titulo="No encontrado", descripcion="Recurso inexistente"), 404

@app.errorhandler(500)
def error_interno(e):
    return render_template("error.html", codigo=500, titulo="Error Interno", descripcion=str(e)), 500

@app.route("/provocar-error")
def provocar_error_test():
    """Endpoint de diagnóstico para probar el manejo de errores 500"""
    return 1 / 0

if __name__ == "__main__":
    app.run(debug=True)