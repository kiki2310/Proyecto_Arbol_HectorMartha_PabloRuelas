#Sistema de Archivos en Consola (UAS)
#Martha Lopez Hector Ulises
#Ruelas Lopez Juan Pablo
---------------------------------------------------------------------------------------------------------------------
Implementación de un sistema de archivos jerárquico simulado en consola utilizando Árboles binarios y Tries para busqueda eficiente
---------------------------------------------------------------------------------------------------------------------
#Descripcion

Este proyecto simula un sistema de archivos que permite crear carpetas y archivos, navegar entre directorios, renombrar, eliminar, recuperar elementos, etc.

---------------------------------------------------------------------------------------------------------------------
#Caracteristicas principales:

Estructura de Datos: Uso de Arbol General para la jerarquia de carpetas

Busqueda Rapida: Implementacion de un Trie para autocompletado y busqueda por prefijo

Persistencia: Guardado y cargado automatico del estado del arbol en formato JSON

Papelera de Reciclaje: Funcionalidad de borrado "temporal" con opcion de restaurar o vaciar

Reportes: Exportacion de la estructura del arbol en recorrido Preorden

---------------------------------------------------------------------------------------------------------------------
#Instalacion y Ejecucion

#Pasos
1. Clonar el repositorio:
https://github.com/kiki2310/Proyecto_Arbol_HectorMartha_PabloRuelas.git
2. Ejecutar el programa
python main.py
3. Correr las pruebas y las pruebas avanzadas (bullying), esto es opcional
En el mismo repositorio contiene estos dos archivos con opciones de testing para desarrollo

---------------------------------------------------------------------------------------------------------------------
#Manual de uso

Opcion 	  Comando			Descripcion
1	mkdir [nombre]		Crea una nueva carpeta en el directorio actual
2	touch [nombre]		Crea un nuevo archivo en el directorio actual
3	ls			Lista los contenidos (hijos) del directorio actual
4	cd [nombre]		Entra a una subcarpeta específica
5	cd ..			Sube un nivel hacia el directorio padre
6	mv [viejo] [nuevo]	Renombra un archivo o carpeta
7	rm [nombre]		Envia un elemento a la papelera de reciclaje
8	bin (Ver Papelera)	Muestra los elementos eliminados temporalmente
9	restore [nombre]	Restaura un elemento de la papelera al directorio actual
10	empty (Vaciar)		Elimina permanentemente todo lo que hay en la papelera
11	search [prefijo]	Busca archivos/carpetas en todo el sistema usando el Trie
12	export			Genera un archivo reporte_preorden.txt con la estructura del arbol
13	save			Guarda los cambios en sistema_archivos.json y sale

---------------------------------------------------------------------------------------------------------------------

#Detalles tecnicos (los de hueva profe)

-Persistencia (JSON)
El estado del árbol se guarda en sistema_archivos.json. 
Al iniciar, el programa reconstruye:
1.-La jerarquia de nodos (Arbol)

2.-Las referencias al nodo padre (para permitir cd ..)

3.-El indice de búsqueda (Trie) sincronizado

-Estructura del Trie
Cada vez que se crea, renombra o restaura un nodo, este se inserta en un Trie (Arbol de Prefijos) que permite realizar busquedas con una complejidad de tiempo dependiente de la longitud de la palabra, no de la cantidad total de archivos, optimizando el rendimiento en sistemas grandes.

---------------------------------------------------------------------------------------------------------------------

