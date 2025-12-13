import time
import random
from main import SistemaArchivos

def prueba_performance():
    print("\n--- PRUEBAS INTESNIVAS---")
    app = SistemaArchivos()
    
    #---carga masiva de archivos
    CANTIDAD = 5000 # crear 2000 archivos
    print(f"Intentando crear {CANTIDAD} archivos...")
    
    inicio = time.time()
    
    #crear carpeta base
    app.crear_nodo("purebaInte", True)
    app.cambiar_directorio("purebaInte")
    
    for i in range(CANTIDAD):
        nombre = f"archivo_{i}"
        app.crear_nodo(nombre, False, f"Contenido {i}")
        
    fin = time.time()
    tiempo_total = fin - inicio
    
    print(f"\nSe crearon {CANTIDAD} nodos.")
    print(f"Tiempo total: {tiempo_total:.4f} segundos.")
    print(f"Promedio: {CANTIDAD / tiempo_total:.2f} operaciones por segundo.")

    #--- probar el trie con muchos archivos
    print("\n--- BUSQUEDA (TRIE) ---")
    print("Buscando 'archivo_199'...")
    
    inicio_busqueda = time.time()
    app.buscar_archivo("archivo_199") 
    fin_busqueda = time.time()
    
    print(f"Tiempo de busqueda: {fin_busqueda - inicio_busqueda:.6f} segundos.")

def prueba_casos_limite():
    print("\n\n--- PRUEBA DE CASOS LIMITE ---")
    app = SistemaArchivos()
    
    #--- nombres duplicados
    print("1. Intentando crear duplicados...")
    app.crear_nodo("test_dup", True)
    app.crear_nodo("test_dup", False) 
    
    #--- navegacion imposible
    print("\n2. Intentando subir de la raiz...")
    app.cambiar_directorio("..")
    app.cambiar_directorio("..") 
    print(f"Ruta actual: {app.obtener_ruta_actual()}")
    
    #--- restaurar archivo fantasma
    print("\n3. Intentando restaurar archivo borrado en papelera...")
    app.restaurar_nodo("archivo_fantasma.txt")
    
    #--- eliminar y buscar
    print("\n4.Crear -> Borrar -> Buscar (No debe estar) -> Restaurar -> Buscar (Debe estar)")
    app.crear_nodo("prueba_borrar.txt", False)
    app.eliminar_nodo("prueba_borrar.txt")
    print("Busqueda tras borrar:")
    app.buscar_archivo("prue")
    app.restaurar_nodo("prueba_borrar.txt")
    print("Busqueda tras restaurar:")
    app.buscar_archivo("prue")

if __name__ == "__main__":
    prueba_performance()
    prueba_casos_limite()
 