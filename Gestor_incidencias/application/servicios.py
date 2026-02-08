from domain.maquina import RegistroIncidencia

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

    def generar_documento(self, incidencia, tecnico_entrante=None):
        if incidencia.estado == "Solventada":
            return f"PDF FINAL: Incidencia {incidencia.id_inc} resuelta en {incidencia.sala.nombre}."
        else:
            if tecnico_entrante:
                msg = f"Pendiente: {incidencia.descripcion}"
                tecnico_entrante.registrar_aviso(msg)
            return f"BORRADOR: Incidencia {incidencia.id_inc} enviada a siguiente turno."