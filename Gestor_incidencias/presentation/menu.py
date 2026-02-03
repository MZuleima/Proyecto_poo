
def nuevo_menu():
    print("\n ---Gestor de incidencias")
    print("1.Mostrar Incidencias")
    print("2.Nueva Incidencia")
    print("3.Incidencias pendientes")
    print("4.Cancelar")
    print("5.Salir")

def opcion_mostrar(servicio):
    pass

def opcion_nueva():
    pass

def opcion_pendientes():
    pass

def opcion_cancelar():
    pass

def main():
    while True:
        nuevo_menu()
        opcion = input("Elige una opción: ").strip()
        try:
            if opcion == "1":
                opcion_mostrar(servicio)
            elif opcion == "2":
                opcion_nueva(servicio)
            elif opcion == "3":
                opcion_pendientes(servicio)
            elif opcion == "4":
                opcion_cancelar(servicio)
            elif opcion == "5":
                print("Fin del programa")
                break
            else:
                print("Opción no valida.")
        except ValueError as e:
            print("Error" +  str(e))

if __name__ == "__main__":
    main()