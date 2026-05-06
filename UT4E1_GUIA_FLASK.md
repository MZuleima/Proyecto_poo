# Guía de rutas Flask — Gestor de Incidencias Técnicas

**Alumna:** Zule  
**Actividad:** ut4e1 — Exposición de la API del dominio como routes Flask  
**Fuente de verdad:** `Gestor_incidencias/03_Testing/`  
**Fecha de última revisión:** 2026-04-24

---

## 1. Dominio

Sistema de gestión de incidencias técnicas en salas de control. Los actores principales son:

- **Técnico**: trabajador con turno asignado y buzón de avisos de relevo.
- **SalaControl**: lugar físico donde ocurre la incidencia.
- **RegistroIncidencia**: entidad central; agrupa técnico, sala, descripción y ciclo de vida del estado.

---

## 2. Inventario completo del menú actual (`presentation/menu.py`)

| Opción | Título en pantalla | Acción |
|--------|--------------------|--------|
| 1 | Registrar nueva incidencia | `servicios.nueva_incidencia(id_inc, tecnico, sala, desc)` |
| 2 | Resolver incidencia (Cierre) | `servicios.resolver(incidencia, resolucion)` |
| 3 | Ver avisos de técnicos (Relevo) | `tecnico.leer_aviso()` (acceso directo al dominio — pendiente de pasar por servicio) |
| 4 | Generar informe técnico (PDF/Borrador) | `servicios.generar_documento(inc, tecnico_entrante?)` |
| 0 | Salir | — |

> **Nota de diseño:** la opción 3 accede actualmente al objeto `Tecnico` directamente desde la presentación. La API Flask debe enrutar esa operación a través del servicio añadiendo `listar_avisos_tecnico(id_tecnico)` (ver sección 5).

---

## 3. Métodos actuales de `ServiciosIncidencias` (`application/servicios.py`)

| Método | Firma completa | Descripción |
|--------|---------------|-------------|
| `__init__` | `__init__(self, repositorio)` | Inyecta el repositorio. |
| `nueva_incidencia` | `nueva_incidencia(self, id_inc, tecnico, sala, desc)` | Crea `RegistroIncidencia` y lo guarda en el repositorio. |
| `obtener_listado` | `obtener_listado(self)` | Devuelve la lista completa de incidencias. |
| `resolver` | `resolver(self, incidencia, resolucion)` | Delega en `incidencia.solventar(resolucion)`. |
| `generar_documento` | `generar_documento(self, obj_incidencia, tecnico_entrante=None)` | Retorna PDF final si está solventada, o borrador notificando al técnico de relevo. |

---

## 4. Rutas sugeridas (toda la API)

La tabla cubre todas las operaciones del menú más las auxiliares necesarias para que la presentación no manipule objetos de dominio directamente.

Los parámetros de creación/modificación se pasan como segmentos de URL.

### Incidencias

| Ruta Flask | Método del servicio | Descripción |
|------------|---------------------|-------------|
| `/incidencias` | `obtener_listado()` | Lista todas las incidencias. |
| `/incidencias/<int:id_inc>` | `buscar_incidencia(id_inc)` | Detalle de una incidencia; 404 si no existe. |
| `/incidencias/nueva/<int:id_inc>/<int:id_tecnico>/<int:id_sala>/<descripcion>` | `nueva_incidencia(id_inc, id_tecnico, id_sala, descripcion)` | Registra una incidencia nueva. |
| `/incidencias/<int:id_inc>/resolver/<resolucion>` | `resolver(incidencia, resolucion)` | Cierra la incidencia con la resolución indicada. |
| `/incidencias/<int:id_inc>/documento` | `generar_documento(incidencia)` | Genera PDF final (solo si está solventada). |
| `/incidencias/<int:id_inc>/relevo/<int:id_tecnico_entrante>` | `generar_documento(incidencia, tecnico_entrante)` | Genera borrador y notifica al técnico entrante. |

