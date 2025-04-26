import csv
import os
import subprocess
import math
from graphviz import Digraph

# ---------------- NODO B ---------------- #
class NodoB:
    def __init__(self, t, hoja=True):
        self.t = t
        self.claves = []
        self.hijos = []
        self.hoja = hoja

# ---------------- ARBOL B ---------------- #
class ArbolB:
    def __init__(self, t):
        self.t = t
        self.max_claves = t - 1
        self.min_claves = math.ceil((t + 1) / 2) - 1
        self.raiz = NodoB(t)

    def buscar(self, k, nodo=None):
        if nodo is None:
            nodo = self.raiz
        i = 0
        while i < len(nodo.claves) and k > nodo.claves[i]:
            i += 1
        if i < len(nodo.claves) and nodo.claves[i] == k:
            return True
        if nodo.hoja:
            return False
        return self.buscar(k, nodo.hijos[i])

    def insertar(self, k):
        r = self.raiz
        if len(r.claves) == self.max_claves:
            nueva_raiz = NodoB(self.t, hoja=False)
            nueva_raiz.hijos.append(self.raiz)
            self.dividir_hijo(nueva_raiz, 0)
            self._insertar_no_lleno(nueva_raiz, k)
            self.raiz = nueva_raiz
        else:
            self._insertar_no_lleno(r, k)

    def _insertar_no_lleno(self, nodo, k):
        i = len(nodo.claves) - 1
        if nodo.hoja:
            nodo.claves.append(None)
            while i >= 0 and k < nodo.claves[i]:
                nodo.claves[i + 1] = nodo.claves[i]
                i -= 1
            nodo.claves[i + 1] = k
        else:
            while i >= 0 and k < nodo.claves[i]:
                i -= 1
            i += 1
            if len(nodo.hijos[i].claves) == self.max_claves:
                self.dividir_hijo(nodo, i)
                if k > nodo.claves[i]:
                    i += 1
            self._insertar_no_lleno(nodo.hijos[i], k)

    def dividir_hijo(self, padre, i):
        t = self.t
        hijo = padre.hijos[i]
        nuevo = NodoB(t, hoja=hijo.hoja)

        mid = self.min_claves
        clave_medio = hijo.claves[mid]

        padre.claves.insert(i, clave_medio)
        padre.hijos.insert(i + 1, nuevo)

        nuevo.claves = hijo.claves[mid + 1:]
        hijo.claves = hijo.claves[:mid]

        if not hijo.hoja:
            nuevo.hijos = hijo.hijos[mid + 1:]
            hijo.hijos = hijo.hijos[:mid + 1]

    # ----------------- Eliminación ----------------- #
    def eliminar(self, k):
        self._eliminar(self.raiz, k)
        if len(self.raiz.claves) == 0 and not self.raiz.hoja:
            self.raiz = self.raiz.hijos[0]

    def _eliminar(self, nodo, k):
        i = 0
        while i < len(nodo.claves) and k > nodo.claves[i]:
            i += 1

        if i < len(nodo.claves) and nodo.claves[i] == k:
            if nodo.hoja:
                nodo.claves.pop(i)
            else:
                self._eliminar_en_interno(nodo, i)
        else:
            if nodo.hoja:
                print("La clave no existe en el árbol.")
                return
            if len(nodo.hijos[i].claves) < self.min_claves:
                self._llenar(nodo, i)
            if i > len(nodo.claves):
                self._eliminar(nodo.hijos[i - 1], k)
            else:
                self._eliminar(nodo.hijos[i], k)

    def _eliminar_en_interno(self, nodo, i):
        k = nodo.claves[i]
        if len(nodo.hijos[i].claves) >= self.min_claves:
            pred = self._obtener_predecesor(nodo.hijos[i])
            nodo.claves[i] = pred
            self._eliminar(nodo.hijos[i], pred)
        elif len(nodo.hijos[i + 1].claves) >= self.min_claves:
            succ = self._obtener_sucesor(nodo.hijos[i + 1])
            nodo.claves[i] = succ
            self._eliminar(nodo.hijos[i + 1], succ)
        else:
            self._unir(nodo, i)
            self._eliminar(nodo.hijos[i], k)

    def _obtener_predecesor(self, nodo):
        actual = nodo
        while not actual.hoja:
            actual = actual.hijos[-1]
        return actual.claves[-1]

    def _obtener_sucesor(self, nodo):
        actual = nodo
        while not actual.hoja:
            actual = actual.hijos[0]
        return actual.claves[0]

    def _llenar(self, nodo, i):
        if i != 0 and len(nodo.hijos[i - 1].claves) >= self.min_claves:
            self._pedir_prestado_izquierda(nodo, i)
        elif i != len(nodo.hijos) - 1 and len(nodo.hijos[i + 1].claves) >= self.min_claves:
            self._pedir_prestado_derecha(nodo, i)
        else:
            if i != len(nodo.hijos) - 1:
                self._unir(nodo, i)
            else:
                self._unir(nodo, i - 1)

    def _pedir_prestado_izquierda(self, nodo, i):
        hijo = nodo.hijos[i]
        hermano = nodo.hijos[i - 1]
        hijo.claves.insert(0, nodo.claves[i - 1])
        if not hijo.hoja:
            hijo.hijos.insert(0, hermano.hijos.pop())
        nodo.claves[i - 1] = hermano.claves.pop()

    def _pedir_prestado_derecha(self, nodo, i):
        hijo = nodo.hijos[i]
        hermano = nodo.hijos[i + 1]
        hijo.claves.append(nodo.claves[i])
        if not hijo.hoja:
            hijo.hijos.append(hermano.hijos.pop(0))
        nodo.claves[i] = hermano.claves.pop(0)

    def _unir(self, nodo, i):
        hijo = nodo.hijos[i]
        hermano = nodo.hijos[i + 1]
        hijo.claves.append(nodo.claves.pop(i))
        hijo.claves.extend(hermano.claves)
        if not hijo.hoja:
            hijo.hijos.extend(hermano.hijos)
        nodo.hijos.pop(i + 1)

