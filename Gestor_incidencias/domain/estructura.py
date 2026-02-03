class sala_de_control:
    def __init__(self, nombre_salas):
        SALAS_VALIDAS = [sala_crisis, sala_operadores, sala_datawall]
        if nombre_salas not in SALAS_VALIDAS:
            print(f"La sala no esta es valida")
        self.nombre_salas = nombre_salas
        self
