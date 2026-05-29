# Gestor de Incidencias Técnicas v5.3.0 — Formularios Web y Transacciones POST Seguro

Este proyecto consiste en un sistema de control crítico para la gestión y trazabilidad de incidencias en salas de control. En esta fase, la aplicación securiza todas sus operaciones de mutación de estado eliminando el paso de parámetros sensibles por la URL, sustituyéndolas por **formularios HTML estructurados vía HTTP POST**, validación con re-renderizado persistente y el patrón estructural **PRG (Post/Redirect/Get)**.

Gracias al diseño basado en **Clean Architecture**, todo el núcleo de lógica de negocio (Dominio), los casos de uso (Aplicación) y el motor relacional (SQLite en Infraestructura) se mantienen intactos y desacoplados de las interfaces de usuario.

---

## 🛠️ Tecnologías Utilizadas
- **Python 3.8+**
- **Flask 3.0.3** (Estructura de Control Web y Gestión de Ciclos de Petición)
- **Jinja2** (Motor de Renderizado, Herencia de Componentes y Persistencia de Formularios)
- **Logging** (Módulo nativo de Python para auditoría en disco)
- **SQLite3** (Motor de persistencia permanente relacional)
- **Unittest** (Batería de pruebas automatizadas del dominio)

---

## 🚀 Requisitos e Instalación

Para desplegar y probar la aplicación web, ejecuta los siguientes comandos desde la raíz de la carpeta `05-flask-04`:

1. **Instalar dependencias necesarias (Flask y Werkzeug):**
   ```bash
   pip install -r requirements.txt
Inicializar la base de datos física y los catálogos maestros:

Bash
python crear_bd.py
💻 Modos de Ejecución Disponibles
Modo 1: Servidor Web (API Flask con Procesamiento POST Seguro)
Para levantar el servidor web dinámico con el soporte de formularios activo, ejecuta la aplicación como un módulo:

Bash
python -m presentation.app
El servidor estará escuchando peticiones en: http://127.0.0.1:5000/

Modo 2: Interfaz de Consola Clásica
El menú interactivo por terminal sigue estando operativo al 100% de manera concurrente compartiendo el motor SQLite. Para usarlo, abre otra terminal y ejecuta:

Bash
python main.py
🎨 Mecanismos de Robustez Web Añadidos
La capa de presentación web se ha rediseñado bajo los estándares de seguridad y usabilidad del desarrollo web:

Formularios Estructurados (<form method="POST">): Las acciones de inserción y resolución recopilan los datos de los inputs, textareas y selectores dinámicos, encapsulándolos en el cuerpo de la petición (request.form) de manera invisible en el historial de navegación.

Patrón Post/Redirect/Get (PRG): Tras un procesamiento exitoso en la persistencia, el controlador ejecuta un redirect(url_for(...)). Esto fuerza al navegador a pasar a un modo de lectura limpia (GET), evitando que el usuario duplique transacciones por error si refresca la pantalla pulsando F5.

Re-render con Persistencia: Si la lógica de negocio del dominio rechaza una operación (por ejemplo, un ID duplicado), la aplicación intercepta la excepción, asocia el código HTTP correspondiente (400 o 409) y vuelve a pintar el formulario conservando los textos que el usuario ya había escrito junto a un cartel de alerta.

🛣️ Mapeo de Rutas de la API Web
Las operaciones del sistema se exponen bajo la siguiente matriz estricta de verbos HTTP:

⚙️ Observabilidad, Diagnóstico y Lectura (GET)
GET / → Renderiza la pantalla de inicio limpia (bienvenida.html).

GET /incidencias → Devuelve el listado completo de incidencias mediante tablas estructuradas en incidencias.html.

GET /tecnicos → Listado del personal técnico disponible renderizado en catalogos.html.

GET /salas → Listado de infraestructuras monitorizadas renderizado en catalogos.html.

GET /ayuda → Diccionario dinámico auto-actualizado de endpoints del servidor.

GET /provocar-error → Endpoint de prueba diseñado para simular un fallo interno (500).

📝 Formularios e Interacciones de Escritura (GET/POST)
GET /incidencias/nueva → Carga el formulario de registro vacío con selectores dinámicos.

POST /incidencias/nueva → Valida, procesa y da de alta una nueva incidencia (Aplica PRG o Re-render).

GET /incidencias/<int:id_inc>/resolver → Carga la pantalla de cierre técnico para la incidencia indicada.

POST /incidencias/<int:id_inc>/resolver → Inserta la solución técnica y clausura el reporte en SQLite.

🚫 Acciones Puras de Servidor (SÓLO-POST)
POST /incidencias/<int:id_inc>/documento → Genera y emite el acta de cierre técnica (Rechaza accesos GET con un 405).

POST /incidencias/<int:id_inc>/relevo/<int:id_tecnico_entrante> → Registra una alerta en el buzón del técnico entrante (Rechaza accesos GET con un 405).

📂 Documentación del Proyecto
El desglose técnico detallado de esta fase se encuentra en los siguientes manuales de la carpeta docs/:

Ejecución del Sistema (docs/EJECUCION.md): Guía de despliegue, matriz exhaustiva de verbos HTTP y especificaciones del patrón defensivo PRG.

Arquitectura de Capas (docs/ARQUITECTURA_POR_CAPAS.md): Diagrama del flujo de dependencias e integración limpia de Flask.

Contrato del Repositorio (docs/CONTRATO_REPOSITORIO.md): Gestión del almacenamiento y traducción de excepciones en SQLite.