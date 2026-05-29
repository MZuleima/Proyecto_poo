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

    def to_dict(self):
        """Devuelve el diccionario serializable de la infraestructura"""
        return {
            "nombre": self.nombre,
            "ubicacion": self.ubicacion
        }


class RegistroIncidencia:
    def __init__(self, id_inc, tecnico, sala, descripcion):
        self._id_inc = id_inc
        self._tecnico = tecnico
        self._sala = sala
        self._descripcion = descripcion

        self._estado = "Borrador"  # Forzado a "Borrador" para sincronía con las fases web
        self._resolucion = ""
        self._fecha_apertura = datetime.now()
        self._fecha_cierre = None

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

    @estado.setter
    def estado(self, nuevo_estado):
        estados_permitidos = ["Borrador", "Solventada", "Cancelada"]
        if nuevo_estado not in estados_permitidos:
            raise ValueError(f"Estado inválido. Debe ser uno de: {estados_permitidos}")
        self._estado = nuevo_estado

    @resolucion.setter
    def resolucion(self, texto):
        if not texto or len(texto.strip()) < 5:
            raise ValueError("La resolución es demasiado corta (mínimo 5 caracteres).")
        self._resolucion = texto

    def solventar(self, texto_resolucion):
        self.resolucion = texto_resolucion
        self.estado = "Solventada"
        self._fecha_cierre = datetime.now()

    def to_dict(self):
        """Devuelve el diccionario estructurado completo para la API REST"""
        return {
            "id_inc": self.id_inc,
            "estado": self.estado,
            "descripcion": self.descripcion,
            "resolucion": self.resolucion if self.resolucion else None,
            "fecha_apertura": self._fecha_apertura.strftime("%Y-%m-%d %H:%M:%S") if isinstance(self._fecha_apertura, datetime) else str(self._fecha_apertura),
            "fecha_cierre": self._fecha_cierre.strftime("%Y-%m-%d %H:%M:%S") if self._fecha_cierre else None,
            "tecnico": self.tecnico.to_dict() if hasattr(self.tecnico, "to_dict") else str(self.tecnico),
            "sala": self.sala.to_dict() if hasattr(self.sala, "to_dict") else str(self.sala)
        }