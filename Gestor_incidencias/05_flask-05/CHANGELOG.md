# Registro de Cambios (Changelog)

## [0.8.0] - Fase VIII: Formularios HTML y Transacciones POST Seguro
### Añadido
- **Formularios de Escritura Estructurados**: Creación de las plantillas `crear_incidencia.html` y `resolver_incidencia.html` equipadas con etiquetas `<form method="POST">`, `<select>` dinámicos e inputs obligatorios.
- **Patrón Post/Redirect/Get (PRG)**: Implementación de redirecciones web explícitas (`redirect(url_for(...))`) tras procesar un `POST` con éxito, protegiendo al sistema contra el reenvío de datos por duplicado al pulsar F5.
- **Mecanismo de Re-renderizado con Persistencia**: Captura de excepciones de negocio del dominio en las ramas `POST` para volver a pintar el formulario conservando los datos tecleados y mostrando alertas rojas informativas.
- **Acciones Puras de Servidor Seguras**: Configuración de las rutas de emisión de actas y gestión de relevos para aceptar exclusivamente el método `POST`, bloqueando indexaciones automáticas o accesos accidentales vía `GET`.

### Modificado
- `presentation/app.py`: Reestructuración exhaustiva de los controladores de mutación para ramificar los ciclos de vida (`if request.method == 'POST'`) y extraer la información del cuerpo de la petición mediante `request.form`.
- `presentation/templates/incidencias.html`: Actualización de la tabla para integrar botones interactivos de redirección (`GET`) y pequeños formularios en línea para las acciones de escritura directa (`POST`).
- Documentación del proyecto: Actualización de `README.md` y `docs/EJECUCION.md` detallando la matriz operativa de verbos HTTP y los nuevos componentes de robustez de la interfaz.

---

## [0.7.0] - Fase VII: Plantillas Jinja2 (Separación de Vistas y Herencia)
### Añadido
- **Plantilla Base Estructural (`presentation/templates/base.html`)**: Implementación del esqueleto contenedor global HTML5 con los estilos CSS embebidos de la aplicación y la barra de navegación superior fija y unificada.
- **Plantilla Unificada de Errores (`presentation/templates/error.html`)**: Diseño común que hereda de la base para renderizar de forma dinámica los estados de error web (404 y 500) manteniendo la cabecera del sitio operativa para el usuario.
- **Plantillas Hijas de Lectura (`bienvenida.html`, `incidencias.html`, `catalogos.html`, `ayuda.html`)**: Archivos independientes especializados que extienden de `base.html` y aprovechan las directivas de control de Jinja2 (`{% for %}`, `{% if %}`) para iterar datos del backend.
- **Integración de `url_for`**: Sustitución de enlaces cableados a mano por el constructor nativo de rutas dinámicas de Flask en el menú global de navegación.

### Modificado
- `presentation/app.py`: Limpieza total del controlador web eliminando las cadenas de texto HTML inline. Refactorización de las rutas de lectura e introspección mediante el método `render_template` para delegar la interfaz al motor Jinja2.
- Documentación del proyecto: Actualización de `README.md` y `docs/EJECUCION.md` para detallar la nueva estructura del árbol de plantillas, la lógica de herencia y los componentes web añadidos.

---

## [0.6.0] - Fase VI: Observabilidad (Manejadores de Error, Introspección y Logging)
### Añadido
- **Manejador Global Error 404 (`@app.errorhandler(404)`)**: Captura centralizada de peticiones a rutas o recursos inexistentes para retornar una respuesta HTML personalizada y amigable.
- **Manejador Global Error 500 (`@app.errorhandler(500)`)**: Interceptor de excepciones críticas no controladas en el código; renderiza una página HTML de emergencia técnica y registra la traza interna en el archivo de log.
- **Ruta de Introspección Dinámica (`/ayuda`)**: Implementación del patrón de lectura en tiempo real mediante el mapeo de `app.url_map.iter_rules()`, excluyendo recursos estáticos para generar automáticamente un diccionario web de endpoints activos.
- **Hook de Intercepción (`@app.before_request`)**: Auditoría automática que registra el método HTTP, la ruta de acceso y la dirección IP de procedencia de cada petición entrante.
- **Persistencia de Eventos en Disco (`logging.basicConfig`)**: Inicialización del sistema de logging nativo configurado para escribir las trazas con marcas de tiempo en el archivo local `gestor_incidencias.log`.
- **Ruta Temporal de Diagnóstico (`/provocar-error`)**: Endpoint de prueba para forzar una excepción aritmética (`ZeroDivisionError`) y validar el comportamiento controlado del manejador de error 500.
- **Protección de Entorno (`.gitignore`)**: Adición de la directiva `*.log` para asegurar el aislamiento de las auditorías de operaciones locales y evitar su versionado en la nube.

