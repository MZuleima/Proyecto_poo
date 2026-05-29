#CAPA DE PRESENTACIÓN: Servidor Web Flask con Plantillas Jinja2
import logging
from flask import Flask, redirect, url_for, request, render_template
from application.servicios import ServiciosIncidencias
from infrastructure.repositorio_sqlite import RepositorioSQLite
from domain.excepciones import ErrorPersistencia

#CONFIGURACIÓN DEL SISTEMA DE LOGGING
logging.basicConfig(
    filename='gestor_incidencias.log',
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

app = Flask(__name__)

#Inicialización única e Inyección de Dependencia Relacional
path_db = "incidencias.db"
repo = RepositorioSQLite(path_db)
servicios = ServiciosIncidencias(repo)

#HOOK DE INTERCEPCIÓN DE PETICIONES
@app.before_request
def registrar_peticion():
    logging.info(f"Petición entrante: {request.method} {request.path} - IP: {request.remote_addr}")

#RUTAS DE LECTURA CON PLANTILLAS JINJA2

@app.route("/")
def bienvenida():
    # Renderiza la plantilla de inicio limpia
    return render_template("bienvenida.html")

@app.route("/incidencias")
def listar_incidencias():
    try:
        incidencias = servicios.obtener_listado()
        # Inyectamos la lista de objetos de dominio directamente en la plantilla hija
        return render_template("incidencias.html", lista_incidencias=incidencias)
    except ErrorPersistencia as e:
        return render_template("error.html", codigo=500, titulo="Error de Almacenamiento", descripcion=str(e)), 500

@app.route("/tecnicos")
def listar_tecnicos_web():
    try:
        tecnicos = servicios.listar_tecnicos()
        return render_template("catalogos.html", titulo_seccion="Catálogo Maestro de Técnicos", elementos=tecnicos)
    except ErrorPersistencia as e:
        return render_template("error.html", codigo=500, titulo="Fallo de Persistencia", descripcion=str(e)), 500

@app.route("/salas")
def listar_salas_web():
    try:
        salas = servicios.listar_salas()
        return render_template("catalogos.html", titulo_seccion="Catálogo Maestro de Salas de Control", elementos=salas)
    except ErrorPersistencia as e:
        return render_template("error.html", codigo=500, titulo="Fallo de Persistencia", descripcion=str(e)), 500

#INTROSPECCIÓN Y DIAGNÓSTICO (JINJA2)

@app.route("/ayuda")
def mostrar_ayuda():
    # Filtramos las reglas estáticas y enviamos el iterador de Flask a la plantilla
    reglas_filtradas = [r for r in app.url_map.iter_rules() if r.endpoint != 'static']
    return render_template("ayuda.html", mapa_rutas=reglas_filtradas)

@app.route("/provocar-error")
def provocar_error_test():
    logging.info("Se ha invocado deliberadamente la ruta /provocar-error")
    # Forzamos división por cero para activar el errorhandler(500)
    resultado_bloqueante = 1 / 0 
    return f"Inalcanzable: {resultado_bloqueante}"

#OPERACIONES DE ESCRITURA Y REDIRECCIÓN

@app.route("/incidencias/nueva/<int:id_inc>/<int:id_tecnico>/<int:id_sala>/<descripcion>")
def crear_incidencia_url(id_inc, id_tecnico, id_sala, descripcion):
    try:
        servicios.nueva_incidencia(id_inc, id_tecnico, id_sala, descripcion)
        return redirect(url_for("listar_incidencias"))
    except ValueError as e:
        msg = str(e)
        cod = 409 if "Ya existe" in msg else (404 if "No existe" in msg else 400)
        return render_template("error.html", codigo=cod, titulo="Datos de Registro Inválidos", descripcion=msg), cod
    except ErrorPersistencia as e:
        return render_template("error.html", codigo=500, titulo="Fallo Crítico en Base de Datos", descripcion=str(e)), 500

@app.route("/incidencias/<int:id_inc>/resolver/<resolucion>")
def resolver_incidencia_url(id_inc, resolucion):
    try:
        inc = servicios.buscar_incidencia(id_inc)
        servicios.resolver(inc, resolucion)
        return redirect(url_for("listar_incidencias"))
    except ValueError as e:
        msg = str(e)
        cod = 409 if "ya está resuelta" in msg else 404
        return render_template("error.html", codigo=cod, titulo="Conflicto de Resolución", descripcion=msg), cod
    except ErrorPersistencia as e:
        return render_template("error.html", codigo=500, titulo="Fallo Crítico en Base de Datos", descripcion=str(e)), 500

#Las rutas específicas secundarias de lectura de texto crudo se mantienen igual hasta introducir formularios
@app.route("/incidencias/<int:id_inc>")
def detalle_incidencia(id_inc):
    try:
        inc = servicios.buscar_incidencia(id_inc)
        return f"Incidencia #{inc.id_inc} - {inc.descripcion} | Estado: {inc.estado}"
    except ValueError as e: return render_template("error.html", codigo=404, titulo="No Encontrado", descripcion=str(e)), 404

@app.route("/incidencias/<int:id_inc>/documento")
def obtener_documento(id_inc):
    try:
        inc = servicios.buscar_incidencia(id_inc)
        if inc.estado != "Solventada": return "Error: Incidencia abierta.", 400
        return servicios.generar_documento(inc)
    except ValueError as e: return render_template("error.html", codigo=404, titulo="No Encontrado", descripcion=str(e)), 404

@app.route("/incidencias/<int:id_inc>/relevo/<int:id_tecnico_entrante>")
def derivar_relevo(id_inc, id_tecnico_entrante):
    try:
        inc = servicios.buscar_incidencia(id_inc)
        tecnico_sig = servicios.obtener_tecnico(id_tecnico_entrante)
        return servicios.generar_documento(inc, tecnico_entrante=tecnico_sig)
    except ValueError as e: return render_template("error.html", codigo=404, titulo="Personal Inexistente", descripcion=str(e)), 404

@app.route("/tecnicos/<int:id_tecnico>/avisos")
def ver_avisos_buzon(id_tecnico):
    try:
        avisos = servicios.listar_avisos_tecnico(id_tecnico)
        return f"Buzón Técnico {id_tecnico}: {avisos}"
    except ValueError as e: return render_template("error.html", codigo=404, titulo="No Encontrado", descripcion=str(e)), 404

#MANEJADORES GLOBALES CON PLANTILLA ÚNICA

@app.errorhandler(404)
def error_no_encontrado(e):
    logging.warning(f"Error 404 detectado en: {request.path}")
    return render_template(
        "error.html", 
        codigo=404, 
        titulo="Error 404: Recurso No Encontrado", 
        descripcion="Lo sentimos, la dirección web o el recurso técnico que buscas no existe en el sistema."
    ), 404

@app.errorhandler(500)
def error_interno_servidor(e):
    logging.error(f"Error 500 Crítico no controlado: {e}", exc_info=True)
    return render_template(
        "error.html", 
        codigo=500, 
        titulo="Error 500: Fallo Interno del Servidor", 
        descripcion="Ha ocurrido un error inesperado en el sistema de control de la sala."
    ), 500

if __name__ == "__main__":
    app.run(debug=True)