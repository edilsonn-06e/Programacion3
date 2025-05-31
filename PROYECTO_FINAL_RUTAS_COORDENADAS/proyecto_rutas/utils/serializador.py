
import pickle

def guardar_arbol(arbol, ruta):
    with open(ruta, "wb") as f:
        pickle.dump(arbol, f)

def cargar_arbol(ruta):
    try:
        with open(ruta, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return None

def guardar_grafo(grafo, ruta):
    with open(ruta, "wb") as f:
        pickle.dump(grafo, f)

def cargar_grafo(ruta):
    try:
        with open(ruta, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return None
