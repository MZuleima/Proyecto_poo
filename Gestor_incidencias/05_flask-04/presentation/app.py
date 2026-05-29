#CAPA DE PRESENTACIÓN: Servidor Web Flask con Formularios POST y Patrón PRG
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

# Inicialización única e Inyección de Dependencia Relacional
path_db = "incidencias.db"
repo = RepositorioSQLite(path_db)
servicios = ServiciosIncidencias(repo)

# Hook de intercepción de peticiones para auditoría
@app.before_request
def registrar_peticion():
    logging.info(f"Petición: {request.method} {request.path} - IP: {request.remote_addr}")

#RUTAS DE LECTURA (GET)

@app.route("/")
def bienvenida():
    return render_template("bienvenida.html")

@app.route("/incidencias")
def listar_incidencias():
    try:
        incidencias = servicios.obtener_listado()
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

@app.route("/ayuda")
def mostrar_ayuda():
    reglas_filtradas = [r for r in app.url_map.iter_rules() if r.endpoint != 'static']
    return render_template("ayuda.html", mapa_rutas=reglas_filtradas)

#RUTAS DE ESCRITURA INTERACTIVAS (GET/POST)

@app.route("/incidencias/nueva", methods=['GET', 'POST'])
def crear_incidencia_web():
    # RAMA GET: Renderiza el formulario vacío cargando los selectores dinámicos
    if request.method == 'GET':
        try:
            tecnicos = servicios.listar_tecnicos()
            salas = servicios.listar_salas()
            return render_template("crear_incidencia.html", tecnicos=tecnicos, salas=salas, valores={})
        except ErrorPersistencia as e:
            return render_template("error.html", codigo=500, titulo="Error de Infraestructura", descripcion=str(e)), 500

    # RAMA POST: Procesa el envío de datos del formulario HTML
    if request.method == 'POST':
        # Recuperamos datos del diccionario request.form
        id_inc_raw = request.form.get("id_inc")
        id_tecnico_raw = request.form.get("id_tecnico")
        id_sala_raw = request.form.get("id_sala")
        descripcion = request.form.get("descripcion", "").strip()

        try:
            # Validación primaria de conversión de tipos
            id_inc = int(id_inc_raw)
            id_tecnico = int(id_tecnico_raw)
            id_sala = int(id_sala_raw)
            
            # Invocación de la lógica de negocio
            servicios.nueva_incidencia(id_inc, id_tecnico, id_sala, descripcion)
            
            # ÉXITO: Aplicamos el patrón Post/Redirect/Get redirigiendo al listado general
            return redirect(url_for("listar_incidencias"))
            
        except (ValueError, TypeError) as e:
            # Captura de errores de formato o validaciones del Dominio
            msg = str(e)
            cod = 409 if "Ya existe" in msg else (404 if "No existe" in msg else 400)
            
            # RE-RENDER con persistencia: recargamos los catálogos y devolvemos lo tecleado
            tecnicos = servicios.listar_tecnicos()
            salas = servicios.listar_salas()
            valores_introducidos = {
                "id_inc": id_inc_raw, "id_tecnico": id_tecnico_raw, 
                "id_sala": id_sala_raw, "descripcion": descripcion
            }
            return render_template("crear_incidencia.html", tecnicos=tecnicos, salas=salas, 
                                   valores=valores_introducidos, error=msg), cod
        except ErrorPersistencia as e:
            return render_template("error.html", codigo=500, titulo="Fallo Crítico en Base de Datos", descripcion=str(e)), 500


@app.route("/incidencias/<int:id_inc>/resolver", methods=['GET', 'POST'])
def resolver_incidencia_web(id_inc):
    try:
        inc = servicios.buscar_incidencia(id_inc)
    except ValueError as e:
        return render_template("error.html", codigo=404, titulo="Reporte No Encontrado", descripcion=str(e)), 404

    # RAMA GET: Renderiza la vista de resolución para la incidencia seleccionada
    if request.method == 'GET':
        return render_template("resolver_incidencia.html", inc=inc, valores={})

    # RAMA POST: Ejecuta la firma del acta y muta el estado
    if request.method == 'POST':
        resolucion = request.form.get("resolucion", "").strip()
        try:
            servicios.resolver(inc, resolucion)
            # ÉXITO: Redirección limpia (PRG)
            return redirect(url_for("listar_incidencias"))
        except ValueError as e:
            # RE-RENDER en caso de violación de estados o texto vacío
            valores_introducidos = {"resolucion": resolucion}
            return render_template("resolver_incidencia.html", inc=inc, valores=valores_introducidos, error=str(e)), 409
        except ErrorPersistencia as e:
            return render_template("error.html", codigo=500, titulo="Fallo de Persistencia Relacional", descripcion=str(e)), 500

#ACCIONES DE ESCRITURA PURA (SÓLO-POST)

@app.route("/incidencias/<int:id_inc>/documento", methods=['POST'])
def obtener_documento_post(id_inc):
    try:
        inc = servicios.buscar_incidencia(id_inc)
        if inc.estado != "Solventada": 
            return render_template("error.html", codigo=400, titulo="Acción Inválida", descripcion="La incidencia está abierta."), 400
        return servicios.generar_documento(inc)
    except ValueError as e: 
        return render_template("error.html", codigo=404, titulo="No Encontrado", descripcion=str(e)), 404

@app.route("/incidencias/<int:id_inc>/relevo/<int:id_tecnico_entrante>", methods=['POST'])
def derivar_relevo_post(id_inc, id_tecnico_entrante):
    try:
        inc = servicios.buscar_incidencia(id_inc)
        tecnico_sig = servicios.obtener_tecnico(id_tecnico_entrante)
        return servicios.generar_documento(inc, tecnico_entrante=tecnico_sig)
    except ValueError as e: 
        return render_template("error.html", codigo=404, titulo="Personal Inexistente", descripcion=str(e)), 404

#RUTAS SECUNDARIAS DE DIAGNÓSTICO

@app.route("/provocar-error")
def provocar_error_test():
    logging.info("Invocación deliberada de excepción")
    resultado_bloqueante = 1 / 0 
    return f"Inalcanzable: {resultado_bloqueante}"

#MANEJADORES GLOBALES DE ERROR

@app.errorhandler(404)
def error_no_encontrado(e):
    logging.warning(f"Error 404: {request.path}")
    return render_template("error.html", codigo=404, titulo="⚠️ Error 404: Recurso No Encontrado", 
                           descripcion="La dirección web o el recurso técnico solicitado no existe."), 404

@app.errorhandler(500)
def error_interno_servidor(e):
    logging.error(f"Error 500 Crítico: {e}", exc_info=True)
    return render_template("error.html", codigo=500, titulo="💥 Error 500: Fallo Interno del Servidor", 
                           descripcion="Ha ocurrido un error inesperado en el sistema de control."), 500

if __name__ == "__main__":
    app.run(debug=True)