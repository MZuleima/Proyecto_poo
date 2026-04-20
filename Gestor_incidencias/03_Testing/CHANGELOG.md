# Registro de Cambios (Changelog)

## [2.0.0] - Fase II: Documentando
### Añadido
- Comentarios Docstring en todas las clases y métodos.
- Validación de longitud en las resoluciones de incidencias.
- Carpeta `docs/` con toda la documentación técnica.
- Archivos Markdown para descripción, arquitectura y reglas de negocio.

### Corregido
- Error de cierre de bloques `try/except` en el menú.
- Error de módulos no encontrados (`ModuleNotFoundError`) al organizar las carpetas.

## [3.0.0] - Fase III: Testing
### Añadido
- Suite de pruebas unitarias en `tests/test_dominio.py`.
- Cobertura de tests para las clases `RegistroIncidencia` y `Tecnico`.
- Documentación técnica sobre cómo ejecutar y verificar los tests.