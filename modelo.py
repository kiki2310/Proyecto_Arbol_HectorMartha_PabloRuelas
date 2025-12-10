import json

# definimos la clase Nodo, osea cada carpeta o archivo del sistema
class Nodo:
    def __init__(self, id_nodo, nombre, es_carpeta=True, contenido=None):
        self.id = id_nodo
        self.nombre = nombre
        #Si es True es carpeta, si no pues es archivo, no hay pierde
        self.es_carpeta = es_carpeta  
        #Aqui va lo q escribes adentro, nomas si es archivo
        self.contenido = contenido    
        # Esta lista es pa guardar a los hijos del nodo
        self.hijos = []               
        # Pa saber quien es el patron (el nodo padre)
        self.padre = None             

    # funcion es pa convertir el objeto a diccionario
    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "tipo": "carpeta" if self.es_carpeta else "archivo",
            "contenido": self.contenido,
            "hijos": [hijo.to_dict() for hijo in self.hijos]
        }

    #Esta es pa lo contrario, pa leer del json y armar el arbol de nuevo
    # Metodo de clase pa no ocupar instanciar a lo menso
    @classmethod
    def from_dict(cls, data):
        es_carpeta = (data["tipo"] == "carpeta")
        # Armamos el nodo con los datos que traemos del diccionario
        nodo = cls(data["id"], data["nombre"], es_carpeta, data.get("contenido"))
        
        # Si trae hijos, hay que armarlos tambien
        if "hijos" in data:
            for hijo_data in data["hijos"]:
                hijo_nodo = cls.from_dict(hijo_data)
                hijo_nodo.padre = nodo  # Le decimos quien es su padre
                nodo.hijos.append(hijo_nodo)
        
        return nodo