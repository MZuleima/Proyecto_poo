#CAPA DE PRESENTACIÓN: Servidor Web Flask
from flask import Flask, redirect, url_for
from application.servicios import ServiciosIncidencias
from infrastructure.repositorio_sqlite import RepositorioSQLite
from domain.excepciones import ErrorPersistencia

app = Flask(__name__)

# Inicialización única de componentes e Inyección de Dependencia Relacional
path_db = "incidencias.db"
repo = RepositorioSQLite(path_db)
servicios = ServiciosIncidencias(repo)

#RUTA RAÍZ

@app.route("/")
def bienvenida():
    """Ruta de bienvenida con el mapa completo de la API disponible."""
    return (
        "<h1>GESTOR DE INCIDENCIAS TÉCNICAS - API WEB</h1>"
        "<p>Bienvenido al sistema de control crítico de Salas de Control.</p>"
        "<h3>Rutas Disponibles:</h3>"
        "<ul>"
        "<li><a href='/incidencias'>/incidencias</a> &rarr; Listado global de incidencias</li>"
        "<li><a href='/tecnicos'>/tecnicos</a> &rarr; Catálogo de técnicos de guardia</li>"
        "<li><a href='/salas'>/salas</a> &rarr; Catálogo de salas monitorizadas</li>"
        "</ul>"
        "<p><strong>Nota:</strong> Las rutas de inserción, resolución y relevos se ejecutan "
        "pasando los parámetros directamente en la URL según la guía técnica.</p>"
    )

#RUTAS DE INCIDENCIAS

@app.route("/incidencias")
def listar_incidencias():
    """Lista todas las incidencias formateadas como texto plano transitable."""
    try:
        incidencias = servicios.obtener_listado()
        if not incidencias:
            return "No hay incidencias registradas en el sistema relacional.", 200
        
        lineas = []
        for inc in incidencias:
            lineas.append(
                f"[{inc.id_inc}] Estado: {inc.estado} | Sala: {inc.sala.nombre} "
                f"| Técnico: {inc.tecnico.nombre} | Descripción: {inc.descripcion} "
                f"| Resolución: {inc.resolucion or 'Ninguna'}"
            )
        return "<br>".join(lineas)
    except ErrorPersistencia as e:
        return f"Error interno de almacenamiento: {e}", 500

@app.route("/incidencias/<int:id_inc>")
def detalle_incidencia(id_inc):
    """Muestra el detalle específico de una incidencia. Retorna 404 si no existe."""
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
    """
    Registra una incidencia desde la URL.
    Aplica el patrón 'Actúa -> Redirige' para evitar reenvíos de datos.
    """
    try:
        servicios.nueva_incidencia(id_inc, id_tecnico, id_sala, descripcion)
        #redirigimos al listado global
        return redirect(url_for("listar_incidencias"))
    except ValueError as e:
        msg = str(e)
        if "Ya existe" in msg:
            return f"Conflicto de negocio: {msg}", 409
        if "No existe" in msg:
            return f"Recurso no encontrado: {msg}", 404
        return f"Datos inválidos provistos: {msg}", 400
    except ErrorPersistencia as e:
        return f"Fallo de persistencia en SQLite: {e}", 500

@app.route("/incidencias/<int:id_inc>/resolver/<resolucion>")
def resolver_incidencia_url(id_inc, resolucion):
    """Cierra y solventa una incidencia activa. Redirige tras actuar."""
    try:
        inc = servicios.buscar_incidencia(id_inc)
        servicios.resolver(inc, resolucion)
        return redirect(url_for("listar_incidencias"))
    except ValueError as e:
        msg = str(e)
        if "No existe" in msg:
            return f"Error: {msg}", 404
        if "ya está resuelta" in msg:
            return f"Conflicto de estado: {msg}", 409
        return f"Petición incorrecta: {msg}", 400
    except ErrorPersistencia as e:
        return f"Error técnico en el UPDATE de SQLite: {e}", 500

@app.route("/incidencias/<int:id_inc>/documento")
def obtener_documento(id_inc):
    """Genera el acta PDF final (solo si está resuelta). Exige código 400 si está pendiente."""
    try:
        inc = servicios.buscar_incidencia(id_inc)
        if inc.estado != "Solventada":
            return "Petición Inválida: No se puede generar el acta PDF de un borrador pendiente.", 400
        doc = servicios.generar_documento(inc)
        return f"<strong>Documento Emitido:</strong> {doc}"
    except ValueError as e:
        return f"No encontrado: {e}", 404

@app.route("/incidencias/<int:id_inc>/relevo/<int:id_tecnico_entrante>")
def derivar_relevo(id_inc, id_tecnico_entrante):
    """Genera borrador de turno y envía una alerta al buzón del técnico entrante."""
    try:
        inc = servicios.buscar_incidencia(id_inc)
        tecnico_sig = servicios.obtener_tecnico(id_tecnico_entrante)
        
        doc = servicios.generar_documento(inc, tecnico_entrante=tecnico_sig)
        return f"<strong>Operación de Relevo Procesada:</strong> {doc}"
    except ValueError as e:
        return f"Error en identificadores: {e}", 404

#RUTAS AUXILIARES: TÉCNICOS Y SALAS

@app.route("/tecnicos")
def listar_tecnicos_web():
    """Lista todos los técnicos del catálogo relacional."""
    try:
        tecnicos = servicios.listar_tecnicos()
        lineas = [f"ID: {t.id_empleado} | Nombre: {t.nombre} | Turno: {t.turno}" for t in tecnicos]
        return "<h3>Catálogo de Técnicos</h3>" + "<br>".join(lineas)
    except ErrorPersistencia as e:
        return str(e), 500

@app.route("/tecnicos/<int:id_tecnico>")
def detalle_tecnico_web(id_tecnico):
    """Muestra la ficha individual del técnico."""
    try:
        t = servicios.obtener_tecnico(id_tecnico)
        return f"Técnico de Guardia: {t.nombre} <br> ID Empleado: {t.id_empleado} <br> Horario: {t.turno}"
    except ValueError as e:
        return str(e), 404

@app.route("/tecnicos/<int:id_tecnico>/avisos")
def ver_avisos_buzon(id_tecnico):
    """Devuelve los avisos acumulados en el buzón del técnico (Opción 3 de Consola)."""
    try:
        avisos = servicios.listar_avisos_tecnico(id_tecnico)
        return f"<h3>Buzón de Avisos (ID Técnico: {id_tecnico})</h3><pre>{avisos}</pre>"
    except ValueError as e:
        return str(e), 404

@app.route("/salas")
def listar_salas_web():
    """Lista todas las salas disponibles extraídas de SQLite."""
    try:
        salas = servicios.listar_salas()
        lineas = [f"ID Sala: {s.id_empleado} | Nombre: {s.nombre} | Ubicación: {s.ubicacion}" for s in salas]
        return "<h3>Salas Monitorizadas</h3>" + "<br>".join(lineas)
    except ErrorPersistencia as e:
        return str(e), 500

@app.route("/salas/<int:id_sala>")
def detalle_sala_web(id_sala):
    """Detalle individual de una infraestructura."""
    try:
        s = servicios.obtener_sala(id_sala)
        return f"Infraestructura: {s.nombre} <br> Sector: {s.ubicacion} <br> ID Base de Datos: {s.id_empleado}"
    except ValueError as e:
        return str(e), 404

# Entrada de inicialización estándar mediante módulo
if __name__ == "__main__":
    app.run(debug=True)