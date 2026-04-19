# infrastructure/datos_iniciales.py
from domain.repositorio import RepositorioIncidencias
from domain.item import Tecnico
from domain.estructura import SalaControl

class RepositorioMemoria(RepositorioIncidencias):
    "Implementación real del repositorio usando una lista en memoria."
    def __init__(self):
        self._incidencias = []

    def guardar(self, incidencia):
        "Mete la ficha de la incidencia en la lista. "
        self._incidencias.append(incidencia)

    def obtener_todas(self):
        " Devuelve la lista completa de lo que tenemos guardado. "
        return self._incidencias

    def buscar_por_id(self, id_inc):
        """ 
        Busca entre todas las fichas hasta encontrar una que coincida con el ID.
        Si no la encuentra, devuelve None (nada).
        """
        return next((i for i in self._incidencias if i.id_inc == id_inc), None)

    @staticmethod
    def cargar_tecnicos():
        # Plantilla de tecnicos
        return [Tecnico("Juan", 1, "Mañana"), Tecnico("Ana", 2, "Tarde"), Tecnico("Pedro", 3, "Noche")]

    @staticmethod
    def cargar_salas():
        # Se definen las salas
        return [SalaControl("Sala de Emergencias", "Planta 1"), SalaControl("Sala de Comunicaciones", "Planta 0"), SalaControl("Sala de Control", "Planta baja")]