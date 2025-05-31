
class NodoGrafo:
    def __init__(self, lugar):
        self.lugar = lugar

class Grafo:
    def __init__(self):
        self.nodos = {}  # nombre_lugar -> NodoGrafo
        self.conexiones = {}  # nombre_lugar -> lista de (destino, distancia, tiempo)

    def agregar_lugar(self, nombre, lugar):
        if nombre not in self.nodos:
            self.nodos[nombre] = NodoGrafo(lugar)
            self.conexiones[nombre] = []

    def agregar_conexion(self, origen, destino, distancia, tiempo):
        if origen in self.nodos and destino in self.nodos:
            self.conexiones[origen].append((destino, distancia, tiempo))
            self.conexiones[destino].append((origen, distancia, tiempo))  # conexión bidireccional

    def obtener_vecinos(self, nombre_lugar):
        return self.conexiones.get(nombre_lugar, [])
