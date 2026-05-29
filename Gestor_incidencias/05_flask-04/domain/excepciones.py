class ErrorPersistencia(Exception):
    "Excepción base para errores en el almacenamiento."
    pass

class RegistroNoEncontrado(ErrorPersistencia):
    "Se lanza cuando buscamos un ID que no existe en la BD."
    pass