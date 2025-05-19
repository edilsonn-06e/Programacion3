import folium

def generar_mapa(lugares, grafo=None, origen_nombre=None):
    if not lugares:
        mapa = folium.Map(location=[15.5, -90.25], zoom_start=7)
        mapa.save("proyecto_rutas/static/mapa.html")
        return

    promedio_lat = sum([l.latitud for l in lugares]) / len(lugares)
    promedio_lon = sum([l.longitud for l in lugares]) / len(lugares)
    mapa = folium.Map(location=[promedio_lat, promedio_lon], zoom_start=7)

    coords = {}
    for lugar in lugares:
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

    # Dibujar líneas si hay grafo y origen
    if grafo and origen_nombre in grafo.nodos:
        origen_coords = coords.get(origen_nombre)
        if origen_coords:
            conexiones = grafo.obtener_vecinos(origen_nombre)
            if origen_nombre and len(lugares) > 1:
                secuencia_coords = [(l.latitud, l.longitud) for l in lugares]
                folium.PolyLine(
                    secuencia_coords,
                    color="blue",
                    weight=4,
                    opacity=0.6
                ).add_to(mapa)


    mapa.save("proyecto_rutas/static/mapa.html")
