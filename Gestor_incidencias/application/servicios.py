from domain.estructura import RegistroIncidencia

class ServiciosIncidencias:
    def __init__(self):
        self.listado_incidencias = []

    def nueva_incidencia(self, id_inc, tecnico, sala, desc):
        incidencia = RegistroIncidencia(id_inc, tecnico, sala, desc)
        self.listado_incidencias.append(incidencia)
        return incidencia

    def resolver(self, incidencia, resolucion):
        incidencia.resolucion = resolucion
        incidencia.estado = "Solventada"

    def generar_documento(self, obj_incidencia, tecnico_entrante=None):
        if obj_incidencia.estado == "Solventada":
            return f"PDF FINAL: Incidencia {obj_incidencia.id_inc} resuelta en {obj_incidencia.sala.nombre}."
        else:
            if tecnico_entrante:
                msg = f"Pendiente: {obj_incidencia.descripcion}"
                tecnico_entrante.registrar_aviso(msg)
            return f"BORRADOR: Incidencia {obj_incidencia.id_inc} enviada a siguiente turno."