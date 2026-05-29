# Gestor de Incidencias Técnicas v5.1.0 — API Web con Observabilidad

Este proyecto consiste en un sistema de control crítico para la gestión y trazabilidad de incidencias en salas de control. En esta fase, la aplicación consolida su arquitectura web con Flask mediante la incorporación de una **capa de observabilidad global** que incluye interceptores de peticiones, diagnóstico de rutas por introspección y manejadores de error HTML personalizados.

Gracias al diseño basado en **Clean Architecture**, todo el núcleo de lógica de negocio (Dominio), los casos de uso (Aplicación) y el motor relacional (SQLite en Infraestructura) se mantienen intactos y desacoplados de las interfaces de usuario.

---

## 🛠️ Tecnologías Utilizadas
- **Python 3.8+**
- **Flask 3.0.3** (Presentación Web y Endpoints de Diagnóstico)
- **Logging** (Módulo nativo de Python para auditoría en disco)
- **SQLite3** (Motor de persistencia permanente)
- **Unittest** (Batería de pruebas automatizadas del dominio)

---

## 🚀 Requisitos e Instalación

Para desplegar y probar la aplicación, ejecuta los siguientes comandos desde la raíz de la carpeta `05-flask-02`:

1. **Instalar dependencias necesarias (Flask y Werkzeug):**
   ```bash
   pip install -r requirements.txt
Inicializar la base de datos física y los catálogos maestros:

Bash
python crear_bd.py
💻 Modos de Ejecución Disponibles
Modo 1: Servidor Web (API Flask)
Para levantar el servidor web dinámico con el sistema de rastreo activo, ejecuta la aplicación como un módulo:

Bash
python -m presentation.app
El servidor estará escuchando peticiones en: http://127.0.0.1:5000/

Modo 2: Interfaz de Consola Clásica
El menú interactivo por terminal sigue estando operativo al 100% de manera concurrente. Para usarlo, abre otra terminal y ejecuta:

Bash
python main.py
🛣️ Mapeo de Rutas de la API Web
Las operaciones del dominio y las herramientas de diagnóstico se exponen a través de los siguientes endpoints:

⚙️ Observabilidad y Diagnóstico (Nuevos)
GET /ayuda → Diccionario dinámico auto-actualizado que lee e imprime todas las rutas activas del servidor en tiempo real.

GET /provocar-error → Endpoint de prueba diseñado para forzar un fallo crítico del código (ZeroDivisionError) y evaluar el aislamiento del manejador de error 500.

gestor_incidencias.log → Archivo local que audita en disco de forma automática cada petición recibida con su timestamp, método HTTP e IP de procedencia.

📝 Gestión de Incidencias
GET /incidencias → Devuelve el listado completo de incidencias.

GET /incidencias/<int:id_inc> → Detalle específico de una incidencia (404 si no existe).

GET /incidencias/nueva/<id_inc>/<id_tecnico>/<id_sala>/<descripcion> → Registra una nueva incidencia y redirige al listado general (409 si el ID ya existe, 400 si faltan datos).

GET /incidencias/<id_inc>/resolver/<resolucion> → Solventar y cerrar una incidencia (409 si ya estaba resuelta).

GET /incidencias/<id_inc>/documento → Genera el acta PDF final (solo si está resuelta, 400 si está pendiente).

GET /incidencias/<int:id_inc>/relevo/<int:id_tecnico_entrante> → Genera borrador y notifica al técnico entrante.

👥 Catálogos y Buzones (Auxiliares)
GET /tecnicos → Listado de personal técnico disponible.

GET /tecnicos/<int:id_tecnico>/avisos → Consulta del buzón de avisos de relevo de un técnico.

GET /salas → Listado de infraestructuras monitorizadas.

📂 Documentación del Proyecto
El desglose técnico detallado de esta fase se encuentra en los siguientes manuales de la carpeta docs/:

Ejecución del Sistema (docs/EJECUCION.md): Guía de despliegue, batería de URLs de prueba y reporte de la prueba de coexistencia concurrente Web-Consola.

Arquitectura de Capas (docs/ARQUITECTURA_POR_CAPAS.md): Diagrama del flujo de dependencias e integración limpia de Flask.

Contrato del Repositorio (docs/CONTRATO_REPOSITORIO.md): Gestión del almacenamiento y traducción de excepciones en SQLite.