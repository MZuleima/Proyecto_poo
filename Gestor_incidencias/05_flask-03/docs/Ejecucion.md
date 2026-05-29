# Manual de Ejecución del Sistema (Consola y Web con Plantillas Jinja2)

El sistema soporta un doble entorno de presentación (interfaz de línea de comandos clásica y servidor API Web mediante Flask), ambos conectados al mismo motor de persistencia relacional SQLite. Esta versión desacopla el diseño visual del código de control migrando toda la presentación a plantillas motorizadas por **Jinja2**.

## 1. Requisitos Previos e Instalación

Asegúrate de contar con Python 3.8 o superior. Antes de iniciar cualquiera de los entornos, es obligatorio instalar las dependencias del proyecto e inicializar el archivo de datos:

```bash
# 1. Instalar Flask, Werkzeug y dependencias del sistema
pip install -r requirements.txt

# 2. Inicializar la base de datos relacional (Tablas y Catálogos Semilla)
python crear_bd.py
2. Entorno Web (API Flask con Motor Jinja2)
Para arrancar la interfaz web del sistema como módulo de Python, ejecuta el siguiente comando en tu terminal:

Bash
python -m presentation.app
El servidor web se levantará en modo de desarrollo en: http://127.0.0.1:5000/

🎨 Arquitectura de Vistas Dinámicas (presentation/templates/)
La capa de presentación web se ha unificado bajo el patrón de diseño por herencia de Jinja2, eliminando cualquier rastro de HTML inline en los controladores del backend:

Estructura Base (base.html): Actúa como el esqueleto contenedor global de la aplicación. Define los estilos estructurados y la barra de navegación superior unificada.

Bloques Dinámicos ({% block content %}): Las plantillas hijas (bienvenida.html, incidencias.html, catalogos.html y ayuda.html) extienden automáticamente de la base inyectando sus datos estructurados (tablas relacionales, badges de estado e iteradores de colecciones).

🔍 Herramientas de Diagnóstico y Control de Errores
Introspección de Rutas (/ayuda):

Accede a http://127.0.0.1:5000/ayuda para examinar el listado auto-actualizado de endpoints. Renderiza dinámicamente las propiedades del mapa de rutas activo de Flask dentro de una estructura limpia heredada de base.html.

Plantilla Común de Errores (error.html):

Los manejadores globales para estados 404 (Not Found) y 500 (Internal Server Error) ahora comparten una plantilla unificada. Al visitar una URL inválida o forzar un fallo del sistema mediante http://127.0.0.1:5000/provocar-error, la respuesta altera sus colores y textos informativos de forma dinámica, garantizando que la cabecera y el menú de navegación sigan siendo visibles para el usuario.

📋 Gestión y Auditoría de Logs (gestor_incidencias.log)
Cada interacción, ruta transitada o error crítico se almacena con marcas de tiempo explícitas en el archivo local gestor_incidencias.log gracias al hook interceptor before_request.

Ubicación: Se genera automáticamente en la raíz del proyecto.

Privacidad: Este archivo está excluido del control de versiones de Git mediante el archivo .gitignore.

3. Interfaz de Consola Clásica (Menú)
Para ejecutar de manera paralela la terminal tradicional interactiva, abre otra pestaña en tu terminal y ejecuta:

Bash
python main.py
4. Verificación de Coexistencia Concurrente (Web ↔ Consola)
El sistema ha sido verificado con éxito operando simultáneamente bajo ambas interfaces de presentación sin provocar bloqueos (deadlocks) en la persistencia:

Flujo Web → Consola: Si registras una incidencia desde el navegador accediendo a la URL de inserción rápida (http://127.0.0.1:5000/incidencias/nueva/444/1/1/Fallo_de_alimentacion_UPS), el sistema procesará la petición y te redirigirá al listado web estructurado. Si inmediatamente acudes a la terminal de consola y solicitas el listado general, la incidencia 444 aparecerá listada al instante.

Flujo Consola → Web: Al dar de alta una incidencia utilizando el menú interactivo por teclado, la transacción se consolida en el archivo de SQLite de forma inmediata. Al refrescar la página web http://127.0.0.1:5000/incidencias, el nuevo registro se renderiza en la lista Jinja2 con su respectivo componente badge sin necesidad de reiniciar el servidor Flask.

5. Ejecución de Pruebas Automáticas
Para ejecutar la batería de pruebas unitarias sobre las reglas puras del negocio:

Bash
python -m unittest discover tests