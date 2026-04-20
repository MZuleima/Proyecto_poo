# domain/repositorio.py

class RepositorioIncidencias:
    """ 
        Obliga a que el almacén sepa cómo guardar una incidencia nueva.
        Si alguien intenta usarlo sin programarlo, saltará un error (NotImplementedError).
    """
    def guardar(self, incidencia):
        raise NotImplementedError("El método guardar() debe ser implementado")

    def obtener_todas(self):
        raise NotImplementedError("El método obtener_todas() debe ser implementado")
    
    def buscar_por_id(self, id_inc):
        raise NotImplementedError("El método buscar_por_id() debe ser implementado")