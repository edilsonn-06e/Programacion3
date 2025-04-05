import csv
import os
import subprocess
from graphviz import Digraph

class Nodo:
    def __init__(self, clave):  # Constructor corregido
        self.clave = clave
        self.izq = None
        self.der = None
        self.altura = 1

# ---------------- ABB ---------------- #
class ABB:
    def insertar(self, raiz, clave):
        if not raiz:
            return Nodo(clave)
        if clave < raiz.clave:
            raiz.izq = self.insertar(raiz.izq, clave)
        else:
            raiz.der = self.insertar(raiz.der, clave)
        return raiz

    def buscar(self, raiz, clave):
        if not raiz or raiz.clave == clave:
            return raiz
        if clave < raiz.clave:
            return self.buscar(raiz.izq, clave)
        return self.buscar(raiz.der, clave)

    def eliminar(self, raiz, clave):
        if not raiz:
            return raiz
        if clave < raiz.clave:
            raiz.izq = self.eliminar(raiz.izq, clave)
        elif clave > raiz.clave:
            raiz.der = self.eliminar(raiz.der, clave)
        else:
            if not raiz.izq:
                return raiz.der
            elif not raiz.der:
                return raiz.izq
            temp = self.obtener_min(raiz.der)
            raiz.clave = temp.clave
            raiz.der = self.eliminar(raiz.der, temp.clave)
        return raiz

    def obtener_min(self, nodo):
        actual = nodo
        while actual.izq:
            actual = actual.izq
        return actual

# ---------------- AVL ---------------- #
class AVL(ABB): #para que fuera más sencillo, heredamos algunas funciones del arbol abb que teniamos en la tarea3
    def altura(self, nodo):
        return nodo.altura if nodo else 0

    def actualizar_altura(self, nodo):
        nodo.altura = 1 + max(self.altura(nodo.izq), self.altura(nodo.der))

    def balance(self, nodo):
        return self.altura(nodo.izq) - self.altura(nodo.der)

    def rotar_der(self, y):
        x = y.izq
        T2 = x.der
        x.der = y
        y.izq = T2
        self.actualizar_altura(y)
        self.actualizar_altura(x)
        return x

    def rotar_izq(self, x):
        y = x.der
        T2 = y.izq
        y.izq = x
        x.der = T2
        self.actualizar_altura(x)
        self.actualizar_altura(y)
        return y

    def insertar(self, nodo, clave):
        if not nodo:
            return Nodo(clave)

        if clave < nodo.clave:
            nodo.izq = self.insertar(nodo.izq, clave)
        elif clave > nodo.clave:
            nodo.der = self.insertar(nodo.der, clave)
        else:
            return nodo  # Duplicados no permitidos

        self.actualizar_altura(nodo)
        balance = self.balance(nodo)

        # Casos de desbalance
        if balance > 1 and clave < nodo.izq.clave:
            return self.rotar_der(nodo)
        if balance < -1 and clave > nodo.der.clave:
            return self.rotar_izq(nodo)
        if balance > 1 and clave > nodo.izq.clave:
            nodo.izq = self.rotar_izq(nodo.izq)
            return self.rotar_der(nodo)
        if balance < -1 and clave < nodo.der.clave:
            nodo.der = self.rotar_der(nodo.der)
            return self.rotar_izq(nodo)

        return nodo

    def eliminar(self, nodo, clave):
        nodo = super().eliminar(nodo, clave)
        if not nodo:
            return nodo
        self.actualizar_altura(nodo)
        balance = self.balance(nodo)

        if balance > 1:
            if self.balance(nodo.izq) >= 0:
                return self.rotar_der(nodo)
            else:
                nodo.izq = self.rotar_izq(nodo.izq)
                return self.rotar_der(nodo)
        if balance < -1:
            if self.balance(nodo.der) <= 0:
                return self.rotar_izq(nodo)
            else:
                nodo.der = self.rotar_der(nodo.der)
                return self.rotar_izq(nodo)
        return nodo

# ---------------- Graphviz y CSV (acá ocurre la magia xd) ---------------- #
def cargar_desde_csv(ruta):
    try:
        with open(ruta, newline='') as archivo:
            reader = csv.reader(archivo)
            datos = []
            for fila in reader:
                datos.extend([int(x) for x in fila if x.strip().isdigit()])
            return datos
    except Exception as e:
        print(f"Error leyendo el archivo: {e}")
        return []

def generar_y_mostrar_graphviz(raiz, nombre='arbol'):
    dot = Digraph()
    agregar_nodos(dot, raiz)
    archivo_png = f"{nombre}.png"
    dot.render(filename=nombre, format='png', cleanup=True)
    print(f"Árbol generado en '{archivo_png}'")
    abrir_imagen(archivo_png)

def agregar_nodos(dot, nodo):
    if nodo:
        dot.node(str(nodo.clave))
        if nodo.izq:
            dot.edge(str(nodo.clave), str(nodo.izq.clave))
            agregar_nodos(dot, nodo.izq)
        if nodo.der:
            dot.edge(str(nodo.clave), str(nodo.der.clave))
            agregar_nodos(dot, nodo.der)

def abrir_imagen(ruta):
    try:
        if os.name == 'nt':
            os.startfile(ruta)
        elif os.name == 'posix':
            subprocess.call(['xdg-open', ruta])
    except Exception as e:
        print(f"No se pudo abrir la imagen: {e}")

# ---------------- NUESTRO MENU INGE ---------------- #
def menu_interactivo():
    arbol = AVL()
    raiz = None

    while True:
        print("\n=== MENU ===")
        print("1. INSERTAR UN NUMERO")
        print("2. BUSCAR UN NUMERO")
        print("3. ELIMINAR UN NUMERO")
        print("4. CARGAR LISTA DE NUMERO DESDE ARCHIVO .CSV")
        print("5. GENERAR GRAFICO")
        print("6. SALIR")

        opcion = input("Selecciona una opción: ")

        if opcion == '1':
            try:
                numero = int(input("Introduce un número: "))
                raiz = arbol.insertar(raiz, numero)
                print("¡Número insertado!")
            except:
                print("Entrada inválida.")
        elif opcion == '2':
            try:
                numero = int(input("Número a buscar: "))
                encontrado = arbol.buscar(raiz, numero)
                print("Número encontrado." if encontrado else "No encontrado.")
            except:
                print("Entrada inválida.")
        elif opcion == '3':
            try:
                numero = int(input("Número a eliminar: "))
                raiz = arbol.eliminar(raiz, numero)
                print("¡Número eliminado!")
            except:
                print("Entrada inválida.")
        elif opcion == '4':
            ruta = input("Ruta del archivo CSV: ")
            datos = cargar_desde_csv(ruta)
            for numero in datos:
                raiz = arbol.insertar(raiz, numero)
            print(f"{len(datos)} números insertados desde CSV.")
        elif opcion == '5':
            generar_y_mostrar_graphviz(raiz)
        elif opcion == '6':
            print("Saliendo del programa. ¡Hasta luego!")
            break
        else:
            print("Opción no válida. Intenta de nuevo.")

if __name__ == "__main__":
    menu_interactivo()
