# Arquitectura por Capas e Integración de Flask

El diseño de este sistema se rige bajo los principios de la **Arquitectura Limpia (Clean Architecture)** o Arquitectura de Cebolla. La regla fundamental es que las capas externas pueden depender de las internas, pero las capas internas jamás conocen la existencia de las externas.

## 1. Estructura de Dependencias de la Fase V

Con la incorporación de Flask, el sistema demuestra la potencia de este desacoplamiento. Ahora disponemos de **dos mecanismos de presentación paralelos** que consumen las mismas reglas de negocio sin duplicar una sola línea de lógica:

              [ presentation/menu.py ] (Consola)
                         │
                         ▼
[ presentation/app.py ] ───┼──► [ application/servicios.py ] ──► [ domain/ ] (Reglas puras)
(Flask Web)         │             (Casos de Uso)
▼
[ infrastructure/repositorio_sqlite.py ]
│
▼
[ incidencias.db ]


---

## 2. Desglose de Responsabilidades por Capa

### A. Capa de Dominio (`domain/`)
- **Componentes**: `RegistroIncidencia`, `Tecnico`, `SalaControl`, `excepciones.py`.
- **Aislamiento**: Es el núcleo más interno. No sabe qué es SQLite ni sabe qué es Flask. Define las entidades de negocio y los errores permitidos (ej. resoluciones cortas, estados duplicados).

### B. Capa de Aplicación (`application/`)
- **Componentes**: `ServiciosIncidencias`.
- **Orquestación**: Expone los casos de uso del sistema. En esta fase se han unificado todas las búsquedas de ID numéricos y catálogos en esta capa para que la presentación no tenga que interactuar con colecciones de dominio directamente.

### C. Capa de Infraestructura (`infrastructure/`)
- **Componentes**: `RepositorioSQLite`.
- **Persistencia**: Implementa el almacenamiento en la base de datos relacional. Traduce objetos de dominio en sentencias SQL parametrizadas para evitar ataques de Inyección SQL.

### D. Capa de Presentación (`presentation/`)
En esta versión, la capa se duplica limpiamente en dos controladores autónomos:
1. **`menu.py` (CLI)**: Captura las interacciones por teclado del operario en local.
2. **`app.py` (Web Flask)**: Mapea la API mediante segmentos de URL dinámicos (`<int:id_inc>`), traduce las excepciones de negocio del dominio en códigos de respuesta estándar de Internet (`400`, `404`, `409`), y reconduce los flujos mediante redirecciones HTTP directas.

---

## 3. Beneficios del Diseño en esta Fase
- **Intercambiabilidad**: Si el día de mañana se decide eliminar la interfaz web de Flask por una interfaz gráfica en móviles o escritorio, el código de las carpetas `domain`, `application` e `infrastructure` permanecerá intacto al 100%.
- **Robustez contra caídas**: Las rutas de Flask controlan los errores de las capas inferiores a nivel de HTTP, garantizando que un error de un usuario (como buscar un ID de incidencia que no existe) resulte en un código `404 Not Found` controlado en el navegador, en lugar de provocar la caída (*crash*) del servidor web.