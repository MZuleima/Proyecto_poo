#CAPA DE PRESENTACIÓN: Servidor Web Flask con Observabilidad
import logging
from flask import Flask, redirect, url_for, request
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

#Inicialización e Inyección de Dependencia Relacional
path_db = "incidencias.db"
repo = RepositorioSQLite(path_db)
servicios = ServiciosIncidencias(repo)

#INTERCEPCIÓN DE PETICIONES
@app.before_request
def registrar_peticion():
    """Registra en el archivo .log el método y la ruta de cada petición entrante."""
    logging.info(f"Petición entrante: {request.method} {request.path} - IP: {request.remote_addr}")

# RUTAS DE LA API

@app.route("/")
def bienvenida():
    return (
        "<h1>GESTOR DE INCIDENCIAS TÉCNICAS - API WEB</h1>"
        "<p>Bienvenido al sistema de control crítico de Salas de Control.</p>"
        "<h3>Herramientas de Diagnóstico:</h3>"
        "<ul>"
        "<li><a href='/ayuda'>/ayuda</a> &rarr; Diccionario e introspección de rutas del servidor</li>"
        "<li><a href='/provocar-error'>/provocar-error</a> &rarr; Forzar excepción (Prueba de error 500)</li>"
        "</ul>"
        "<h3>Rutas Principales:</h3>"
        "<ul>"
        "<li><a href='/incidencias'>/incidencias</a> &rarr; Listado global de incidencias</li>"
        "<li><a href='/tecnicos'>/tecnicos</a> &rarr; Catálogo de técnicos de guardia</li>"
        "<li><a href='/salas'>/salas</a> &rarr; Catálogo de salas monitorizadas</li>"
        "</ul>"
    )

@app.route("/incidencias")
def listar_incidencias():
    try:
        incidencias = servicios.obtener_listado()
        if not incidencias:
            return "No hay incidencias registradas en el sistema relacional.", 200
        lineas = [
            f"[{inc.id_inc}] Estado: {inc.estado} | Sala: {inc.sala.nombre} "
            f"| Técnico: {inc.tecnico.nombre} | Descripción: {inc.descripcion} "
            f"| Resolución: {inc.resolucion or 'Ninguna'}"
            for inc in incidencias
        ]
        return "<br>".join(lineas)
    except ErrorPersistencia as e:
        return f"Error interno de almacenamiento: {e}", 500

@app.route("/incidencias/<int:id_inc>")
def detalle_incidencia(id_inc):
    try:
        inc = servicios.buscar_incidencia(id_inc)
        return (
            f"<h2>Incidencia Técnica #{inc.id_inc}</h2>"
            f"<strong>Estado:</strong> {inc.estado}<br>"
            f"<strong>Sala:</strong> {inc.sala.nombre} ({inc.sala.ubicacion})<br>"
            f"<strong>Técnico Asignado:</strong> {inc.tecnico.nombre} (Turno {inc.tecnico.turno})<br>"
            f"<strong>Descripción:</strong> {inc.descripcion}<br>"
            f"<strong>Resolución:</strong> {inc.resolucion or 'Pendiente de cierre'}<br>"
        )
    except ValueError as e:
        return f"Elemento no encontrado: {e}", 404
    except ErrorPersistencia as e:
        return f"Error de base de datos: {e}", 500

@app.route("/incidencias/nueva/<int:id_inc>/<int:id_tecnico>/<int:id_sala>/<descripcion>")
def crear_incidencia_url(id_inc, id_tecnico, id_sala, descripcion):
    try:
        servicios.nueva_incidencia(id_inc, id_tecnico, id_sala, descripcion)
        return redirect(url_for("listar_incidencias"))
    except ValueError as e:
        msg = str(e)
        if "Ya existe" in msg: return f"Conflicto: {msg}", 409
        if "No existe" in msg: return f"No encontrado: {msg}", 404
        return f"Datos inválidos: {msg}", 400
    except ErrorPersistencia as e:
        return f"Fallo en SQLite: {e}", 500

@app.route("/incidencias/<int:id_inc>/resolver/<resolucion>")
def resolver_incidencia_url(id_inc, resolucion):
    try:
        inc = servicios.buscar_incidencia(id_inc)
        servicios.resolver(inc, resolucion)
        return redirect(url_for("listar_incidencias"))
    except ValueError as e:
        msg = str(e)
        if "No existe" in msg: return f"Error: {msg}", 404
        if "ya está resuelta" in msg: return f"Conflicto: {msg}", 409
        return f"Petición incorrecta: {msg}", 400
    except ErrorPersistencia as e:
        return f"Error en SQLite: {e}", 500

@app.route("/incidencias/<int:id_inc>/documento")
def obtener_documento(id_inc):
    try:
        inc = servicios.buscar_incidencia(id_inc)
        if inc.estado != "Solventada":
            return "Petición Inválida: No se puede generar acta de un borrador.", 400
        doc = servicios.generar_documento(inc)
        return f"<strong>Documento Emitido:</strong> {doc}"
    except ValueError as e: return f"No encontrado: {e}", 404

@app.route("/incidencias/<int:id_inc>/relevo/<int:id_tecnico_entrante>")
def derivar_relevo(id_inc, id_tecnico_entrante):
    try:
        inc = servicios.buscar_incidencia(id_inc)
        tecnico_sig = servicios.obtener_tecnico(id_tecnico_entrante)
        doc = servicios.generar_documento(inc, tecnico_entrante=tecnico_sig)
        return f"<strong>Operación de Relevo Procesada:</strong> {doc}"
    except ValueError as e: return f"Error en identificadores: {e}", 404

