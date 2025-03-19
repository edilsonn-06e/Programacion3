import os
import csv
from graphviz import Digraph

class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.izquierda = None
        self.derecha = None

class ArbolBinarioBusqueda:
    def __init__(self):
        self.raiz = None

    def insertar(self, valor):
        self.raiz = self._insertar_recursivo(self.raiz, valor)

    def _insertar_recursivo(self, nodo, valor):
        if nodo is None:
            return Nodo(valor)
        if valor < nodo.valor:
            nodo.izquierda = self._insertar_recursivo(nodo.izquierda, valor)
        elif valor > nodo.valor:
            nodo.derecha = self._insertar_recursivo(nodo.derecha, valor)
        return nodo

    def buscar(self, valor):
        return self._buscar_recursivo(self.raiz, valor)

    def _buscar_recursivo(self, nodo, valor):
        if nodo is None:
            return False
        if nodo.valor == valor:
            return True
        if valor < nodo.valor:
            return self._buscar_recursivo(nodo.izquierda, valor)
        return self._buscar_recursivo(nodo.derecha, valor)

    def eliminar(self, valor):
        self.raiz = self._eliminar_recursivo(self.raiz, valor)

    def _eliminar_recursivo(self, nodo, valor):
        if nodo is None:
            return None
        if valor < nodo.valor:
            nodo.izquierda = self._eliminar_recursivo(nodo.izquierda, valor)
        elif valor > nodo.valor:
            nodo.derecha = self._eliminar_recursivo(nodo.derecha, valor)
        else:
            if nodo.izquierda is None:
                return nodo.derecha
            if nodo.derecha is None:
                return nodo.izquierda
            temp = self._encontrar_minimo(nodo.derecha)
            nodo.valor = temp.valor
            nodo.derecha = self._eliminar_recursivo(nodo.derecha, temp.valor)
        return nodo

    def _encontrar_minimo(self, nodo):
        while nodo.izquierda is not None:
            nodo = nodo.izquierda
        return nodo

    def cargar_desde_csv(self, ruta_archivo):
        try:
            with open(ruta_archivo, mode='r') as archivo:
                lector_csv = csv.reader(archivo)
                for fila in lector_csv:
                    for numero in fila:
                        self.insertar(int(numero))
                print("ARCHIVO CARGADO CORRECTAMENTE!")
        except FileNotFoundError:
            print(f"El archivo '{ruta_archivo}' no fue encontrado.")
        except ValueError:
            print("El archivo contiene datos no válidos. Asegúrate de que sean números.")

    def generar_graphviz(self, nombre_archivo='arbol'):
        dot = Digraph(comment='Árbol Binario de Búsqueda')
        self._generar_graphviz_recursivo(self.raiz, dot)
        archivo_generado = dot.render(nombre_archivo, format='png', cleanup=True)
        print(f"El archivo Graphviz ha sido generado como '{archivo_generado}'.")


        try:
            if os.name == 'nt':
                os.startfile(archivo_generado)
            elif os.name == 'posix':
                os.system(f'open "{archivo_generado}"') if os.uname().sysname == 'Darwin' else os.system(
                    f'xdg-open "{archivo_generado}"')
        except Exception as e:
            print(f"No se pudo abrir el archivo automáticamente: {e}")

    def _generar_graphviz_recursivo(self, nodo, dot):
        if nodo:
            dot.node(str(nodo.valor), str(nodo.valor))
            if nodo.izquierda:
                dot.edge(str(nodo.valor), str(nodo.izquierda.valor))
                self._generar_graphviz_recursivo(nodo.izquierda, dot)
            if nodo.derecha:
                dot.edge(str(nodo.valor), str(nodo.derecha.valor))
                self._generar_graphviz_recursivo(nodo.derecha, dot)


def menu_interactivo():
    arbol = ArbolBinarioBusqueda()

    while True:
        print("\n=== Menú ===")
        print("1. Insertar número")
        print("2. Buscar número")
        print("3. Eliminar número")
        print("4. Cargar desde archivo CSV")
        print("5. Generar representación Graphviz")
        print("6. Salir")

        opcion = input("Selecciona una opción: ")

        if opcion == '1':
            numero = int(input("Introduce un número: "))
            arbol.insertar(numero)
            print(f"¡Número {numero} insertado!")

        elif opcion == '2':
            numero = int(input("Introduce un número a buscar: "))
            encontrado = arbol.buscar(numero)
            print(f"¿Número encontrado?: {'Sí' if encontrado else 'No'}")

        elif opcion == '3':
            numero = int(input("Introduce un número a eliminar: "))
            arbol.eliminar(numero)
            print(f"¡Número {numero} eliminado!")

        elif opcion == '4':
            ruta = input("Introduce la ruta del archivo CSV: ")
            arbol.cargar_desde_csv(ruta)

        elif opcion == '5':
            arbol.generar_graphviz()

        elif opcion == '6':
            print("Saliendo del programa.")
            break

        else:
            print("Opción no válida. Intenta de nuevo.")

if __name__ == "__main__":
    menu_interactivo()

