class RepositorioInicial:
    """Los datos de los 3 técnicos y las 3 salas."""
    @staticmethod
    def cargar_tecnicos():
        # Aquí definimos los 3 técnicos requeridos
        return [
            Tecnico("Juan Pérez", "T-01", "Mañana"),
            Tecnico("Ana López", "T-02", "Tarde"),
            Tecnico("Carlos Ruiz", "T-03", "Noche"),
        ]

    @staticmethod
    def cargar_salas():
        # Aquí definimos las 3 salas requeridas
        return [
            SalaControl("Crisis"),
            SalaControl("Operadores"),
            SalaControl("Datawall")
        ]