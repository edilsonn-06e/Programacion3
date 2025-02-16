from graphviz import Digraph
import subprocess
import platform


class Nodo:
    def __init__(self, nombre, apellido, carnet):
        self.nombre = nombre
        self.apellido = apellido
        self.carnet = carnet
        self.siguiente = None
        self.anterior = None


class ListaDobleEnlazada:
    def __init__(self):
        self.head = None

    def agregar_al_inicio(self, nombre, apellido, carnet):
        nuevo_nodo = Nodo(nombre, apellido, carnet)
        if self.head is None:
            self.head = nuevo_nodo
        else:
            nuevo_nodo.siguiente = self.head
            self.head.anterior = nuevo_nodo
            self.head = nuevo_nodo

    def agregar_al_final(self, nombre, apellido, carnet):
        nuevo_nodo = Nodo(nombre, apellido, carnet)
        if self.head is None:
            self.head = nuevo_nodo
        else:
            nodo_actual = self.head
            while nodo_actual.siguiente is not None:
                nodo_actual = nodo_actual.siguiente
            nodo_actual.siguiente = nuevo_nodo
            nuevo_nodo.anterior = nodo_actual

    def eliminar_por_valor(self, carnet):
        nodo_actual = self.head
        while nodo_actual is not None:
            if nodo_actual.carnet == carnet:
                if nodo_actual.anterior is not None:
                    nodo_actual.anterior.siguiente = nodo_actual.siguiente
                if nodo_actual.siguiente is not None:
                    nodo_actual.siguiente.anterior = nodo_actual.anterior
                if nodo_actual == self.head:
                    self.head = nodo_actual.siguiente
                return True
            nodo_actual = nodo_actual.siguiente
        return False

    def imprimir_lista(self):
        nodo_actual = self.head
        resultado = "None"
        while nodo_actual is not None:
            resultado += f" <- [{nodo_actual.nombre} {nodo_actual.apellido} {nodo_actual.carnet}] ->"
            nodo_actual = nodo_actual.siguiente
        resultado += " None"
        print(resultado)

    def generar_grafico(self):
        dot = Digraph(comment='Lista Doblemente Enlazada')
        nodo_actual = self.head
        while nodo_actual is not None:
            label = f"{nodo_actual.nombre} {nodo_actual.apellido} {nodo_actual.carnet}"
            dot.node(str(id(nodo_actual)), label)
            if nodo_actual.siguiente is not None:
                dot.edge(str(id(nodo_actual)), str(id(nodo_actual.siguiente)), label="siguiente")
            if nodo_actual.anterior is not None:
                dot.edge(str(id(nodo_actual)), str(id(nodo_actual.anterior)), label="anterior")
            nodo_actual = nodo_actual.siguiente
        nombre_archivo = 'lista_doble_enlazada'
        dot.render(nombre_archivo, format='png', cleanup=True)
        print(f"Gráfico generado como '{nombre_archivo}.png'")

        # Abrir la imagen automáticamente
        self.abrir_imagen(nombre_archivo + '.png')

    def abrir_imagen(self, ruta_imagen):
        sistema_operativo = platform.system()
        try:
            if sistema_operativo == "Windows":
                subprocess.run(['start', ruta_imagen], shell=True)
            elif sistema_operativo == "Darwin":  # macOS
                subprocess.run(['open', ruta_imagen])
            elif sistema_operativo == "Linux":
                subprocess.run(['xdg-open', ruta_imagen])
            else:
                print(f"No se pudo abrir la imagen automáticamente en el sistema operativo: {sistema_operativo}")
        except Exception as e:
            print(f"Error al abrir la imagen: {e}")


def main():
    lista = ListaDobleEnlazada()
    while True:
        print("\nOpciones:")
        print("1. Agregar al inicio")
        print("2. Agregar al final")
        print("3. Imprimir lista")
        print("4. Eliminar por carnet")
        print("5. Generar gráfico")
        print("6. Salir")
        opcion = input("Elige una opción: ")

        if opcion == "1":
            nombre = input("Introduce el nombre: ")
            apellido = input("Introduce el apellido: ")
            carnet = input("Introduce el carnet: ")
            lista.agregar_al_inicio(nombre, apellido, carnet)
        elif opcion == "2":
            nombre = input("Introduce el nombre: ")
            apellido = input("Introduce el apellido: ")
            carnet = input("Introduce el carnet: ")
            lista.agregar_al_final(nombre, apellido, carnet)
        elif opcion == "3":
            print("La lista es: ")
            lista.imprimir_lista()
        elif opcion == "4":
            carnet = input("Introduce el carnet del nodo a eliminar: ")
            if lista.eliminar_por_valor(carnet):
                print(f"El nodo con carnet {carnet} ha sido eliminado de la lista.")
            else:
                print(f"El nodo con carnet {carnet} no se encontró en la lista.")
        elif opcion == "5":
            lista.generar_grafico()
        elif opcion == "6":
            break
        else:
            print("Opción no válida, intenta de nuevo.")


if __name__ == "__main__":
    main()