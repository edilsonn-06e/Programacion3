import folium
import os



def generar_mapa(lugares, grafo=None, origen_nombre=None):
    if not lugares:
        # Si no hay lugares, se pone en guatemala xd
        mapa = folium.Map(location=[15.5, -90.25], zoom_start=7)
    else:
        promedio_lat = sum([l.latitud for l in lugares]) / len(lugares)
        promedio_lon = sum([l.longitud for l in lugares]) / len(lugares)
        mapa = folium.Map(location=[promedio_lat, promedio_lon], zoom_start=7)

        coords = {}
        for lugar in lugares: #ESTO SIRVE PARA MOSTRAR LOS LUGARES EN EL MAPA
            popup_html = f"""
            <b>{lugar.nombre}</b><br>
            Calificación: {lugar.calificacion}/5<br>
            Q{lugar.costo} – {lugar.tiempo} hrs<br>
            <a href='/?calificar={lugar.nombre}' target='_parent' style='color:white; text-decoration:none;' class='btn btn-sm btn-primary mt-2'>Calificar</a>
            """
            folium.Marker(
                location=[lugar.latitud, lugar.longitud],
                popup=folium.Popup(popup_html, max_width=250),
                tooltip=lugar.nombre
            ).add_to(mapa)

            coords[lugar.nombre] = (lugar.latitud, lugar.longitud)

        # DIBUJA LAS LINEAS ENTRE LOS GRAFOS SOLO SI HAY CONEXION, SINO NO MUESTRA NA'
        if grafo and origen_nombre in grafo.nodos:
            if origen_nombre and len(lugares) > 1:
                secuencia_coords = [(l.latitud, l.longitud) for l in lugares]
                folium.PolyLine(
                    secuencia_coords,
                    color="blue",
                    weight=4,
                    opacity=0.6
                ).add_to(mapa)

    # Guardar el mapa
    base_dir = os.path.abspath(os.path.dirname(__file__))
    ruta_mapa = os.path.join(base_dir, "..", "static", "mapa.html")
    ruta_mapa = os.path.normpath(ruta_mapa)
    os.makedirs(os.path.dirname(ruta_mapa), exist_ok=True)
    mapa.save(ruta_mapa)
