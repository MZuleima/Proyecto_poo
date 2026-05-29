import sqlite3
from datetime import datetime
from domain.repositorio import RepositorioIncidencias
from domain.excepciones import ErrorPersistencia, RegistroNoEncontrado
from domain.estructura import RegistroIncidencia, SalaControl
from domain.item import Tecnico

class RepositorioSQLite(RepositorioIncidencias):
    """
    Implementación real del repositorio con persistencia en SQLite.
    Mapea filas de tablas relacionales a objetos complejos del dominio.
    """
    def __init__(self, path_db="incidencias.db"):
        self.path_db = path_db

    def _conectar(self):
        """Método privado helper para asegurar la conexión con llaves foráneas."""
        con = sqlite3.connect(self.path_db)
        con.execute("PRAGMA foreign_keys = ON;")
        return con

    def guardar(self, inc):
        """Traduce e inserta u ofrece persistencia al objeto Incidencia."""
        try:
            with self._conectar() as con:
                # Comprobamos si ya existe para decidir si es INSERT o UPDATE (Cierre)
                cursor = con.execute("SELECT 1 FROM incidencias WHERE id = ?", (inc.id_inc,))
                existe = cursor.fetchone()

                # Parseo seguro de fechas a string 
                f_apertura = inc._fecha_apertura.strftime("%Y-%m-%d %H:%M:%S") if isinstance(inc._fecha_apertura, datetime) else str(inc._fecha_apertura)
                f_cierre = inc._fecha_cierre.strftime("%Y-%m-%d %H:%M:%S") if isinstance(inc._fecha_cierre, datetime) else None

                if not existe:
                    con.execute("""
                        INSERT INTO incidencias (id, tecnico_id, sala_id, descripcion, estado, resolucion, fecha_apertura, fecha_cierre)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """, (inc.id_inc, inc.tecnico.id_empleado, inc.sala.id_empleado if hasattr(inc.sala, 'id_empleado') else 1, 
                          inc.descripcion, inc.estado, inc.resolucion, f_apertura, f_cierre))
                else:
                    con.execute("""
                        UPDATE incidencias 
                        SET estado = ?, resolucion = ?, fecha_cierre = ? 
                        WHERE id = ?
                    """, (inc.estado, inc.resolucion, f_cierre, inc.id_inc))
        except sqlite3.Error as e:
            raise ErrorPersistencia(f"Fallo al sincronizar los datos en SQLite: {e}")

    def obtener_todas(self):
        """Consulta la BD mediante un JOIN y reconstruye la lista de objetos de dominio."""
        incidencias_objetos = []
        try:
            with self._conectar() as con:
            
                query = """
                    SELECT i.id, i.descripcion, i.estado, i.resolucion, i.fecha_apertura, i.fecha_cierre,
                           t.nombre, t.id, t.turno,
                           s.nombre, s.ubicacion
                    FROM incidencias i
                    JOIN tecnicos t ON i.tecnico_id = t.id
                    JOIN salas s ON i.sala_id = s.id
                """
                cursor = con.execute(query)
                for fila in cursor.fetchall():
                    # 1. Reconstruimos el Técnico y la Sala con sus datos de la BD
                    tecnico = Tecnico(fila[6], fila[7], fila[8])
                    sala = SalaControl(fila[9], fila[10])
                    
                    # 2. Instanciamos el objeto raíz del Dominio
                    inc = RegistroIncidencia(fila[0], tecnico, sala, fila[1])
                    inc._estado = fila[2]
                    inc._resolucion = fila[3]
                    
                    # 3. Parsear strings de fechas de vuelta a objetos datetime de Python
                    if fila[4]:
                        try: inc.fecha_apertura = datetime.strptime(fila[4], "%Y-%m-%d %H:%M:%S")
                        except ValueError: pass
                    if fila[5]:
                        try: inc.fecha_cierre = datetime.strptime(fila[5], "%Y-%m-%d %H:%M:%S")
                        except ValueError: pass
                        
                    incidencias_objetos.append(inc)
            return incidencias_objetos
        except sqlite3.Error as e:
            raise ErrorPersistencia(f"Error al reconstruir el listado de incidencias: {e}")

    def buscar_por_id(self, id_inc):
        """Busca una incidencia por ID reconstruyendo su objeto completo."""
        try:
            with self._conectar() as con:
                query = """
                    SELECT i.id, i.descripcion, i.estado, i.resolucion, i.fecha_apertura, i.fecha_cierre,
                           t.nombre, t.id, t.turno,
                           s.nombre, s.ubicacion
                    FROM incidencias i
                    JOIN tecnicos t ON i.tecnico_id = t.id
                    JOIN salas s ON i.sala_id = s.id
                    WHERE i.id = ?
                """
                cursor = con.execute(query, (id_inc,))
                fila = cursor.fetchone()
                if not fila:
                    raise RegistroNoEncontrado(f"No se encontró la incidencia técnica con ID {id_inc}")
                
                tecnico = Tecnico(fila[6], fila[7], fila[8])
                sala = SalaControl(fila[9], fila[10])
                
                inc = RegistroIncidencia(fila[0], tecnico, sala, fila[1])
                inc._estado = fila[2]
                inc._resolucion = fila[3]
                
                if fila[4]:
                    try: inc.fecha_apertura = datetime.strptime(fila[4], "%Y-%m-%d %H:%M:%S")
                    except ValueError: pass
                if fila[5]:
                    try: inc.fecha_cierre = datetime.strptime(fila[5], "%Y-%m-%d %H:%M:%S")
                    except ValueError: pass
                    
                return inc
        except sqlite3.Error as e:
            raise ErrorPersistencia(f"Error de lectura en consulta única: {e}")