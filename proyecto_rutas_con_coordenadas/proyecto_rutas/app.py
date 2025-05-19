
from flask import Flask, render_template, request, redirect, send_file
import os
from arbol_b import ArbolB, Lugar
from utils.generador_mapa import generar_mapa
from utils.parser_csv import cargar_csv, exportar_csv, cargar_conexiones
from utils.serializador import guardar_arbol, cargar_arbol, guardar_grafo, cargar_grafo
from recomendador import recomendar_rutas



from grafo import Grafo

#grafo = Grafo()
ARCHIVO_ARBOL = os.path.join(os.path.dirname(__file__), "datos", "arbol_guardado.pkl")
ARCHIVO_GRAFO = os.path.join(os.path.dirname(__file__), "datos", "grafo_guardado.pkl")
arbol = cargar_arbol(ARCHIVO_ARBOL) or ArbolB(3)
grafo = cargar_grafo(ARCHIVO_GRAFO) or Grafo()
rutas = []




app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'datos')

#arbol = ArbolB(3)  # Grado mínimo t = 3

@app.route("/")
def inicio():
    lugares = arbol.obtener_lugares()
    departamentos = sorted(set(l.departamento for l in lugares))
    depto_filtrado = request.args.get("departamento")
    calificar_lugar = request.args.get("calificar")  # <<--- nuevo

    lugares_filtrados = [l for l in lugares if l.departamento == depto_filtrado] if depto_filtrado else []
    generar_mapa(lugares_filtrados if depto_filtrado else [])
    
    return render_template(
        "inicio.html",
        lugares=lugares_filtrados,
        departamentos=departamentos,
        calificar=calificar_lugar  # <<--- lo mandamos al template
    )


@app.route("/recomendar", methods=["POST"])
def recomendar():
    global rutas
    origen = request.form["origen"].strip()
    presupuesto = float(request.form["presupuesto"])
    horas = float(request.form["horas"])
    rutas = recomendar_rutas(grafo, origen, presupuesto, horas)
    generar_mapa([], grafo=grafo, origen_nombre=origen)  # Mapa limpio, sin ruta aún
    return render_template("inicio.html", lugares=[], departamentos=[], rutas=rutas)


@app.route("/insertar", methods=["GET", "POST"])
def insertar():
    if request.method == "POST":
            nombre = request.form["nombre"]
            depto = request.form["departamento"]
            calif = float(request.form["calificacion"])
            costo = float(request.form["costo"])
            tiempo = float(request.form["tiempo"])
            lat = float(request.form["latitud"])
            lon = float(request.form["longitud"])
            lugar = Lugar(nombre, depto, calif, costo, tiempo, lat, lon)
            arbol.insertar(lugar)
            grafo.agregar_lugar(lugar.nombre, lugar)
            guardar_grafo(grafo, ARCHIVO_GRAFO)
            guardar_arbol(arbol, ARCHIVO_ARBOL)
            return redirect("/insertar")
    return render_template("insertar.html")

@app.route("/cargar_csv", methods=["POST"])
def cargar():
    archivo = request.files["archivo"]
    if archivo:
        path = os.path.join(app.config["UPLOAD_FOLDER"], archivo.filename)
        archivo.save(path)
        lugares = cargar_csv(path)
        for lugar in lugares:
            arbol.insertar(lugar)
            grafo.agregar_lugar(lugar.nombre, lugar)
        guardar_grafo(grafo, ARCHIVO_GRAFO)
        guardar_arbol(arbol, ARCHIVO_ARBOL)
    return redirect("/cargar_descargar")

@app.route("/descargar_csv")
def descargar():
    path = os.path.join(app.config["UPLOAD_FOLDER"], "lugares_exportados.csv")
    exportar_csv(arbol.obtener_lugares(), path)
    return send_file(path, as_attachment=True)

@app.route("/cargar_conexiones", methods=["POST"])
def cargar_conexiones_csv():
    archivo = request.files["archivo_conexiones"]
    if archivo:
        path = os.path.join(app.config["UPLOAD_FOLDER"], archivo.filename)
        os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
        archivo.save(path)
        cargar_conexiones(path, grafo)
        guardar_grafo(grafo, ARCHIVO_GRAFO)
    return redirect("/cargar_descargar")

@app.route("/cargar_descargar")
def cargar_descargar():
    return render_template("cargar_descargar.html")

@app.route("/reset")
def reset():
    global arbol, grafo
    try:
        os.remove(ARCHIVO_ARBOL)
    except FileNotFoundError:
        pass
    try:
        os.remove(ARCHIVO_GRAFO)
    except FileNotFoundError:
        pass

    arbol = ArbolB(3)
    grafo = Grafo()

    return redirect("/")

@app.route("/mostrar_ruta")
def mostrar_ruta():
    ruta_id = int(request.args.get("ruta_id", 0))
    if 0 <= ruta_id < len(rutas):
        secuencia = rutas[ruta_id]
        lugares_ruta = [grafo.nodos[n].lugar for n in secuencia if n in grafo.nodos]
        generar_mapa(lugares_ruta, grafo=grafo, origen_nombre=secuencia[0])
        return render_template("inicio.html", lugares=lugares_ruta, departamentos=[], rutas=rutas)
    return redirect("/")


@app.route("/calificar", methods=["POST"])
def calificar():
    nombre = request.form["nombre"]
    nueva = float(request.form["calificacion"])

    if nombre in grafo.nodos:
        lugar = grafo.nodos[nombre].lugar

        # Si ya tiene votos anteriores, actualizamos promedio
        if hasattr(lugar, "votos"):
            lugar.calificacion = round(((lugar.calificacion * lugar.votos) + nueva) / (lugar.votos + 1), 2)
            lugar.votos += 1
        else:
            lugar.votos = 1
            lugar.calificacion = nueva

        # Guardamos cambios
        guardar_arbol(arbol, ARCHIVO_ARBOL)
        guardar_grafo(grafo, ARCHIVO_GRAFO)

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
