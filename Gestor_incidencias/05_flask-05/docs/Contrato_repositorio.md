# Contrato del Repositorio y Evolución de la Persistencia

Para evitar que el programa dependa de una base de datos específica o de tecnologías externas, se utiliza el principio de **Inversión de Dependencias (DIP)**.

## 1. El Contrato (Capa de Dominio)
- **Interfaz (`RepositorioIncidencias`)**: Define las operaciones obligatorias que cualquier almacén debe cumplir: `guardar()`, `obtener_todas()` y `buscar_por_id()`. El dominio exige qué se debe hacer, pero no cómo se hace.

## 2. Implementaciones (Capa de Infraestructura)
A lo largo del ciclo de vida del proyecto, el sistema ha soportado dos motores de persistencia distintos gracias a este diseño desacoplado:

* **`RepositorioMemoria` (Fase II/III)**: Guardaba los datos en listas y diccionarios volátiles de Python. Útil para pruebas rápidas y desarrollo inicial.
* **`RepositorioSQLite` (Fase IV - Actual)**: Traduce los objetos de dominio a sentencias SQL (`INSERT`, `UPDATE`, `SELECT` con `JOIN`) para almacenar la información de forma permanente en el archivo físico `incidencias.db`.

---

## 3. Desacoplamiento mediante Excepciones de Dominio

Un error común al implementar bases de datos es permitir que las excepciones propias del motor (como `sqlite3.Error` o `sqlite3.IntegrityError`) suban hasta la interfaz de usuario (Menú). Esto rompería la arquitectura por capas.

Para evitarlo, en esta fase se ha diseñado la siguiente estrategia de **traducción de excepciones**:

1. El `RepositorioSQLite` ejecuta la consulta dentro de un bloque `try/except`.
2. Si ocurre un fallo técnico o de restricciones, captura el error de SQLite.
3. Lanza en su lugar una excepción pura del dominio (`ErrorPersistencia` o `RegistroNoEncontrado`).

De este modo, el **Menú** y los **Servicios** solo tienen que gestionar errores genéricos del negocio, manteniendo la aplicación blindada ante fallos imprevistos de la base de datos o caídas del archivo.