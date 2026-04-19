from datetime import datetime

class SalaControl:
    def __init__(self, nombre, ubicacion):
        self._nombre = nombre
        self._ubicacion = ubicacion

    @property
    def nombre(self):
        return self._nombre

    @property
    def ubicacion(self):
        return self._ubicacion


class RegistroIncidencia:
    def __init__(self, id_inc, tecnico, sala, descripcion):
        # Atributos protegidos (encapsulamiento)
        self._id_inc = id_inc
        self._tecnico = tecnico
        self._sala = sala
        self._descripcion = descripcion

        # Valores por defecto para una incidencia nueva
        self._estado = "Pendiente"
        self._resolucion = ""
        self._fecha_apertura = datetime.now()
        self._fecha_cierre = None

    # --- PROPIEDADES (Getters) ---
    # Solo lectura para elementos que no deben cambiar tras la creación
    @property
    def id_inc(self):
        return self._id_inc

    @property
    def tecnico(self):
        return self._tecnico

    @property
    def sala(self):
        return self._sala

    @property
    def descripcion(self):
        return self._descripcion

    @property
    def estado(self):
        return self._estado

    @property
    def resolucion(self):
        return self._resolucion

    @property
    def fecha_cierre(self):
        return self._fecha_cierre

    # --- SETTERS (Control de cambios) ---
    @estado.setter
    def estado(self, nuevo_estado):
        " Solo deja cambiar el estado si es uno de los permitidos. "
        estados_permitidos = ["Pendiente", "Solventada", "Cancelada"]
        if nuevo_estado not in estados_permitidos:
            raise ValueError(f"Estado inválido. Debe ser uno de: {estados_permitidos}")
        self._estado = nuevo_estado

    @resolucion.setter
    def resolucion(self, texto):
        " No deja guardar una solución si es demasiado corta o está vacía. "
        if not texto or len(texto.strip()) < 5:
            raise ValueError("La resolución es demasiado corta (mínimo 5 caracteres).")
        self._resolucion = texto

    # --- Acción principal ---
    def solventar(self, texto_resolucion):
        """
        Este es el botón de 'Arreglar'. Actualiza la solución, 
        cambia el estado y apunta la hora exacta en que se terminó.
        """
        self.resolucion = texto_resolucion  # Valida mediante el setter
        self.estado = "Solventada"         # Valida mediante el setter
        self._fecha_cierre = datetime.now()