from modelo import Nodo
import os

# Aqui controlamos todo el show del sistema de archivos
class SistemaArchivos:
    def __init__(self):
        # Creamos la raiz, el mero jefe de jefes (id 0)
        self.raiz = Nodo(0, "root", True)
        # Este puntero nos dice donde andamos parados ahorita
        self.nodo_actual = self.raiz
        # La basura pa cuando borremos algo (requisito del profe)
        self.papelera = []  
        # Contador pa que los IDs no se repitan y choquen
        self.contador_ids = 1 

    # Funcion pa crear carpetas o archivos sin broncas
    def crear_nodo(self, nombre, es_carpeta, contenido=None):
        # Primero checamos que no exista uno igual, pa no hacer cochinero
        for hijo in self.nodo_actual.hijos:
            if hijo.nombre == nombre:
                print(f"Aguanta viejo, ya existe '{nombre}' aqui. Ponle otro nombre.")
                return

        # Si todo bien, armamos el nodo nuevo
        nuevo_nodo = Nodo(self.contador_ids, nombre, es_carpeta, contenido)
        nuevo_nodo.padre = self.nodo_actual # Lo amarramos al padre
        self.nodo_actual.hijos.append(nuevo_nodo) # Lo metemos a la lista de hijos
        
        # Incrementamos el ID pa el que sigue
        self.contador_ids += 1
        
        tipo = "Carpeta" if es_carpeta else "Archivo"
        print(f"Fierro pariente, se creo la {tipo} '{nombre}' al cien.")

    # Pa wachar que hay adentro de la carpeta actual (el ls)
    def listar_directorio(self):
        print(f"\n--- Wachando lo que hay en: /{self.nodo_actual.nombre} ---")
        if not self.nodo_actual.hijos:
            print("  (Esta vacio el canton, no hay nada)")
        else:
            for hijo in self.nodo_actual.hijos:
                # Le pongo D si es Directorio o F si es File, pa ubicar
                tipo = "[DIR]" if hijo.es_carpeta else "[FILE]"
                print(f"  {tipo} {hijo.nombre}")

    # El menu pa que el usuario sepa que rollo
    def mostrar_menu(self):
        print("\n=== SISTEMA DE ARCHIVOS MAMALON (UAS) ===")
        print(f"Andas en la ruta: .../{self.nodo_actual.nombre}")
        print("1. Armar carpeta (mkdir)")
        print("2. Armar archivo (touch)")
        print("3. Wachar hijos (ls)")
        print("4. Fugarse (Salir)")

    # Aqui corre la magia
    def ejecutar(self):
        while True:
            self.mostrar_menu()
            opcion = input("Que vas a hacer plebe? >> ")

            if opcion == "1":
                nombre = input("Echale el nombre a la carpeta: ")
                # Validamos que no este vacio el nombre pa no tronar
                if nombre: 
                    self.crear_nodo(nombre, True)
                else:
                    print("Nombre invalido oiga, escriba bien.")
            
            elif opcion == "2":
                nombre = input("Nombre del archivo viejon: ")
                contenido = input("Que va a llevar adentro?: ")
                if nombre: 
                    self.crear_nodo(nombre, False, contenido)
            
            elif opcion == "3":
                self.listar_directorio()
            
            elif opcion == "4":
                print("Fierro, ahi nos vidrios...")
                break
            
            else:
                print("Esa opcion no existe compa, pongase trucha.")

# Esto es pa que corra si lo ejecutas directo
if __name__ == "__main__":
    app = SistemaArchivos()
    app.ejecutar()