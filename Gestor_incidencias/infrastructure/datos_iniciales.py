class RepositorioInicial:
    """Datos de los 3 técnicos y las 3 salas."""
    @staticmethod
    def cargar_tecnicos():
        return [
            Tecnico("Juan Pérez", "T-01", "Mañana"),
            Tecnico("Ana López", "T-02", "Tarde"),
            Tecnico("Carlos Ruiz", "T-03", "Noche"),
        ]

    @staticmethod
    def cargar_salas():
        return [SalaControl(s) for s in ["Crisis", "Operadores", "Datawall"]]
