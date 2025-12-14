import time
import os
import sys
from main import SistemaArchivos

#colores para la consola
GREEN = '\033[92m'
CYAN = '\033[96m'
YELLOW = '\033[93m'
RESET = '\033[0m'
BOLD = '\033[1m'

def imprimir_titulo(texto):
    print(f"\n{BOLD}{CYAN}=== {texto} ==={RESET}")
    time.sleep(1)

def paso(descripcion):
    print(f"\n{YELLOW}>> Accion: {descripcion}{RESET}")
    time.sleep(0.5)

def ejecutar_demo():
    print(f"{BOLD}{GREEN}INICIANDO DEMO AUTOMATICA{RESET}")
    print("Ejecutando todas las funciones del sistema paso a paso\n")
    
    #limpieza inicial para empezar de cero
    if os.path.exists("demo_data.json"):
        os.remove("demo_data.json")
        print("Se elimino el archivo JSON previo para iniciar limpio")
    
    app = SistemaArchivos("demo_data.json")
    time.sleep(1)

    #creacion y navegacion
    imprimir_titulo("ARBOL Y NAVEGACION")
    
    paso("Creando carpeta 'Semestre_1'")
    app.crear_nodo("Semestre_1", True)
    
    paso("Entrando a 'Semestre_1' (cd)")
    app.cambiar_directorio("Semestre_1")
    
    paso("Creando archivos y subcarpetas dentro")
    app.crear_nodo("Materias", True)
    app.crear_nodo("horario.pdf", False, "Lunes a Viernes")
    app.crear_nodo("lista_proyectos.txt", False, "Proyecto 1, 2 y 3")
    
    paso("Listando contenido actual (ls)")
    app.listar_hijos()

    #busqueda inteligente
    imprimir_titulo("BUSQUEDA CON TRIE")
    
    paso("Buscando prefijo 'hor' (Debe encontrar 'horario.pdf')")
    app.buscar_archivo("hor")
    
    paso("Buscando prefijo 'Mat' (Debe encontrar carpeta 'Materias')")
    app.buscar_archivo("Mat")

    #papelera de reciclaje
    imprimir_titulo("PAPELERA Y RESTAURACION")
    
    paso("Eliminando 'lista_proyectos.txt' (rm)")
    app.eliminar_nodo("lista_proyectos.txt")
    
    paso("Verificando que ya no aparece en busqueda (Trie actualizado)")
    app.buscar_archivo("lista")
    
    paso("Revisando la Papelera")
    app.ver_papelera()
    
    paso("Restaurando 'lista_proyectos.txt'")
    app.restaurar_nodo("lista_proyectos.txt")
    
    paso("Confirmando que regreso al Trie")
    app.buscar_archivo("lista")

    #reportes
    imprimir_titulo("EXPORTACION")
    
    paso("Generando reporte en Preorden")
    app.exportar_preorden()
    print(f"{GREEN}Archivo 'reporte_preorden.txt' generado.{RESET}")

    #persistencia
    imprimir_titulo("PERSISTENCIA (JSON)")
    
    paso("Guardando cambios en sistema_archivos.json")
    app.guardar_datos()
    
    print(f"\n{BOLD}{GREEN}DEMO FINALIZADA{RESET}")
print("Puedes revisar los archivos: 'demo_data.json' y 'reporte_preorden.txt'")

if __name__ == "__main__":
    ejecutar_demo()