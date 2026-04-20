# Contrato del Repositorio

Para evitar que el programa dependa de una base de datos específica, se utiliza la **Inversión de Dependencias**.

- **Interfaz (`RepositorioIncidencias`)**: Define que cualquier almacén debe tener los métodos `guardar()`, `obtener_todas()` y `buscar_por_id()`.
- **Implementación Actual (`RepositorioMemoria`)**: Guarda los datos en listas de Python. Esto permite probar el programa sin necesidad de instalar bases de datos complejas como MySQL o MongoDB.