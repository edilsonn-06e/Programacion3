
import csv
from arbol_b import Lugar

def cargar_csv(ruta):
    lugares = []
    with open(ruta, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            lugar = Lugar(
                row["nombre"],
                row["departamento"],
                float(row["calificacion"]),
                float(row["costo"]),
                float(row["tiempo"]),
                float(row["latitud"]),
                float(row["longitud"])
            )
            lugares.append(lugar)
    return lugares

def exportar_csv(lugares, ruta):
    with open(ruta, "w", newline='', encoding='utf-8') as csvfile:
        campos = ["nombre", "departamento", "calificacion", "costo", "tiempo", "latitud", "longitud"]
        writer = csv.DictWriter(csvfile, fieldnames=campos)
        writer.writeheader()
        for lugar in lugares:
            writer.writerow(lugar.to_dict())


def cargar_conexiones(ruta, grafo):
    import csv
    with open(ruta, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            origen = row["origen"]
            destino = row["destino"]
            distancia = float(row["distancia"])
            tiempo = float(row["tiempo"])
            grafo.agregar_conexion(origen, destino, distancia, tiempo)
