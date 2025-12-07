import unittest
from main import SistemaArchivos

class TestArbol(unittest.TestCase):
    
    def setUp(self):
        """Esto se corre antes de cada prueba, pa tener el changarro limpio"""
        self.app = SistemaArchivos()

    def test_crear_carpeta(self):
        """Probamos si crea carpetas chido"""
        print("\nProbando crear carpeta...")
        self.app.crear_nodo("Tarea_UAS", True)
        # Verificamos que la lista de hijos tenga 1 elemento
        self.assertEqual(len(self.app.nodo_actual.hijos), 1)
        # Verificamos que se llame igual
        self.assertEqual(self.app.nodo_actual.hijos[0].nombre, "Tarea_UAS")

    def test_eliminar_nodo(self):
        """Probamos si borra y manda a la papelera"""
        print("\nProbando eliminar...")
        self.app.crear_nodo("Basura", False)
        self.app.eliminar_nodo("Basura")
        # Ya no debe estar en hijos
        self.assertEqual(len(self.app.nodo_actual.hijos), 0)
        # Debe estar en la papelera
        self.assertEqual(len(self.app.papelera), 1)

    def test_renombrar(self):
        """Probamos el cambio de nombre"""
        print("\nProbando renombrar...")
        self.app.crear_nodo("Feo", True)
        self.app.renombrar_nodo("Feo", "Bonito")
        self.assertEqual(self.app.nodo_actual.hijos[0].nombre, "Bonito")

    def test_ruta_completa(self):
        """Probamos que la ruta se armen bien los strings"""
        print("\nProbando rutas...")
        # Creo carpeta y me meto
        self.app.crear_nodo("Carpeta1", True)
        self.app.cambiar_directorio("Carpeta1")
        ruta = self.app.obtener_ruta_actual()
        self.assertEqual(ruta, "/root/Carpeta1")

if __name__ == '__main__':
    unittest.main()