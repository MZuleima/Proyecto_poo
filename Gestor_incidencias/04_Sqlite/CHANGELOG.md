# Registro de Cambios (Changelog)

## [4.0.0] - Fase IV: Persistencia con SQLite y Excepciones de Dominio
### Añadido
- **Persistencia Real**: Nueva clase `RepositorioSQLite` en la capa de infraestructura para sustituir el almacenamiento volátil en memoria.
- **Script de Inicialización**: Archivo `crear_bd.py` para la creación automatizada de tablas relacionales (`tecnicos`, `salas`, `incidencias`) e inserción de datos semilla (*seeds*).
- **Desacoplamiento de Errores**: Archivo `domain/excepciones.py` con las clases `ErrorPersistencia` y `RegistroNoEncontrado` para evitar la propagación de excepciones del driver de la base de datos a las capas superiores.
- **Seguridad contra Inyección SQL**: Implementación de consultas parametrizadas utilizando marcadores de posición (`?`) en todas las interacciones con la base de datos.
- **Integridad Relacional**: Activación explícita del control de claves foráneas mediante la directiva `PRAGMA foreign_keys = ON;`.

### Modificado
- `application/servicios.py`: El método `resolver()` ahora invoca explícitamente a `repo.guardar()` para sincronizar los cambios de estado ejecutando una sentencia `UPDATE` en la base de datos.
- `presentation/menu.py`: Modificado para inyectar la dependencia `RepositorioSQLite` y consumir dinámicamente los listados de técnicos y salas desde la persistencia relacional en lugar de objetos estáticos.

---

## [3.0.0] - Fase III: Testing
### Añadido
- Suite de pruebas unitarias en `tests/test_dominio.py`.
- Cobertura de tests para las clases `RegistroIncidencia` y `Tecnico`.
- Documentación técnica sobre cómo ejecutar y verificar los tests.

### Modificado
...