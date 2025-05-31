from graphviz import Digraph

def graficar_arbol(arbol, path_salida="static/arbol_b.png"):
    dot = Digraph()
    dot.attr('node', shape='record')

    def agregar_nodo(nodo, id_nodo=0):
        if nodo is None:
            return id_nodo

        nodo_id = f"n{id_nodo}"
        etiquetas = "|".join([f"<f{i}> {lugar.nombre}" for i, lugar in enumerate(nodo.claves)])
        dot.node(nodo_id, f"{{{etiquetas}}}")

        id_actual = id_nodo + 1
        for i, hijo in enumerate(nodo.hijos):
            hijo_id = f"n{id_actual}"
            id_actual = agregar_nodo(hijo, id_actual)
            dot.edge(nodo_id, hijo_id)

        return id_actual

    agregar_nodo(arbol.raiz)
    dot.render(filename=path_salida.replace(".png", ""), format='png', cleanup=True)
