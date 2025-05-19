from collections import deque

def recomendar_rutas(grafo, origen, presupuesto_max, tiempo_max):
    rutas = []

    if origen not in grafo.nodos:
        return []

    # Preparar BFS limitado con acumuladores
    def buscar_rutas(criterio, limite=5):
        rutas_encontradas = []
        visitadas = set()

        queue = deque()
        queue.append(([origen], 0.0, 0.0))  # (ruta, costo, tiempo)

        while queue and len(rutas_encontradas) < limite:
            ruta, costo_total, tiempo_total = queue.popleft()
            actual = ruta[-1]

            if len(ruta) > 1:
                rutas_encontradas.append((ruta, costo_total, tiempo_total))

            for vecino, dist, tiempo in grafo.obtener_vecinos(actual):
                if vecino in ruta:
                    continue
                lugar_vecino = grafo.nodos[vecino].lugar
                nuevo_costo = costo_total + lugar_vecino.costo
                nuevo_tiempo = tiempo_total + lugar_vecino.tiempo
                if nuevo_costo <= presupuesto_max and nuevo_tiempo <= tiempo_max:
                    queue.append((ruta + [vecino], nuevo_costo, nuevo_tiempo))

        # Aplicar criterio de ordenamiento
        if criterio == "calificacion":
            rutas_encontradas.sort(key=lambda r: sum(grafo.nodos[n].lugar.calificacion for n in r[0]), reverse=True)
        elif criterio == "cantidad":
            rutas_encontradas.sort(key=lambda r: len(r[0]), reverse=True)
        elif criterio == "equilibrado":
            rutas_encontradas.sort(key=lambda r: (sum(grafo.nodos[n].lugar.calificacion for n in r[0]) / len(r[0])) if len(r[0]) > 0 else 0, reverse=True)
        elif criterio == "cercania":
            rutas_encontradas.sort(key=lambda r: len(r[0]))  # simulación simple: ruta corta
        elif criterio == "costo":
            rutas_encontradas.sort(key=lambda r: r[1])  # menor costo total

        return [r[0] for r in rutas_encontradas[:1]]  # solo la mejor por criterio

    rutas += buscar_rutas("calificacion")
    rutas += buscar_rutas("cantidad")
    rutas += buscar_rutas("equilibrado")
    rutas += buscar_rutas("cercania")
    rutas += buscar_rutas("costo")

    return rutas