# ---------------- CSV ---------------- #
def cargar_desde_csv(ruta):
    try:
        with open(ruta, newline='') as archivo:
            reader = csv.reader(archivo)
            return [int(x) for fila in reader for x in fila if x.strip().isdigit()]
    except Exception as e:
        print(f"Error leyendo el archivo: {e}")
        return []

# ---------------- GRAPHVIZ ---------------- #
def generar_y_mostrar_graphviz(arbol, nombre='arbol_b'):
    dot = Digraph()
    agregar_nodos(dot, arbol.raiz)
    archivo_png = f"{nombre}.png"
    dot.render(filename=nombre, format='png', cleanup=True)
    print(f"Árbol generado en '{archivo_png}'")
    abrir_imagen(archivo_png)

def agregar_nodos(dot, nodo, id_padre=None):
    if nodo and nodo.claves: 
        id_nodo = str(id(nodo))
        label = '|'.join(str(k) for k in nodo.claves)
        dot.node(id_nodo, label)
        if id_padre:
            dot.edge(id_padre, id_nodo)
        for hijo in nodo.hijos:
            agregar_nodos(dot, hijo, id_nodo)

def abrir_imagen(ruta):
    try:
        if os.name == 'nt':
            os.startfile(ruta)
        elif os.name == 'posix':
            subprocess.call(['xdg-open', ruta])
    except Exception as e:
        print(f"No se pudo abrir la imagen: {e}")

# ---------------- MENU ---------------- #
def menu_interactivo():
    try:
        t = int(input("Introduce el grado del Árbol B (t >= 3): "))
        if t < 3:
            print("El grado debe ser al menos 3.")
            return
    except:
        print("Grado inválido.")
        return

    arbol = ArbolB(t)

    while True:
        print("\n=== MENU ===")
        print("1. INSERTAR UN NÚMERO")
        print("2. BUSCAR UN NÚMERO")
        print("3. ELIMINAR UN NÚMERO")
        print("4. CARGAR LISTA DE NÚMEROS DESDE ARCHIVO .CSV")
        print("5. GENERAR GRÁFICO")
        print("6. SALIR")

        opcion = input("Selecciona una opción: ")

        if opcion == '1':
            try:
                numero = int(input("Introduce un número: "))
                arbol.insertar(numero)
                print("¡Número insertado!")
            except:
                print("Entrada inválida.")
        elif opcion == '2':
            try:
                numero = int(input("Número a buscar: "))
                encontrado = arbol.buscar(numero)
                print("Número encontrado." if encontrado else "No encontrado.")
            except:
                print("Entrada inválida.")
        elif opcion == '3':
            try:
                numero = int(input("Número a eliminar: "))
                arbol.eliminar(numero)
                print("¡Número eliminado!")
            except:
                print("Entrada inválida.")
        elif opcion == '4':
            ruta = input("Ruta del archivo CSV: ")
            datos = cargar_desde_csv(ruta)
            for numero in datos:
                arbol.insertar(numero)
            print(f"{len(datos)} números insertados desde CSV.")
        elif opcion == '5':
            generar_y_mostrar_graphviz(arbol)
        elif opcion == '6':
            print("Saliendo del programa. ¡Hasta luego!")
            break
        else:
            print("Opción no válida. Intenta de nuevo.")

if __name__ == "__main__":
    menu_interactivo()
