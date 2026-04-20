from domain.estructura import RegistroIncidencia

class ServiciosIncidencias:
    def __init__(self, repositorio):
        """
        Aquí conectamos el servicio con el "almacén" (repositorio).
        Le pasamos el almacén para que sepa dónde guardar las cosas.
        """
        self.repo = repositorio

    def nueva_incidencia(self, id_inc, tecnico, sala, desc):
        "Crea una ficha de incidencia nueva y le dice al almacén que la guarde."
        incidencia = RegistroIncidencia(id_inc, tecnico, sala, desc)
        self.repo.guardar(incidencia)
        return incidencia

    def obtener_listado(self):
        "Pide las incidencias guardadas"
        return self.repo.obtener_todas()

    def resolver(self, incidencia, resolucion):
        "No se edita la incidencia, la incidencia se encarga de cambiar el estado y validarlo"
        incidencia.solventar(resolucion)

    def generar_documento(self, obj_incidencia, tecnico_entrante=None):
        "Si está lista, saca el PDF. Si no, avisa al siguiente técnico."
        if obj_incidencia.estado == "Solventada":
            return f"PDF FINAL: Incidencia {obj_incidencia.id_inc} resuelta en {obj_incidencia.sala.nombre}."
        
        if tecnico_entrante:
            msg = f"Pendiente: {obj_incidencia.descripcion}"
            tecnico_entrante.registrar_aviso(msg)
            
        return f"BORRADOR: Incidencia {obj_incidencia.id_inc} enviada a siguiente turno."