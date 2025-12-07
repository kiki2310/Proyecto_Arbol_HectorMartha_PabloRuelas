from modelo import Nodo
import os
import json

class NodoTrie:
    def __init__(self):
        self.hijos = {}
        self.es_fin_palabra = False
        self.nodo_arbol = None #referencia al nodo real del sistema

class Trie:
    def __init__(self):
        self.raiz = NodoTrie()

    def insertar(self, palabra, nodo):
        temp = self.raiz
        for char in palabra:
            if char not in temp.hijos:
                temp.hijos[char] = NodoTrie()
            temp = temp.hijos[char]
        temp.es_fin_palabra = True
        temp.nodo_arbol = nodo

    def buscar_autocompletado(self, prefijo):
        temp = self.raiz
        #navegar hasta el final del prefijo
        for char in prefijo:
            if char not in temp.hijos:
                return [] #fo hay nada con ese inicio
            temp = temp.hijos[char]
        
        #recolectar todas las palabras que cuelgan de ahi
        resultados = []
        self._recolectar(temp, prefijo, resultados)
        return resultados

    def _recolectar(self, nodo_trie, palabra_actual, lista):
        if nodo_trie.es_fin_palabra:
            tipo = "carpeta" if nodo_trie.nodo_arbol.es_carpeta else "archivo"
            lista.append(f"{tipo} {palabra_actual}")
        
        for char, hijo in nodo_trie.hijos.items():
            self._recolectar(hijo, palabra_actual + char, lista)

    def eliminar(self, palabra):
        #funcion recursiva para borrar y limpiar nodos huerfanos
        def _borrar(nodo, palabra, profundidad):
            if profundidad == len(palabra):
                if not nodo.es_fin_palabra:
                    return False #la palabra no existia
                nodo.es_fin_palabra = False
                nodo.nodo_arbol = None
                return len(nodo.hijos) == 0 #si no tiene hijos, se puede borrar
            
            char = palabra[profundidad]
            if char not in nodo.hijos:
                return False
            
            debe_borrar_hijo = _borrar(nodo.hijos[char], palabra, profundidad + 1)
            
            if debe_borrar_hijo:
                del nodo.hijos[char]
                return len(nodo.hijos) == 0 and not nodo.es_fin_palabra
            
            return False

        _borrar(self.raiz, palabra, 0)



