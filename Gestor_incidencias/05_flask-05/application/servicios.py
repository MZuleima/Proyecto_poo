# --- CAPA DE APLICACIÓN: Servicios de Orquestación ---
import sqlite3
from datetime import datetime
from domain.estructura import RegistroIncidencia, SalaControl
from domain.item import Tecnico
from domain.excepciones import RegistroNoEncontrado, ErrorPersistencia

class ServiciosIncidencias:
    """
    Coordinador de casos de uso. Orquesta la comunicación entre la capa
    de presentación (Consola/Flask) y la persistencia en SQLite.
    """
    def __init__(self, repositorio):
        """
        Inicializa el servicio inyectando su dependencia de almacenamiento.
        """
        self.repo = repositorio

    def nueva_incidencia(self, id_inc, id_tecnico, id_sala, desc):
        """
        Caso de Uso: Registra una nueva incidencia utilizando identificadores numéricos.
        Busca las entidades maestras correspondientes antes de instanciar el objeto.
        """
        if not desc or desc.strip() == "":
            raise ValueError("Descripción vacía")

        # Comprobamos si el ID de incidencia ya existe para lanzar el error de conflicto
        try:
            self.repo.buscar_por_id(id_inc)
            raise ValueError("Ya existe una incidencia con ese ID")
        except RegistroNoEncontrado:
            pass  # Es lo esperado, podemos continuar

        # Buscamos el técnico y la sala reales en la persistencia
        tecnico = self.obtener_tecnico(id_tecnico)
        sala = self.obtener_sala(id_sala)

        # Creamos la entidad e indicamos al repositorio que la guarde
        incidencia = RegistroIncidencia(id_inc, tecnico, sala, desc)
        self.repo.guardar(incidencia)
        return incidencia

    def obtener_listado(self):
        """Caso de Uso: Devuelve la lista completa de incidencias."""
        return self.repo.obtener_todas()

    def resolver(self, incidencia, resolucion):
            """
            Caso de Uso: Transiciona el estado de una incidencia a Solventada.
            """
            if incidencia.estado == "Solventada": 
                raise ValueError("La incidencia ya ha sido cerrada.")
            if incidencia.estado != "Borrador":
                raise ValueError(f"No se puede resolver una incidencia en estado {incidencia.estado}")
                
            incidencia.solventar(resolucion)
            self.repo.guardar(incidencia)

    def generar_documento(self, obj_incidencia, tecnico_entrante=None):
        """Caso de Uso: Generación de actas de cierre o derivación de borradores."""
        if obj_incidencia.estado == "Solventada":
            return f"PDF FINAL: Incidencia {obj_incidencia.id_inc} resuelta en {obj_incidencia.sala.nombre}."
        
        if tecnico_entrante:
            msg = f"Pendiente: {obj_incidencia.descripcion}"
            tecnico_entrante.registrar_aviso(msg)
            
        return f"BORRADOR: Incidencia {obj_incidencia.id_inc} enviada a siguiente turno."

    def buscar_incidencia(self, id_inc: int):
        """Busca una incidencia por su ID. Traduce el RegistroNoEncontrado a ValueError."""
        try:
            return self.repo.buscar_por_id(id_inc)
        except RegistroNoEncontrado:
            raise ValueError("No existe técnico/sala/incidencia con ese ID")

    def listar_tecnicos(self):
        """Retorna la lista de técnicos disponibles directamente desde la base de datos."""
        tecnicos = []
        try:
            with sqlite3.connect(self.repo.path_db) as con:
                cursor = con.execute("SELECT nombre, id, turno FROM tecnicos")
                for fila in cursor.fetchall():
                    tecnicos.append(Tecnico(fila[0], fila[1], fila[2]))
            return tecnicos
        except sqlite3.Error as e:
            raise ErrorPersistencia(f"Error al listar técnicos: {e}")

    def obtener_tecnico(self, id_tecnico: int):
        """Localiza un técnico específico por su id_empleado."""
        try:
            with sqlite3.connect(self.repo.path_db) as con:
                cursor = con.execute("SELECT nombre, id, turno FROM tecnicos WHERE id = ?", (id_tecnico,))
                fila = cursor.fetchone()
                if not fila:
                    raise ValueError("No existe técnico/sala/incidencia con ese ID")
                return Tecnico(fila[0], fila[1], fila[2])
        except sqlite3.Error as e:
            raise ErrorPersistencia(f"Error al obtener técnico: {e}")

    def listar_salas(self):
        """Retorna la lista de salas disponibles desde la base de datos."""
        salas = []
        try:
            with sqlite3.connect(self.repo.path_db) as con:
                cursor = con.execute("SELECT nombre, ubicacion, id FROM salas")
                for fila in cursor.fetchall():
                    sala = SalaControl(fila[0], fila[1])
                    sala.id_empleado = fila[2]
                    salas.append(sala)
            return salas
        except sqlite3.Error as e:
            raise ErrorPersistencia(f"Error al listar salas: {e}")

    def obtener_sala(self, id_sala: int):
        """Localiza una sala específica por su identificador."""
        try:
            with sqlite3.connect(self.repo.path_db) as con:
                cursor = con.execute("SELECT nombre, ubicacion, id FROM salas WHERE id = ?", (id_sala,))
                fila = cursor.fetchone()
                if not fila:
                    raise ValueError("No existe técnico/sala/incidencia con ese ID")
                sala = SalaControl(fila[0], fila[1])
                sala.id_empleado = fila[2]
                return sala
        except sqlite3.Error as e:
            raise ErrorPersistencia(f"Error al obtener sala: {e}")

    def listar_avisos_tecnico(self, id_tecnico: int):
        """Localiza al técnico y extrae el buzón de notificaciones de su entidad."""
        tecnico = self.obtener_tecnico(id_tecnico)
        # Nota: Los avisos se gestionan actualmente en la RAM del objeto Técnico
        return tecnico.leer_aviso()