### Técnicos

| Ruta Flask | Método del servicio | Descripción |
|------------|---------------------|-------------|
| `/tecnicos` | `listar_tecnicos()` (**a añadir**) | Lista todos los técnicos. |
| `/tecnicos/<int:id_tecnico>` | `obtener_tecnico(id_tecnico)` (**a añadir**) | Detalle de un técnico. |
| `/tecnicos/<int:id_tecnico>/avisos` | `listar_avisos_tecnico(id_tecnico)` (**a añadir**) | Devuelve todos los avisos del buzón de un técnico (≡ opción 3 del menú). |

### Salas

| Ruta Flask | Método del servicio | Descripción |
|------------|---------------------|-------------|
| `/salas` | `listar_salas()` (**a añadir**) | Lista todas las salas disponibles. |
| `/salas/<int:id_sala>` | `obtener_sala(id_sala)` (**a añadir**) | Detalle de una sala. |

### Ejemplo: cómo quedaría `app.py` con dos rutas ya hechas

El siguiente fragmento muestra la estructura mínima de `app.py` con dos rutas implementadas
para que puedas tomar el patrón y aplicarlo al resto:

```python
from flask import Flask
from application.servicios import ServiciosIncidencias
from infrastructure.datos_iniciales import RepositorioMemoria

app = Flask(__name__)

repo = RepositorioMemoria()
servicios = ServiciosIncidencias(repo)


@app.route("/")
def bienvenida():
    return (
        "Bienvenido al gestor de incidencias técnicas\n"
        "  /incidencias  → lista todas las incidencias\n"
    )


@app.route("/incidencias")
def listar_incidencias():
    incidencias = servicios.obtener_listado()
    if not incidencias:
        return "No hay incidencias registradas."
    return "\n".join(str(i) for i in incidencias)


if __name__ == "__main__":
    app.run(debug=True)
```

**Lo que hace cada parte:**

- El repositorio y el servicio se crean **una sola vez** fuera de las vistas, al arrancar la
  aplicación. Así todas las rutas comparten el mismo estado en memoria.
- Cada función de vista llama al método del servicio correspondiente y devuelve texto plano.
- Para rutas con `ValueError` puedes devolver una tupla `(mensaje, código)`:
  `return "No encontrado", 404` o `return "Ya existe", 409`.

---

## 5. Métodos a añadir en `ServiciosIncidencias`

Los siguientes métodos no existen aún pero son necesarios para que la capa de presentación Flask no acceda a objetos de dominio directamente (problema de diseño ya señalado en REVIEW_2026_04_22.md).

| Método | Firma sugerida | Propósito |
|--------|---------------|-----------|
| `listar_tecnicos` | `listar_tecnicos(self)` | Retorna la lista de técnicos (actualmente solo accesible vía `RepositorioMemoria.cargar_tecnicos()`). |
| `obtener_tecnico` | `obtener_tecnico(self, id_tecnico: int)` | Localiza un técnico por su `id_empleado`. Lanza `ValueError` si no existe. |
| `listar_salas` | `listar_salas(self)` | Retorna la lista de salas disponibles. |
| `obtener_sala` | `obtener_sala(self, id_sala: int)` | Localiza una sala por índice o identificador. Lanza `ValueError` si no existe. |
| `listar_avisos_tecnico` | `listar_avisos_tecnico(self, id_tecnico: int)` | Localiza el técnico y retorna su lista de avisos (`notificacion_pendiente`). Encapsula el acceso al dominio. |
| `buscar_incidencia` | `buscar_incidencia(self, id_inc: int)` | Envuelve `self.repo.buscar_por_id(id_inc)` con control de `None` → `ValueError`. |

> Con estos métodos, `nueva_incidencia` puede recibir `id_tecnico: int` e `id_sala: int` en lugar de objetos de dominio, resolviendo el bug de diseño señalado en la revisión.

---

## 6. Errores disponibles y su traducción a HTTP