class SistemaArchivos:
    def __init__(self):
        self.raiz = Nodo(0, "root", True)
        self.nodo_actual = self.raiz
        self.papelera = []  # Aqui van los muertitos (papelera temporal) 
        self.contador_ids = 1 
        self.trie = Trie()
        self.cargar_datos()
        
    # --- FUNCIONES AUXILIARES (Pa no repetir codigo) ---
    def buscar_hijo(self, nombre):
        """Busca un plebe por nombre en la carpeta actual."""
        for hijo in self.nodo_actual.hijos:
            if hijo.nombre == nombre:
                return hijo
        return None

    def obtener_ruta_actual(self):
        """Te dice la ruta completa desde la raiz tipo /root/carpeta/archivo"""
        ruta = []
        nodo = self.nodo_actual
        while nodo is not None:
            ruta.insert(0, nodo.nombre) # Insertamos al inicio pa que quede en orden
            nodo = nodo.padre
        return "/" + "/".join(ruta)

    # --- OPERACIONES DEL ARBOL (Lo que pide el PDF) ---
    def crear_nodo(self, nombre, es_carpeta, contenido=None):
        if self.buscar_hijo(nombre):
            print(f"Epaaaa, ya existe '{nombre}' aquí. No se aceptan clones.")
            return

        nuevo_nodo = Nodo(self.contador_ids, nombre, es_carpeta, contenido)
        nuevo_nodo.padre = self.nodo_actual 
        self.nodo_actual.hijos.append(nuevo_nodo) 
        self.contador_ids += 1
        print(f"Listo el pollo, se creó '{nombre}'.")
        self.trie.insertar(nombre, nuevo_nodo)

    def eliminar_nodo(self, nombre):
        """Manda el nodo a la papelera (soft delete)."""
        nodo = self.buscar_hijo(nombre)
        if nodo:
            self.nodo_actual.hijos.remove(nodo) # Lo sacamos de la lista de hijos
            self.papelera.append(nodo)          # Lo guardamos en la papelera por si las moscas
            self.trie.eliminar(nombre)
            print(f" Fierro, '{nombre}' se fue a la basura.")
        else:
            print(" No lo hallé, oiga. Escriba bien el nombre.")

    def renombrar_nodo(self, nombre_viejo, nombre_nuevo):
        nodo = self.buscar_hijo(nombre_viejo)
        if nodo:
            # Validamos que el nombre nuevo no exista ya
            if self.buscar_hijo(nombre_nuevo):
                print(f" Nel, ya hay algo que se llama '{nombre_nuevo}'.")
                return
            self.trie.eliminar(nombre_viejo) #sacar el viejo
            nodo.nombre = nombre_nuevo
            self.trie.insertar(nombre_nuevo, nodo) #meter el nuevo
            print(f" Simona la mona, ahora se llama '{nombre_nuevo}'.")
        else:
            print(" Ese nodo no existe, pariente.")

    def cambiar_directorio(self, nombre):
        """El famoso 'cd' pa moverse entre carpetas."""
        if nombre == "..":
            if self.nodo_actual.padre:
                self.nodo_actual = self.nodo_actual.padre
            else:
                print(" Ya estas en la raiz, no puedes subir mas.")
            return

        nodo = self.buscar_hijo(nombre)
        if nodo and nodo.es_carpeta:
            self.nodo_actual = nodo
        elif nodo and not nodo.es_carpeta:
            print(" Ese es un archivo, no te puedes meter ahi.")
        else:
            print(" No existe esa carpeta.")

    def guardar_datos(self):
        try:
            datos = self.raiz.to_dict()
            with open("sistema_archivos.json", "w") as archivo:
                json.dump(datos, archivo, indent=4)
            print("Datos guardados correctamente en sistema_archivos.json")
        except Exception as e:
            print(f"Error al guardar: {e}")

    def cargar_datos(self):
        if not os.path.exists("sistema_archivos.json"):
            print("No se encontro archivo de datos previo.")
            return

        try:
            with open("sistema_archivos.json", "r") as archivo:
                datos = json.load(archivo)
                self.raiz = Nodo.from_dict(datos)
                self.nodo_actual = self.raiz
                #reconstruir los padres porque el JSON no guarda referencias circulares, solo la jerarquia hacia abajo
                self._reconstruir_padres(self.raiz)
                
                #llenar el trie de nuevo
                if hasattr(self, 'trie'):
                    self.trie = Trie() # Reiniciar trie
                    self._reconstruir_trie_recursivo(self.raiz)
                    
                #recuperar las referencias al padre
                self._reconstruir_padres(self.raiz)

                #recuperar el contador de IDs
                self.contador_ids = self._obtener_max_id(self.raiz) + 1
                
                #reconstruir el trie
                self.trie = Trie() # Limpiar trie viejo
                self._reconstruir_trie_recursivo(self.raiz)
                
            print("Datos cargados correctamente.")
        except Exception as e:
            print(f"Error al cargar: {e}")

    #funcion auxiliar para reconstruir el trie
    def _reconstruir_trie_recursivo(self, nodo):
        if nodo.nombre != "root": # No metemos al root al buscador
            self.trie.insertar(nodo.nombre, nodo)
        for hijo in nodo.hijos:
            self._reconstruir_trie_recursivo(hijo)

    #funcion auxiliar para reconstruir los padres
    def _reconstruir_padres(self, nodo_actual):
        for hijo in nodo_actual.hijos:
            hijo.padre = nodo_actual
            self._reconstruir_padres(hijo)

    # Funcion auxiliar para que los IDs no se repitan despues de cargar
    def _obtener_max_id(self, nodo):
        # Busca cual es el ID mas grande que ya existe
        max_id = nodo.id
        for hijo in nodo.hijos:
            max_id = max(max_id, self._obtener_max_id(hijo))
        return max_id

    def buscar_archivo(self, prefijo):
        print(f"Buscando archivos que inicien con '{prefijo}'...")
        resultados = self.trie.buscar_autocompletado(prefijo)
        if resultados:
            print("Coincidencias encontradas:")
            for r in resultados:
                print(f"  -> {r}")
        else:
            print("No se encontro nada con ese inicio, pariente.")

    # --- INTERFAZ DE CONSOLA ---
    def mostrar_menu(self):
        ruta = self.obtener_ruta_actual() # Requisito: mostrar ruta completa 
        print(f"\n Ruta: {ruta}")
        print("1. Crear Carpeta (mkdir)")
        print("2. Crear Archivo (touch)")
        print("3. Listar (ls)")
        print("4. Entrar a carpeta (cd nombre)")
        print("5. Subir de nivel (cd ..)")
        print("6. Renombrar (mv nombre nuevo_nombre)")
        print("7. Eliminar (rm nombre)")
        print("8. Salir(sin guardar)")
        print("9. Buscar (prefijo)")
        print("10. Guardar")


    def ejecutar(self):
        print("=== SISTEMA DE ARCHIVOS UAS v1.0 ===")
        while True:
            self.mostrar_menu()
            entrada = input(">> ").split()
            
            if not entrada: continue
            cmd = entrada[0]

            if cmd == "1" and len(entrada) > 1: self.crear_nodo(entrada[1], True)
            elif cmd == "2" and len(entrada) > 1: self.crear_nodo(entrada[1], False, "Vacio")
            elif cmd == "3": self.listar_hijos()
            elif cmd == "4" and len(entrada) > 1: self.cambiar_directorio(entrada[1])
            elif cmd == "5": self.cambiar_directorio("..")
            elif cmd == "6" and len(entrada) > 2: self.renombrar_nodo(entrada[1], entrada[2])
            elif cmd == "7" and len(entrada) > 1: self.eliminar_nodo(entrada[1])
            elif cmd == "8": break
            elif cmd == "9" and len(entrada) > 1: self.buscar_archivo(entrada[1])
            elif cmd == "10": 
                self.guardar_datos()
            else: print(" Comando no reconocido o faltan datos.")

    def listar_hijos(self):
        if not self.nodo_actual.hijos:
            print("  (Vacio como mi cartera)")
        for h in self.nodo_actual.hijos:
            tipo = "carpeta" if h.es_carpeta else "archivo"
            print(f"  {tipo} {h.nombre}")






if __name__ == "__main__":
    app = SistemaArchivos()
    app.ejecutar()