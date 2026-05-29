# Manual de Ejecución del Sistema (Consola y Web con Observabilidad)

El sistema soporta un doble entorno de presentación (interfaz de línea de comandos clásica y servidor API Web mediante Flask), ambos conectados al mismo motor de persistencia relacional SQLite. Esta versión incluye una capa de observabilidad para monitorizar el comportamiento del servidor en tiempo real.

## 1. Requisitos Previos e Instalación

Asegúrate de contar con Python 3.8 o superior. Antes de iniciar cualquiera de los entornos, es obligatorio instalar las dependencias del proyecto e inicializar el archivo de datos:

```bash
# 1. Instalar Flask, Werkzeug y dependencias del sistema
pip install -r requirements.txt

# 2. Inicializar la base de datos relacional (Tablas y Catálogos Semilla)
python crear_bd.py
2. Entorno Web (API Flask con Observabilidad)
Para arrancar la interfaz web del sistema como módulo de Python, ejecuta el siguiente comando en tu terminal:

Bash
python -m presentation.app
El servidor web se levantará en modo de desarrollo en: http://127.0.0.1:5000/

🔍 Herramientas de Observabilidad e Introspección
Introspección de Rutas (/ayuda):

Accede a http://127.0.0.1:5000/ayuda para ver un diccionario auto-actualizado en HTML con todos los endpoints registrados en el servidor. Si se añaden nuevas rutas en el código, este mapa las reflejará automáticamente sin mantenimiento manual.

Manejador Global de Errores 404 (Recurso No Encontrado):

Introduce cualquier URL aleatoria que no exista (ej. http://127.0.0.1:5000/servicios/criticos). El servidor interceptará la petición y renderizará una interfaz HTML personalizada estilizada con un aviso controlado en lugar de la página genérica del navegador.

Manejador Global de Errores 500 (Fallo Interno):

Para comprobar el aislamiento del servidor ante excepciones no controladas en el código, visita http://127.0.0.1:5000/provocar-error. El sistema forzará una división por cero de manera controlada, interceptará el crash, y mostrará una página HTML de emergencia técnica.

📋 Gestión y Auditoría de Logs (gestor_incidencias.log)
Cada interacción, ruta transitada o error crítico se almacena con marcas de tiempo explícitas en el archivo local gestor_incidencias.log gracias al hook interceptor before_request.

Ubicación: Se genera automáticamente en la raíz del proyecto.

Nota de Configuración: Para desactivar temporalmente el guardado en disco o modificar el nivel de captura (ej. pasar de INFO a WARNING en producción), se puede editar el parámetro level en la instrucción logging.basicConfig(...) al inicio de presentation/app.py.

Privacidad: Este archivo está excluido del control de versiones mediante .gitignore para salvaguardar los datos de auditoría local.

3. Interfaz de Consola Clásica (Menú)
Para ejecutar de manera paralela la terminal tradicional interactiva, abre otra pestaña en tu terminal y ejecuta:

Bash
python main.py
4. Verificación de Coexistencia Concurrente (Web ↔ Consola)
El sistema ha sido verificado con éxito operando simultáneamente bajo ambas interfaces de presentación sin provocar bloqueos (deadlocks) en la persistencia:

Flujo Web → Consola: Si registras una incidencia desde el navegador accediendo a la URL de inserción rápida (http://127.0.0.1:5000/incidencias/nueva/444/1/1/Fallo_de_alimentacion_UPS), el sistema procesará la petición y te redirigirá al listado web. Si inmediatamente acudes a la terminal de consola y solicitas el listado general, la incidencia 444 aparecerá listada al instante.

Flujo Consola → Web: Al dar de alta una incidencia utilizando el menú interactivo por teclado, la transacción se consolida en el archivo de SQLite de forma inmediata. Al refrescar la página web http://127.0.0.1:5000/incidencias, el nuevo registro se renderiza en la lista sin necesidad de reiniciar el servidor Flask.

5. Ejecución de Pruebas Automáticas
Para ejecutar la batería de pruebas unitarias sobre las reglas puras del negocio:

Bash
python -m unittest discover tests