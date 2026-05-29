# Modelo de Dominio

### Entidades Principales:
- **RegistroIncidencia**: La entidad central que agrupa la sala, el técnico y el estado del problema.
- **Tecnico**: Hereda de `Trabajador`. Posee un turno y un buzón de notificaciones.
- **SalaControl**: Representa el lugar físico donde ocurre el evento.

### Relaciones:
- Una **Incidencia** pertenece a una **Sala**.
- Una **Incidencia** es asignada a un **Tecnico**.
- Un **Tecnico** puede recibir múltiples avisos de relevo.
