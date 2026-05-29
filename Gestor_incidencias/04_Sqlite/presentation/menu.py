# --- CAPA DE PRESENTACIÓN: Menú de Consola ---
import sqlite3
from application.servicios import ServiciosIncidencias
from infrastructure.repositorio_sqlite import RepositorioSQLite
from domain.excepciones import ErrorPersistencia
from domain.item import Tecnico
from domain.estructura import SalaControl

def mostrar_opciones():
    """Muestra la interfaz del menú en la consola."""
    print("\n" + "="*40)
    print("      GESTOR DE INCIDENCIAS TÉCNICAS")
    print("="*40)
    print("1. Registrar nueva incidencia")
    print("2. Resolver incidencia (Cierre)")
    print("3. Ver avisos de técnicos (Relevo)")
    print("4. Generar informe técnico (PDF/Borrador)")
    print("0. Salir")
    return input("\nSeleccione una opción: ")

def cargar_maestros_desde_db(path_db):
    """Auxiliar para extraer las entidades maestras sincronizadas en las tablas de SQLite."""
    tecnicos = []
    salas = []
    try:
        with sqlite3.connect(path_db) as con:
            # Leer técnicos de la BD
            cursor = con.execute("SELECT nombre, id, turno FROM tecnicos")
            for fila in cursor.fetchall():
                tecnicos.append(Tecnico(fila[0], fila[1], fila[2]))
            
            # Leer salas de la BD
            cursor = con.execute("SELECT nombre, ubicacion, id FROM salas")
            for fila in cursor.fetchall():
                sala = SalaControl(fila[0], fila[1])
                sala.id_empleado = fila[2]  # Acoplamos el ID de la base de datos para la relación
                salas.append(sala)
    except sqlite3.Error as e:
        print(f" Alerta: No se pudieron precargar los catálogos maestros: {e}")
        # Valores de respaldo por seguridad si el script crear_bd.py no se ejecutó
        tecnicos = [Tecnico("Juan", 1, "Mañana"), Tecnico("Ana", 2, "Tarde")]
        salas = [SalaControl("Sala de Control", "Planta Baja")]
        salas[0].id_empleado = 1
    return tecnicos, salas

def ejecutar_sistema():
    """Inicia el sistema inyectando el motor de persistencia SQLite."""
    path_base_datos = "incidencias.db"
    
    # Inicialización de la infraestructura real
    repo = RepositorioSQLite(path_base_datos)
    servicios = ServiciosIncidencias(repo)
    
    # Carga dinámica desde la base de datos relacional
    tecnicos, salas = cargar_maestros_desde_db(path_base_datos)

    while True:
        opcion = mostrar_opciones()

        if opcion == "1":
            print("\n--- REGISTRO DE INCIDENCIA ---")
            try:
                id_inc = int(input("ID de la incidencia (numérico): "))
                
                for i, t in enumerate(tecnicos): 
                    print(f" [{i}] {t.nombre} - Turno: {t.turno}")
                idx_t = int(input("Seleccione índice del técnico: "))
                
                for i, s in enumerate(salas): 
                    print(f" [{i}] {s.nombre}")
                idx_s = int(input("Seleccione índice de la sala: "))
                
                desc = input("Descripción del problema: ")
                
                # Gestión segura mediante excepciones de dominio
                servicios.nueva_incidencia(id_inc, tecnicos[idx_t], salas[idx_s], desc)
                print("\n Incidencia registrada y guardada en SQLite con éxito.")
            except (ValueError, IndexError) as e:
                print(f"\n Error en la entrada de datos: {e}")
            except ErrorPersistencia as e:
                print(f"\n Error de almacenamiento: {e}")

        elif opcion == "2":
            try:
                incidencias = servicios.obtener_listado()
                if not incidencias:
                    print("\n No hay incidencias registradas en la base de datos.")
                    continue

                print("\n--- RESOLVER INCIDENCIA ---")
                for i, inc in enumerate(incidencias):
                    print(f" [{i}] ID: {inc.id_inc} | Estado: {inc.estado} | Sala: {inc.sala.nombre}")
            
                idx = int(input("Seleccione la incidencia a cerrar: "))
                resolucion = input("Indique la solución técnica: ")
                
                servicios.resolver(incidencias[idx], resolucion)
                print("Registro actualizado y cerrado en la base de datos.")
            except (ValueError, IndexError) as e:
                print(f"Selección inválida: {e}")
            except ErrorPersistencia as e:
                print(f"Error al procesar la actualización: {e}")

        elif opcion == "3":
            print("\n--- PANEL DE AVISOS ---")
            for i, t in enumerate(tecnicos): 
                print(f" [{i}] {t.nombre}")
            
            try:
                idx_t = int(input("Ver avisos del técnico: "))
                print(f"\nNOTIFICACIONES PARA {tecnicos[idx_t].nombre}:")
                print("-" * 30)
                print(tecnicos[idx_t].leer_aviso())
            except (ValueError, IndexError):
                print("Técnico no seleccionado correctamente.")

        elif opcion == "4":
            try:
                incidencias = servicios.obtener_listado()
                if not incidencias:
                    print("\n No hay documentos disponibles para generar.")
                    continue

                print("\n--- GENERAR DOCUMENTACIÓN ---")
                for i, inc in enumerate(incidencias):
                    print(f" [{i}] ID: {inc.id_inc} - {inc.estado}")
            
                idx = int(input("Seleccione índice de incidencia: "))
                inc = incidencias[idx]
                
                if inc.estado != "Solventada":
                    print("\nIncidencia pendiente. ¿A quién notificamos el relevo?")
                    for i, t in enumerate(tecnicos): print(f" [{i}] {t.nombre}")
                    idx_t = int(input("Seleccione técnico entrante: "))
                    print(f"\n{servicios.generar_documento(inc, tecnico_entrante=tecnicos[idx_t])}")
                else:
                    print(f"\n{servicios.generar_documento(inc)}")
            except (ValueError, IndexError):
                print("Selección de datos inválida.")
            except ErrorPersistencia as e:
                print(f"Error al consultar la documentación: {e}")

        elif opcion == "0":
            print("Cerrando la conexión del sistema...")
            break
        else:
            print("Opción no válida, intente de nuevo.")

if __name__ == "__main__":
    ejecutar_sistema()