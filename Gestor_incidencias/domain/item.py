#En este archivo se aplica la herencia.
from datetime import datetime

class Trabajador:
    #Clase Padre.
    def __init__(self, nombre, id_empleado):
        #self.nombre -> Almacena el nombre del trabajadr
        self.nombre = nombre
        #self.id_empleado -> Almacena el ID que identifica al trabajador
        self.id_empleado = id_empleado
    
    def perfil(self):
        #Devuelve la cadena con la información
        return f"Empleado: {self.nombre} -> ID: {self.id_empleado}"

class Tecnico(Trabajador):
    #Clase heredada
    def __init__(self, nombre, id_empleado, turno):
        #Llama a la clase padre, para no repetir código
        super().__init__(nombre, id_empleado)
        #Define el turno en que trabaja cada trabajador
        self.turno = turno
        #Buzon de entrada -> almacena los mensajes 
        self.notificacion_pendiente = []
    
    def registro_aviso(self, mensaje):
        #Añadir un aviso con la fecha y hora actual
        fecha = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
        #Añadir a la lista el mensaje con el tiempo.
        self.notificacion_pendiente.append(f"{fecha} -> {mensaje}")

    def leer_aviso(self):
        #Devuelve los avisos acumulados al relevo de turno
        #Si la lista esta vácia, se muestra que no hay tareas pendientes
        if not self.notificacion_pendiente:
            return "No hay avisos pendientes"
        #Si hay mensajes, los une en un texto separados por saltos de línea
        return "/n".join(self.notificacion_pendiente)

        