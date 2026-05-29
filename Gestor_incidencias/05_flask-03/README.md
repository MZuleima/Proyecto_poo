Aquí tienes tu archivo README.md actualizado para la Fase VII (versión 5.2.0). He reorganizado las secciones, reparado los bloques de código desalineados que venían del archivo anterior y añadido toda la descripción técnica sobre la incorporación del motor de renderizado Jinja2 y el patrón de herencia estructural de vistas.

Sustituye todo el contenido de tu README.md por esta versión definitiva:

Markdown
# Gestor de Incidencias Técnicas v5.2.0 — API Web con Plantillas Jinja2

Este proyecto consiste en un sistema de control crítico para la gestión y trazabilidad de incidencias en salas de control. En esta fase, la aplicación elimina el HTML inline de los controladores web y unifica su interfaz de usuario mediante el **motor de plantillas Jinja2**, implementando un diseño modular basado en herencia y bloques estructurados.

Gracias al diseño basado en **Clean Architecture**, todo el núcleo de lógica de negocio (Dominio), los casos de uso (Aplicación) y el motor relacional (SQLite en Infraestructura) se mantienen intactos y desacoplados de las interfaces de usuario.

---

## 🛠️ Tecnologías Utilizadas
- **Python 3.8+**
- **Flask 3.0.3** (Estructura de Control Web y Enrutamiento)
- **Jinja2** (Motor de Renderizado y Herencia de Plantillas HTML5)
- **Logging** (Módulo nativo de Python para auditoría en disco)
- **SQLite3** (Motor de persistencia permanente)
- **Unittest** (Batería de pruebas automatizadas del dominio)

---

## 🚀 Requisitos e Instalación

Para desplegar y probar la aplicación web, ejecuta los siguientes comandos desde la raíz de la carpeta `05-flask-03`:

1. **Instalar dependencias necesarias (Flask y Werkzeug):**
   ```bash
   pip install -r requirements.txt
Inicializar la base de datos física y los catálogos maestros:

Bash
python crear_bd.py
💻 Modos de Ejecución Disponibles
Modo 1: Servidor Web (API Flask con Vistas Jinja2)
Para levantar el servidor web dinámico con el motor de plantillas activo, ejecuta la aplicación como un módulo:

Bash
python -m presentation.app
El servidor estará escuchando peticiones en: http://127.0.0.1:5000/

Modo 2: Interfaz de Consola Clásica
El menú interactivo por terminal sigue estando operativo al 100% de manera concurrente compartiendo la base relacional. Para usarlo, abre otra terminal y ejecuta:

Bash
python main.py
🎨 Arquitectura de la Capa de Presentación Web
La interfaz gráfica se organiza de forma limpia en el directorio presentation/templates/ aplicando herencia estructural:

base.html: Esqueleto estructural global del sitio. Contiene el diseño CSS común y la barra de navegación superior unificada.

error.html: Plantilla común y dinámica reutilizada por los manejadores globales @app.errorhandler(404) y (500), asegurando que el usuario nunca pierda el menú de navegación al sufrir un fallo en la ruta.

Vistas de Lectura Colectoras: Archivos HTML independientes (bienvenida.html, incidencias.html, catalogos.html, ayuda.html) que extienden de la base e iteran colecciones de objetos mediante la sintaxis de Jinja2 ({% for %}, {% if %}).

🛣️ Mapeo de Rutas de la API Web
Las operaciones del dominio y las herramientas de diagnóstico se exponen a través de los siguientes endpoints:

⚙️ Observabilidad y Diagnóstico
GET /ayuda → Diccionario dinámico auto-actualizado que lee e imprime todas las rutas activas del servidor utilizando la plantilla ayuda.html.

GET /provocar-error → Endpoint de prueba diseñado para forzar un fallo crítico del código (ZeroDivisionError) y evaluar la respuesta dinámica de la plantilla error.html con estado HTTP 500.

gestor_incidencias.log → Archivo local que audita en disco de forma automática cada petición recibida de manera interceptada.

📝 Gestión de Incidencias
GET /incidencias → Devuelve el listado completo de incidencias mediante tablas estructuradas en incidencias.html.

GET /incidencias/<int:id_inc> → Detalle específico de una incidencia (404 si no existe).

GET /incidencias/nueva/<id_inc>/<id_tecnico>/<id_sala>/<descripcion> → Registra una nueva incidencia y redirige al listado general (409 si el ID ya existe, 400 si faltan datos).

GET /incidencias/<id_inc>/resolver/<resolucion> → Solventar y cerrar una incidencia (409 si ya estaba resuelta).

GET /incidencias/<id_inc>/documento → Genera el acta PDF final (solo si está resuelta).

GET /incidencias/<int:id_inc>/relevo/<int:id_tecnico_entrante> → Genera borrador y notifica al técnico entrante.

👥 Catálogos y Buzones (Auxiliares)
GET /tecnicos → Listado de personal técnico disponible renderizado en catalogos.html.

GET /tecnicos/<int:id_tecnico>/avisos → Consulta del buzón de avisos de relevo de un técnico.

GET /salas → Listado de infraestructuras monitorizadas renderizado en catalogos.html.

📂 Documentación del Proyecto
El desglose técnico detallado de esta fase se encuentra en los siguientes manuales de la carpeta docs/:

Ejecución del Sistema (docs/EJECUCION.md): Guía de despliegue, estructura jerárquica de plantillas y reporte de la prueba de coexistencia concurrente Web-Consola.

Arquitectura de Capas (docs/ARQUITECTURA_POR_CAPAS.md): Diagrama del flujo de dependencias e integración limpia de Flask.

Contrato del Repositorio (docs/CONTRATO_REPOSITORIO.md): Gestión del almacenamiento y traducción de excepciones en SQLite.