Los errores del dominio deben capturarse en la route y devolver el mensaje con el código HTTP apropiado.

| Excepción en dominio | Causa | Código HTTP sugerido |
|----------------------|-------|----------------------|
| `ValueError("Ya existe una incidencia con ese ID")` | ID duplicado al registrar | `409 Conflict` |
| `ValueError("La resolución es demasiado corta...")` | Resolución < 5 caracteres | `400 Bad Request` |
| `ValueError("Estado inválido...")` | Estado no permitido | `400 Bad Request` |
| `ValueError("La incidencia ya está resuelta")` | Resolver una incidencia ya solventada | `409 Conflict` |
| `ValueError("No existe técnico/sala/incidencia con ese ID")` | Recurso no encontrado | `404 Not Found` |
| `ValueError("Descripción vacía")` | Descripción en blanco al crear | `400 Bad Request` |

> Los `ValueError` de `ValueError("La resolución es demasiado corta...")` y `ValueError("Estado inválido...")` ya están implementados en los setters de `RegistroIncidencia`. Los demás están pendientes de implementación (ver REVIEW_2026_04_22.md, sección Fase 01 — Bugs).

---

## 7. Advertencias

### 7.1. Máquina de estados de la incidencia (es decir, el estado solo puede avanzar en un orden concreto y no puede volver atrás)

El dominio actual implementa los estados: `Pendiente` → `Solventada` y `Pendiente` → `Cancelada`.

```
[Pendiente] ──solventar()──▶ [Solventada]
[Pendiente] ──(cancelar)──▶ [Cancelada]   ← estado permitido, pero sin método ni route todavía
```

- `Solventada` es un **estado terminal**: no se puede volver a `Pendiente` ni volver a resolver.
- `Cancelada` está como valor permitido en el setter pero no hay método de servicio que lo aplique. Si se expone la API, conviene añadir `servicios.cancelar(id_inc)` y la route `/incidencias/<int:id_inc>/cancelar`.
- La route `/incidencias/<int:id_inc>/resolver/<resolucion>` debe rechazar con `409` si el estado actual no es `Pendiente`.

### 7.2. Relevo de turno y avisos

- La opción 4 del menú combina dos operaciones: generar documento **y** notificar al técnico entrante si la incidencia está pendiente.
- En la API Flask conviene separar estas responsabilidades: `/incidencias/<int:id_inc>/documento` para el informe y `/incidencias/<int:id_inc>/relevo/<int:id_tecnico_entrante>` para la notificación.
- El buzón de avisos (`notificacion_pendiente`) es en memoria: los avisos se pierden al reiniciar. En la fase SQLite esto cambiará.

### 7.3. Responsabilidades mezcladas en `RepositorioMemoria`

Actualmente `RepositorioMemoria` gestiona incidencias **y** proporciona técnicos y salas via `cargar_tecnicos()` / `cargar_salas()`. Para la API Flask:
- Los técnicos y salas deben ser accesibles desde el servicio (métodos `listar_tecnicos`, `listar_salas`).
- El servicio necesita recibir un repositorio de técnicos/salas o que `ServiciosIncidencias.__init__` reciba también esas listas.

### 7.4. Mostrar datos de incidencias como texto

`RegistroIncidencia`, `Tecnico` y `SalaControl` no son cadenas de texto directamente.
Para mostrarlos en el route Flask, usa `str(incidencia)` (si el dominio tiene `__str__`)
o construye el texto accediendo a sus atributos:

```python
linea = (
    f"[{inc.id_inc}] {inc.estado} — "
    f"Sala: {inc.sala.nombre} — "
    f"Técnico: {inc.tecnico.nombre} — "
    f"Apertura: {str(inc._fecha_apertura)}"
)
```

> Nota: `_fecha_apertura` es un atributo protegido. Si el dominio no expone una propiedad pública equivalente, acceder con `inc._fecha_apertura` es aceptable en ut4e1.
