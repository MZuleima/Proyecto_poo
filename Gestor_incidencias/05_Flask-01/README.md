# Proyecto modelo. Máquina expendedora de refrescos y snacks

## Ejecución del proyecto

<details>
  <summary>Fase 04 - persistencia con SQLite</summary>

### Diseño e implementación del esquema de base de datos

- [ ] Copiar en `04-sqlite` el estado base de `03-testing` (o crear rama específica para la fase 04).
- [ ] Diseñar las tablas SQL mapeando cada entidad de dominio a tablas con sus columnas, tipos y restricciones (`PRIMARY KEY`, `NOT NULL`, `FOREIGN KEY`).
- [ ] Usar nombres de columnas en snake_case.

### Script de inicialización de base de datos

- [ ] Crear script que cree el esquema de la BD e inserte datos iniciales de prueba
  - Debe poder ejecutarse varias veces sin error
  - Crea todas las tablas respetando dependencias de claves foráneas
  - Inserta datos iniciales para probar la aplicación

### Excepciones de dominio para persistencia

- [ ] (*opcional*) Crear fichero de excepciones (`infrastructure/errores.py`) con las excepciones que el repositorio SQLite lanza al usuario
  - Clase base para todas las excepciones de persistencia
  - Excepciones por cada tipo de error que puede ocurrir (duplicado, no encontrado, etc.)

### Implementación del repositorio SQLite

- [ ] Crear clase(s) de repositorio que implementen persistencia en SQLite (realizando las mismas operaciones que el repositorio en memoria: guardar, obtener, actualizar, eliminar, etc.)
- [ ] Usar consultas SQL parametrizadas (parámetros `?`) para prevenir inyección SQL
- [ ] Capturar excepciones SQLite (`sqlite3.IntegrityError`, `sqlite3.OperationalError`, etc.) y transformarlas en excepciones de dominio
- [ ] Activar `PRAGMA foreign_keys = ON` al conectar para garantizar integridad referencial
- [ ] **El flujo principal de la aplicación (menú) debe usar SOLO el repositorio SQLite para persistencia** (no usar en memoria)

### Repositorio en memoria (referencia, no en uso)

- [ ] (**opcional**) Mantener el código del repositorio en memoria como referencia de implementación y contrato
- [ ] (**opcional**) Modificar `infrastructure/repositorio_memoria.py` para lanzar las **mismas excepciones de dominio** que el repositorio SQLite (útil para tests sin persistencia)

### Integración con SQLite en la capa de presentación

- [ ] Modificar la capa de presentación para cargar datos iniciales desde la BD en lugar de desde memoria (al iniciar la aplicación)
- [ ] Capturar excepciones de dominio, no excepciones de `sqlite3`
- [ ] (*opcional*) Mostrar mensajes amigables al usuario cuando ocurran errores de persistencia
- [ ] No hacer imports de `sqlite3` directamente en la presentación.

### Actualización de los tests

- [ ] *(opcional)* Actualizar tests existentes para esperar excepciones de dominio en lugar de excepciones genéricas de Python
- [ ] Verificar que `python -m unittest` pasa con todos los tests en verde
- [ ] *(opcional)* Crear tests específicos para el repositorio SQLite

### Documentación

- [ ] Actualizar `CHANGELOG.md` (versión `0.4.0`) con los cambios principales
- [ ] Actualizar `README.md` con instrucciones de cómo ejecutar el script de inicialización
- [ ] Documentar el diseño de la BD en `docs/DISEÑO_BD.md`:
- [ ] (*opcional*) Documentar el contrato de excepciones en `docs/CONTRATO_EXCEPCIONES.md`:

### Verificación final

- [ ] La aplicación funciona igual desde el punto de vista del usuario (mismo menú, mismas operaciones)
- [ ] Los datos persisten entre ejecuciones (cierra y reabre la app, verifica que los datos están)
- [ ] Los tests pasan todos sin cambios de lógica de dominio

</details>