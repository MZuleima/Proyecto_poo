# Registro de Cambios (Changelog)

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
- **Patrón "Actúa -> Redirige"**: Incorporación de redirecciones web explícitas mediante `redirect(url_for(...))` en las operaciones de mutación de datos (creación y resolución) para evitar reenvíos duplicados de peticiones.
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
- **Desacoplamiento de Errores**: Archivo `domain/excepciones.py` con las clases `ErrorPersistencia` y `RegistroNoEncontrado` para evitar la propagación de excepciones del driver de la base de datos a las capas superiores.
- **Seguridad contra Inyección SQL**: Implementación de consultas parametrizadas utilizando marcadores de posición (`?`) en todas las interacciones con la base de datos.
- **Integridad Relacional**: Activación explícitamente del control de claves foráneas mediante la directiva `PRAGMA foreign_keys = ON;`.

### Modificado
- `application/servicios.py`: El método `resolver()` ahora invoca explícitamente a `repo.guardar()` para sincronizar los cambios de estado ejecutando una sentencia `UPDATE` en la base de datos.
- `presentation/menu.py`: Modificado para inyectar la dependencia `RepositorioSQLite` y consumir dinámicamente los listados de técnicos y salas desde la persistencia relacional en lugar de objetos estáticos.

---

## [3.0.0] - Fase III: Testing
### Añadido
- Suite de pruebas unitarias en `tests/test_dominio.py`.
- Cobertura de tests para las clases `RegistroIncidencia` y `Tecnico`.
- Documentación técnica sobre cómo ejecutar y verificar los tests.