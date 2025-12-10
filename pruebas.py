import unittest
from main import SistemaArchivos

class TestArbol(unittest.TestCase):
    
    def setUp(self):
        self.app = SistemaArchivos()

    def test_crear_carpeta(self):
        print("\nProbando crear carpeta...")
        self.app.crear_nodo("Tarea_UAS", True)
        # Verificamos que la lista de hijos tenga 1 elemento
        self.assertEqual(len(self.app.nodo_actual.hijos), 1)
        # Verificamos que se llame igual
        self.assertEqual(self.app.nodo_actual.hijos[0].nombre, "Tarea_UAS")

    def test_eliminar_nodo(self):
        print("\nProbando eliminar...")
        self.app.crear_nodo("Basura", False)
        self.app.eliminar_nodo("Basura")
        # Ya no debe estar en hijos
        self.assertEqual(len(self.app.nodo_actual.hijos), 0)
        # Debe estar en la papelera
        self.assertEqual(len(self.app.papelera), 1)

    def test_renombrar(self):
        print("\nProbando renombrar...")
        self.app.crear_nodo("Feo", True)
        self.app.renombrar_nodo("Feo", "Bonito")
        self.assertEqual(self.app.nodo_actual.hijos[0].nombre, "Bonito")

    def test_ruta_completa(self):
        print("\nProbando rutas...")
        # Creo carpeta y me meto
        self.app.crear_nodo("Carpeta1", True)
        self.app.cambiar_directorio("Carpeta1")
        ruta = self.app.obtener_ruta_actual()
        self.assertEqual(ruta, "/root/Carpeta1")

if __name__ == '__main__':
    unittest.main()