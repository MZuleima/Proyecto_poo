# Gestión de Datos Iniciales y Semillas (Seeds)

En esta fase, los catálogos maestros de personal y activos del sistema se han desvinculado por completo del código fuente de Python. Ahora residen de forma permanente en tablas relacionales dentro del archivo físico `incidencias.db`.

## 1. Inicialización del Entorno (`crear_bd.py`)
El sistema cuenta con un script de despliegue independiente denominado `crear_bd.py`. Este componente es el encargado de aplicar el código DDL (Data Definition Language) para crear la estructura e insertar los registros iniciales (datos semilla) para que el sistema pueda operar desde el primer minuto.

---

## 2. Diccionario de Datos Maestros

Los datos que se cargan automáticamente al arrancar la aplicación están estructurados en las siguientes tablas de SQLite:

### Tabla: `tecnicos`
Representa al personal disponible para la asignación de incidencias.
- **id**: `INTEGER` | Llave Primaria (PK). Identificador único del empleado.
- **nombre**: `TEXT` | Obligatorio (`NOT NOT NULL`). Nombre del técnico.
- **turno**: `TEXT` | Obligatorio (`NOT NOT NULL`). Turno asignado (Mañana, Tarde, Noche).

| id (PK) | nombre | turno |
| :--- | :--- | :--- |
| 1 | Juan | Mañana |
| 2 | Ana | Tarde |
| 3 | Pedro | Noche |

### Tabla: `salas`
Representa las ubicaciones físicas monitorizadas por el software.
- **id**: `INTEGER` | Llave Primaria (PK). Identificador de la sala.
- **nombre**: `TEXT` | Obligatorio (`NOT NOT NULL`). Nombre descriptivo.
- **ubicacion**: `TEXT` | Planta o sector del edificio.

| id (PK) | nombre | ubicacion |
| :--- | :--- | :--- |
| 1 | Sala de Emergencias | Planta 1 |
| 2 | Sala de Comunicaciones | Planta 0 |
| 3 | Sala de Control | Planta baja |

---

## 3. Integridad y Carga Segura
Para evitar la duplicidad de registros si el script de inicialización se ejecuta más de una vez, se utiliza la sentencia de rescate `INSERT OR IGNORE`. 

Además, el repositorio fuerza en cada conexión la directiva:
```sql
PRAGMA foreign_keys = ON;