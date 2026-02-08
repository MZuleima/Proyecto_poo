# domain/maquina.py
from datetime import datetime

class SalaControl:
    """
    ENTIDAD INDEPENDIENTE: Representa los espacios físicos del proyecto.
    Define las ubicaciones donde pueden ocurrir las incidencias.
    """
    def __init__(self, nombre_sala):
        # Validamos que la sala sea una de las tres permitidas por el sistema
        # (Sala de Crisis, Sala de Operadores, Sala del Datawall)
        salas_validas = ["Crisis", "Operadores", "Datawall"]
        if nombre_sala not in salas_validas:
            raise ValueError(f"Error: La sala '{nombre_sala}' no está autorizada.")
        
        self.nombre = nombre_sala
        self.activa = True

class RegistroIncidencia:
    """
    ENTIDAD PRINCIPAL: Gestiona el ciclo de vida de una incidencia.
    Vincula a un técnico con una sala y controla el estado para decidir el tipo de reporte.
    """
    def __init__(self, id_inc, tecnico, sala, descripcion):
        # Identificador único de la incidencia
        self.id_inc = id_inc
        # Objeto de la clase Tecnico (proviene de item.py)
        self.tecnico = tecnico  
        # Objeto de la clase SalaControl
        self.sala = sala        
        # Descripción detallada del problema encontrado
        self.descripcion = descripcion
        # Marca de tiempo de apertura automática
        self.fecha_apertura = datetime.now()
        # Estado inicial: Pendiente (genera borrador Word) o Solventada (genera PDF)
        self.estado = "Pendiente"  
        # Texto con la solución aplicada (vacío al inicio)
        self.resolucion = ""
        # Fecha de cierre (se asigna al solventar)
        self.fecha_cierre = None

    def solventar(self, detalle_solucion):
        """
        Cambia el estado de la incidencia a 'Solventada'. 
        Este cambio gatilla la generación del PDF corporativo en la capa de aplicación.
        """
        self.resolucion = detalle_solucion
        self.estado = "Solventada"
        self.fecha_cierre = datetime.now()

    def es_critica(self):
        """
        Ejemplo de lógica de negocio:
        Determina que cualquier incidencia en la Sala de Crisis es prioritaria.
        """
        return self.sala.nombre == "Crisis"

    def obtener_resumen(self):
        """Devuelve un resumen rápido del estado actual de la incidencia."""
        return f"Incidencia #{self.id_inc} en {self.sala.nombre} - Estado: {self.estado}"