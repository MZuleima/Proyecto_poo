# Gestor de Incidencias Técnicas v5.0.0 — API Web con Flask

Este proyecto consiste en un sistema de control crítico para la gestión y trazabilidad de incidencias en salas de control. En esta fase, el sistema evoluciona incorporando **Flask** como una nueva capa de presentación web, conviviendo de forma limpia y paralela con el menú clásico de consola.

Gracias al diseño basado en **Clean Architecture**, todo el núcleo de lógica de negocio (Dominio), los casos de uso (Aplicación) y el motor relacional (SQLite en Infraestructura) se mantienen intactos y desacoplados de las interfaces de usuario.

---

## 🛠️ Tecnologías Utilizadas
- **Python 3.8+**
- **Flask 3.0.3** (Nueva capa de presentación de la API)
- **SQLite3** (Motor de persistencia permanente)
- **Unittest** (Batería de pruebas automatizadas del dominio)

---

## 🚀 Requisitos e Instalación

Para desplegar y probar la aplicación web, ejecuta los siguientes comandos desde la raíz de la carpeta `05-flask-01`:

1. **Instalar dependencias necesarias (Flask y Werkzeug):**
   ```bash
   pip install -r requirements.txt
Inicializar la base de datos física y los catálogos maestros:

Bash
python crear_bd.py
💻 Modos de Ejecución Disponibles
Modo 1: Servidor Web (API Flask)
Para levantar el servidor web dinámico, ejecuta la aplicación como un módulo:

Bash
python -m presentation.app
El servidor estará escuchando peticiones en: http://127.0.0.1:5000/

Modo 2: Interfaz de Consola Clásica
El menú interactivo por terminal sigue estando operativo al 100%. Para usarlo, abre otra terminal y ejecuta:

Bash
python main.py
🛣️ Mapeo de Rutas de la API Web
Las operaciones del dominio se exponen a través de los siguientes segmentos de URL dinámicos:

Gestión de Incidencias
GET /incidencias → Devuelve el listado completo de incidencias.

GET /incidencias/<int:id_inc> → Detalle específico de una incidencia (404 si no existe).

GET /incidencias/nueva/<id_inc>/<id_tecnico>/<id_sala>/<descripcion> → Registra una nueva incidencia y redirige al listado general (409 si el ID ya existe, 400 si faltan datos).

GET /incidencias/<id_inc>/resolver/<resolucion> → Solventar y cerrar una incidencia (409 si ya estaba resuelta).

GET /incidencias/<id_inc>/documento → Genera el acta PDF final (solo si está resuelta, 400 si está pendiente).

GET /incidencias/<id_inc>/relevo/<id_tecnico_entrante> → Genera borrador y notifica al técnico entrante.

Catálogos y Buzones (Auxiliares)
GET /tecnicos → Listado de personal técnico disponible.

GET /tecnicos/<int:id_tecnico>/avisos → Consulta del buzón de avisos de relevo de un técnico.

GET /salas → Listado de infraestructuras monitorizadas.

📂 Documentación del Proyecto
El desglose técnico detallado de esta fase se encuentra en los siguientes manuales de la carpeta docs/:

Ejecución del Sistema (docs/EJECUCION.md): Guía de despliegue paso a paso y batería de URLs de prueba HTTP.

Arquitectura de Capas (docs/ARQUITECTURA_POR_CAPAS.md): Diagrama del flujo de dependencias e integración limpia de Flask.

Contrato del Repositorio (docs/CONTRATO_REPOSITORIO.md): Gestión del almacenamiento y traducción de excepciones.