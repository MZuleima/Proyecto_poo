# Arquitectura por Capas

El proyecto está diseñado bajo el patrón de **Arquitectura de Cebolla**, garantizando que el núcleo (negocio) sea independiente de la tecnología (base de datos o interfaz).

### Estructura de Carpetas:
- **`domain/`**: El núcleo. Contiene las reglas de negocio y los modelos de datos.
- **`application/`**: Orquestación. Traduce las acciones del usuario en cambios en el dominio.
- **`infrastructure/`**: Herramientas. Se encarga de la persistencia de datos (memoria) y la carga inicial.
- **`presentation/`**: Interfaz. Gestiona la entrada y salida de datos por consola.