# Reglas de Negocio

El sistema garantiza la integridad de la información mediante las siguientes reglas programadas en la capa de dominio:

1. **Protección de Datos (Encapsulamiento)**: Todos los atributos de la incidencia (`id`, `estado`, `fecha`) están protegidos (`_`). No se pueden modificar externamente sin pasar por validadores.
2. **Validación de Cierre**: No se permite marcar una incidencia como "Solventada" si la explicación técnica es nula o menor a 5 caracteres.
3. **Inmutabilidad de Apertura**: Una vez creada una incidencia, su `id`, `tecnico` original y `sala` no pueden ser modificados.
4. **Trazabilidad Temporal**: El sistema registra automáticamente la `fecha_apertura` al crear el objeto y la `fecha_cierre` al ejecutar el método `solventar()`.