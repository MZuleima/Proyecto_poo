# presentation/menu.py
from application.servicios import ServiciosIncidencias
from infrastructure.datos_iniciales import RepositorioMemoria

def mostrar_opciones():
    print("\n" + "="*40)
    print("      GESTOR DE INCIDENCIAS TÉCNICAS")
    print("="*40)
    print("1. Registrar nueva incidencia")
    print("2. Resolver incidencia (Cierre)")
    print("3. Ver avisos de técnicos (Relevo)")
    print("4. Generar informe técnico (PDF/Borrador)")
    print("0. Salir")
    return input("\nSeleccione una opción: ")

def ejecutar_sistema():
    # Inicialización de capas
    repo = RepositorioMemoria()
    servicios = ServiciosIncidencias(repo)
    
    # Pedimos a la infraestructura que nos dé la lista de trabajadores y salas iniciales
    tecnicos = RepositorioMemoria.cargar_tecnicos()
    salas = RepositorioMemoria.cargar_salas()

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
                
                servicios.nueva_incidencia(id_inc, tecnicos[idx_t], salas[idx_s], desc)
                print("\n✔ Incidencia registrada correctamente.")
            except (ValueError, IndexError) as e:
                print(f"\n Error en los datos: {e}")

        elif opcion == "2":
            incidencias = servicios.obtener_listado()
            if not incidencias:
                print(f"\n No hay incidencias registradas.")
                continue

            print("\n--- RESOLVER INCIDENCIA ---")
            for i, inc in enumerate(incidencias):
                print(f" [{i}] ID: {inc.id_inc} | Estado: {inc.estado} | Sala: {inc.sala.nombre}")
            
            try:
                idx = int(input("Seleccione la incidencia a cerrar: "))
                resolucion = input("Indique la solución técnica: ")
                servicios.resolver(incidencias[idx], resolucion)
                print("✔ Incidencia cerrada con éxito.")
            except (ValueError, IndexError) as e:
                print(f" Error al resolver: {e}")

        elif opcion == "3":
            print("\n--- PANEL DE AVISOS ---")
            for i, t in enumerate(tecnicos): 
                print(f" [{i}] {t.nombre}")
            
            try:
                idx_t = int(input("Ver avisos del técnico: "))
                print(f"\nNOTIFICACIONES PARA {tecnicos[idx_t].nombre}:")
                print("-" * 30)
                # Aquí usamos el método leer_aviso() que corregimos con \n
                print(tecnicos[idx_t].leer_aviso())
            except (ValueError, IndexError):
                print("Técnico no seleccionado correctamente.")

        elif opcion == "4":
            incidencias = servicios.obtener_listado()
            if not incidencias:
                print("\nNo hay documentos para generar.")
                continue

            print(f"\n--- GENERAR DOCUMENTACIÓN ---")
            for i, inc in enumerate(incidencias):
                print(f" [{i}] ID: {inc.id_inc} - {inc.estado}")
            
            try:
                idx = int(input("Seleccione índice de incidencia: "))
                inc = incidencias[idx]
                
                if inc.estado != "Solventada":
                    print(f"\nIncidencia pendiente. ¿A quién notificamos el relevo?")
                    for i, t in enumerate(tecnicos): print(f" [{i}] {t.nombre}")
                    idx_t = int(input("Seleccione técnico entrante: "))
                    print(f"\n{servicios.generar_documento(inc, tecnico_entrante=tecnicos[idx_t])}")
                else:
                    print(f"\n{servicios.generar_documento(inc)}")
            except (ValueError, IndexError):
                print("Selección inválida.")

        elif opcion == "0":
            print("Cerrando el sistema...")
            break
        else:
            print("Opción no válida, intente de nuevo.")

if __name__ == "__main__":
    ejecutar_sistema()