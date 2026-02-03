from datetime import datetime
class sala_de_control:
    def __init__(self, nombre_salas):
        SALAS_VALIDAS = [sala_crisis, sala_operadores, sala_datawall]
        if nombre_salas not in SALAS_VALIDAS:
            raise ValueError(f"La sala {nombre_salas}, no permitida")
        self.nombre_salas = nombre_salas

class registro_incidencia:
    def __init__(self, id_incidencia, tecnico, sala, descripcion):
        self.id_incidencia = id_incidencia
        self.tecnico = tecnico
        self.sala = sala
        self.descripcion = descripcion
        self.fecha = datetime.now()
        self.estado = "pendiente" #En esta sección debe estar pendiente o solventada
        self.resolucion = ""
