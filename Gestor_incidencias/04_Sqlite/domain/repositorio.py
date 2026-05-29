# --- CAPA DE DOMINIO: Interfaz del Repositorio ---
from domain.excepciones import RegistroNoEncontrado

class RepositorioIncidencias:
    """
    Define qué operaciones son obligatorias, abstrayendo cómo se guardan 
    (ya sea en Memoria, SQLite, etc.).
    """
    
    def guardar(self, incidencia):
        """
        Guarda una nueva incidencia o actualiza una existente.
        """
        raise NotImplementedError("El método guardar() debe ser implementado")

    def obtener_todas(self):
        """
        Recupera el listado completo de incidencias.
        """
        raise NotImplementedError("El método obtener_todas() debe ser implementado")
    
    def buscar_por_id(self, id_inc):
        """
        Busca una incidencia específica por su identificador único.
        """
        raise NotImplementedError("El método buscar_por_id() debe ser implementado")