@app.route("/tecnicos")
def listar_tecnicos_web():
    try:
        tecnicos = servicios.listar_tecnicos()
        lineas = [f"ID: {t.id_empleado} | Nombre: {t.nombre} | Turno: {t.turno}" for t in tecnicos]
        return "<h3>Catálogo de Técnicos</h3>" + "<br>".join(lineas)
    except ErrorPersistencia as e: return str(e), 500

@app.route("/tecnicos/<int:id_tecnico>")
def detalle_tecnico_web(id_tecnico):
    try:
        t = servicios.obtener_tecnico(id_tecnico)
        return f"Técnico: {t.nombre} <br> ID: {t.id_empleado} <br> Turno: {t.turno}"
    except ValueError as e: return str(e), 404

@app.route("/tecnicos/<int:id_tecnico>/avisos")
def ver_avisos_buzon(id_tecnico):
    try:
        avisos = servicios.listar_avisos_tecnico(id_tecnico)
        return f"<h3>Buzón (ID Técnico: {id_tecnico})</h3><pre>{avisos}</pre>"
    except ValueError as e: return str(e), 404

@app.route("/salas")
def listar_salas_web():
    try:
        salas = servicios.listar_salas()
        lineas = [f"ID Sala: {s.id_empleado} | Nombre: {s.nombre} | Ubicación: {s.ubicacion}" for s in salas]
        return "<h3>Salas Monitorizadas</h3>" + "<br>".join(lineas)
    except ErrorPersistencia as e: return str(e), 500

@app.route("/salas/<int:id_sala>")
def detalle_sala_web(id_sala):
    try:
        s = servicios.obtener_sala(id_sala)
        return f"Infraestructura: {s.nombre} <br> Sector: {s.ubicacion} <br> ID: {s.id_empleado}"
    except ValueError as e: return str(e), 404

#RUTA DE INTROSPECCIÓN DINÁMICA

@app.route("/ayuda")
def mostrar_ayuda():
    lineas_html = [
        "<html>",
        "<head><title>Mapa de Rutas - Sistema</title></head>",
        "<body style='font-family: monospace; margin: 30px; background-color: #f5f5f5;'>",
        "<h2>Diccionario Auto-Actualizado de la API Web</h2>",
        "<p>A continuación se listan los endpoints activos en el servidor (excluyendo estáticos):</p>",
        "<table border='1' cellpadding='8' style='border-collapse: collapse; background: white;'>",
        "<tr style='background-color: #e0e0e0;'><th>Ruta Registrada</th><th>Métodos HTTP</th></tr>"
    ]
    for regla in app.url_map.iter_rules():
        if regla.endpoint != 'static':
            metodos = ", ".join(regla.methods)
            lineas_html.append(f"<tr><td><strong>{regla.rule}</strong></td><td>{metodos}</td></tr>")
    lineas_html.extend([
        "</table>",
        "<p><br><a href='/'>&larr; Volver al inicio</a></p>",
        "</body>",
        "</html>"
    ])
    return "".join(lineas_html), 200

@app.route("/provocar-error")
def provocar_error_test():
    logging.info("Se ha invocado deliberadamente la ruta /provocar-error")
    resultado_bloqueante = 1 / 0 
    return f"Esto nunca se renderizará: {resultado_bloqueante}"

#MANEJADORES GLOBALES DE ERROR (Cierre)

@app.errorhandler(404)
def error_no_encontrado(e):
    logging.warning(f"Error 404 detectado en: {request.path}")
    html_error = (
        "<html>"
        "<head><title>404 Not Found - Gestor Incidencias</title></head>"
        "<body style='font-family: Arial, sans-serif; margin: 40px; background-color: #fcf8e3; color: #8a6d3b;'>"
        "<h1>Error 404: Recurso No Encontrado</h1>"
        "<p>Lo sentimos, la dirección web o el recurso técnico que buscas no existe en el sistema.</p>"
        "<hr>"
        "<p><a href='/' style='color: #a94442; font-weight: bold;'>Volver al Índice Principal</a> | "
        "<a href='/ayuda' style='color: #a94442; font-weight: bold;'>Ver Mapa de Rutas (/ayuda)</a></p>"
        "</body>"
        "</html>"
    )
    return html_error, 404

@app.errorhandler(500)
def error_interno_servidor(e):
    logging.error(f"Error 500 Crítico no controlado: {e}", exc_info=True)
    html_error = (
        "<html>"
        "<head><title>500 Internal Server Error - Gestor Incidencias</title></head>"
        "<body style='font-family: Arial, sans-serif; margin: 40px; background-color: #f2dede; color: #a94442;'>"
        "<h1>Error 500: Fallo Interno del Servidor</h1>"
        "<p>Ha ocurrido un error inesperado en el sistema de control. El fallo ha sido registrado en el archivo de logs para su revisión técnica.</p>"
        "<hr>"
        "<p><a href='/' style='color: #31708f; font-weight: bold;'>Regresar a Zona Segura</a></p>"
        "</body>"
        "</html>"
    )
    return html_error, 500

if __name__ == "__main__":
    app.run(debug=True)