### Modificado
- `presentation/app.py`: Reestructurado por completo para integrar de forma desacoplada las directrices de observabilidad sin alterar la API del dominio, las reglas de negocio ni los servicios de aplicación.
- Documentación del proyecto: Actualización de `README.md` y `docs/EJECUCION.md` para incluir el manual de uso del logging, la ruta de diagnóstico y las evidencias del informe de coexistencia concurrente entre la terminal y la interfaz web.

---

## [5.0.0] - Fase V: Flask como Capa de Presentación (Parte 1)
### Añadido
- **Servidor API Web (`presentation/app.py`)**: Implementación completa de la infraestructura web basada en Flask para exponer las operaciones del sistema a través de URLs dinámicas.
- **Parámetros Tipados**: Configuración de reglas de enrutamiento dinámico utilizando segmentos de datos estrictos (`<int:id_inc>`, `<int:id_sala>`).
- **Patrón "Actúa -> Redirige"**: Incorporación de redirecciones web explictas mediante `redirect(url_for(...))` en las operaciones de mutación de datos (creación y resolución) para evitar reenvíos duplicados de peticiones.
- **Traducción de Errores a Códigos HTTP**: Gestión centralizada de excepciones de negocio en cada ruta para responder con los estados nativos de la web: `400 Bad Request` para datos inválidos, `404 Not Found` para elementos inexistentes, y `409 Conflict` para violaciones de estado del dominio.
- **Mapeo de Catálogos**: Nuevas rutas para la lectura directa de las colecciones maestras de técnicos, salas y buzones de avisos (`notificacion_pendiente`).
- **Gestión de Entorno**: Archivo `requirements.txt` con las versiones estables y congeladas de Flask y Werkzeug.

### Modificado
- `application/servicios.py`: Ampliación de la API de servicios con 6 nuevos métodos controladores (`listar_tecnicos`, `obtener_tecnico`, `listar_salas`, `obtener_sala`, `buscar_incidencia`, `listar_avisos_tecnico`) para evitar el acceso directo de la presentación a los objetos de dominio.
- `presentation/menu.py`: Mantenido operativo al 100% y en paralelo al servidor web, compartiendo la misma base de datos sin fricciones.
- Actualizada toda la suite de documentación técnica en la carpeta `docs/` (`README.md`, `EJECUCION.md` y `ARQUITECTURA_POR_CAPAS.md`).

---

## [4.0.0] - Fase IV: Persistencia con SQLite y Excepciones de Dominio
### Añadido
- **Persistencia Real**: Nueva clase `RepositorioSQLite` en la capa de infraestructura para sustituir el almacenamiento volátil en memoria.
- **Script de Inicialización**: Archivo `crear_bd.py` para la creación automatizada de tablas relacionales (`tecnicos`, `salas`, `incidencias`) e inserción de datos semilla (*seeds*).
- **Desacoplamiento de Errores**: Archivo `domain/excepciones.py` con las clases `ErrorPersistencia` y `RegistroNoEncontrado` para evitar la propagación de excepciones

[0.10.0] - Fase IX: API REST y Gestión de Sesiones Seguras
Añadido
API REST (JSON): Implementación de endpoints de lectura (/api/incidencias y /api/incidencias/<id>) para el consumo programático de datos, utilizando serialización directa mediante métodos to_dict() en las entidades del dominio.

Sistema de Mensajes Flash: Integración de notificaciones transitorias de sesión (exito, info, error) mediante flash(), permitiendo un feedback dinámico y no intrusivo para el usuario.

Gestión de Sesiones: Configuración de app.secret_key para la firma y encriptación de cookies de sesión, requisito técnico indispensable para la persistencia temporal de los mensajes flash.

Sincronización de Rutas: Implementación de lógica en app.py y base.html para asegurar la consistencia del enrutamiento, eliminando errores BuildError mediante la eliminación de llamadas obsoletas y la actualización del mapa de rutas.

Modificado
presentation/app.py: Refactorización integral para incluir el soporte de jsonify y flash, además de la unificación de los manejadores de error.

presentation/templates/base.html: Inclusión del colector e iterador de mensajes flash en el layout principal para garantizar que las alertas aparezcan en todas las vistas.

presentation/templates/incidencias.html: Limpieza profunda del código HTML para eliminar formularios de acciones (derivar_relevo_post) que no contaban con soporte en el backend, optimizando la interfaz y la estabilidad.

Documentación del proyecto: Actualización de README.md incluyendo la nueva sección de API REST y guía de consumo mediante cURL.