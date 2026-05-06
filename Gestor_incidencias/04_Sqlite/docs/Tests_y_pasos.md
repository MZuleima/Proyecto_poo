# Pruebas Unitarias (Testing)

Se han implementado tests automatizados utilizando el framework `unittest` para asegurar que las reglas de negocio no se rompan en futuras actualizaciones.

## Cobertura de Tests
1. **Clase RegistroIncidencia**:
   - Validación de estados permitidos.
   - Validación de longitud mínima de resolución (mín. 5 carac.).
   - Registro automático de fecha de cierre.
2. **Clase Tecnico**:
   - Verificación de herencia desde la clase Trabajador.
   - Funcionamiento del sistema de avisos (notificaciones de relevo).

## Cómo ejecutar los tests
Desde la carpeta raíz del proyecto, ejecuta:
```bash
python -m unittest discover tests