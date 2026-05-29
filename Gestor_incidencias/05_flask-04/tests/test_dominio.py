import unittest
from domain.estructura import RegistroIncidencia, SalaControl
from domain.item import Tecnico

class TestDominio(unittest.TestCase):

    def setUp(self):
        """Configuración inicial para cada test."""
        self.sala = SalaControl("Sala 1", "Planta Baja")
        self.tecnico = Tecnico("Marcos", 101, "Mañana")
        self.incidencia = RegistroIncidencia(1, self.tecnico, self.sala, "Fallo de red")

    # --- TESTS PARA REGISTROINCIDENCIA ---
    
    def test_creacion_incidencia(self):
        """Verifica que la incidencia se cree con los datos correctos y estado Pendiente."""
        self.assertEqual(self.incidencia.id_inc, 1)
        self.assertEqual(self.incidencia.estado, "Pendiente")
        self.assertIsNone(self.incidencia.fecha_cierre)

    def test_setter_resolucion_valida(self):
        """Verifica que se puede añadir una resolución válida (>= 5 caracteres)."""
        self.incidencia.solventar("Se cambió el cableado del switch")
        self.assertEqual(self.incidencia.estado, "Solventada")
        self.assertIsNotNone(self.incidencia.fecha_cierre)

    def test_setter_resolucion_invalida(self):
        """Verifica que salte un ValueError si la resolución es muy corta."""
        with self.assertRaises(ValueError):
            self.incidencia.solventar("ok") # Menos de 5 caracteres

    # --- TESTS PARA TECNICO (HERENCIA Y AVISOS) ---

    def test_herencia_trabajador(self):
        """Verifica que el técnico hereda correctamente el nombre del Trabajador."""
        self.assertEqual(self.tecnico.nombre, "Marcos")
        self.assertEqual(self.tecnico.turno, "Mañana")

    def test_sistema_avisos_tecnico(self):
        """Verifica el funcionamiento del buzón de avisos."""
        self.tecnico.registrar_aviso("Revisar aire acondicionado")
        avisos = self.tecnico.leer_aviso()
        self.assertIn("Revisar aire acondicionado", avisos)

if __name__ == '__main__':
    unittest.main()