
import math

class Lugar:
    def __init__(self, nombre, departamento, calificacion, costo, tiempo, latitud, longitud):
        self.nombre = nombre
        self.departamento = departamento
        self.calificacion = float(calificacion)
        self.costo = float(costo)
        self.tiempo = float(tiempo)
        self.latitud = float(latitud)
        self.longitud = float(longitud)

    def __lt__(self, other):
        return self.nombre < other.nombre

    def __eq__(self, other):
        return self.nombre == other.nombre

    def to_dict(self):
        return {
            "nombre": self.nombre,
            "departamento": self.departamento,
            "calificacion": self.calificacion,
            "costo": self.costo,
            "tiempo": self.tiempo,
            "latitud": self.latitud,
            "longitud": self.longitud
        }

    def to_dict(self):
        return {
            "nombre": self.nombre,
            "departamento": self.departamento,
            "calificacion": self.calificacion,
            "costo": self.costo,
            "tiempo": self.tiempo
        }

class NodoB:
    def __init__(self, t):
        self.t = t
        self.claves = []
        self.hijos = []
        self.hoja = True

    def dividir(self, padre, indice):
        if len(self.claves) < self.t:
            return  # No hay suficientes claves para dividir
        nuevo = NodoB(self.t)
        nuevo.hoja = self.hoja
        mid = self.t - 1
        padre.claves.insert(indice, self.claves[mid])
        padre.hijos.insert(indice + 1, nuevo)

        nuevo.claves = self.claves[mid + 1:]
        self.claves = self.claves[:mid]

        if not self.hoja:
            nuevo.hijos = self.hijos[mid + 1:]
            self.hijos = self.hijos[:mid + 1]

    def insertar_no_lleno(self, clave):
        if self.hoja:
            self.claves.append(clave)
            self.claves.sort(key=lambda x: x.nombre)
        else:
            i = len(self.claves) - 1
            while i >= 0 and clave.nombre < self.claves[i].nombre:
                i -= 1
            i += 1
            if len(self.hijos[i].claves) == (2 * self.t) - 1:
                self.hijos[i].dividir(self, i)
                if clave.nombre > self.claves[i].nombre:
                    i += 1
            self.hijos[i].insertar_no_lleno(clave)

    def recorrer_inorden(self):
        resultado = []
        for i in range(len(self.claves)):
            if not self.hoja:
                resultado += self.hijos[i].recorrer_inorden()
            resultado.append(self.claves[i])
        if not self.hoja:
            resultado += self.hijos[-1].recorrer_inorden()
        return resultado

class ArbolB:
    def __init__(self, t):
        self.raiz = NodoB(t)
        self.t = t

    def insertar(self, lugar):
        raiz = self.raiz
        if len(raiz.claves) == (2 * self.t) - 1:
            nueva_raiz = NodoB(self.t)
            nueva_raiz.hoja = False
            nueva_raiz.hijos.append(raiz)
            nueva_raiz.dividir(nueva_raiz, 0)
            self.raiz = nueva_raiz
            self._insertar_no_lleno(self.raiz, lugar)
        else:
            self._insertar_no_lleno(raiz, lugar)

    def _insertar_no_lleno(self, nodo, lugar):
        nodo.insertar_no_lleno(lugar)

    def obtener_lugares(self):
        return self.raiz.recorrer_inorden()
