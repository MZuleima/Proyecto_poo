from datetime import datetime

class Trabajador:
    # Clase Padre.
    def __init__(self, nombre, id_empleado):
        self.nombre = nombre
        self.id_empleado = id_empleado
    
    def perfil(self):
        return f"Empleado: {self.nombre} -> ID: {self.id_empleado}"

class Tecnico(Trabajador):
    # Clase heredada
    def __init__(self, nombre, id_empleado, turno):
        super().__init__(nombre, id_empleado)
        self.turno = turno
        self.notificacion_pendiente = []
    
    def registrar_aviso(self, mensaje):
        fecha = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
        self.notificacion_pendiente.append(f"{fecha} -> {mensaje}")

    def leer_aviso(self):
        if not self.notificacion_pendiente:
            return "No hay avisos pendientes"
        return "\n".join(self.notificacion_pendiente)

    def to_dict(self):
        """Devuelve el diccionario serializable de la entidad"""
        return {
            "id_empleado": self.id_empleado,
            "nombre": self.nombre,
            "turno": self.turno,
            "avisos_pendientes": self.notificacion_pendiente
        }