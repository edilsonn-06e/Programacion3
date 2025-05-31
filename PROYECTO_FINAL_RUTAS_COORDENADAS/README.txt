/************************************ PLANIFICADOR RUTAS TURISTICAS ********************************/

Aplicación web desarrollada con Python y Flask que permite generar rutas turísticas personalizadas dentro de Guatemala, según el presupuesto, horas disponibles y lugar de inicio del usuario.

¿Qué hace esta app?

- Sugiere rutas turísticas completas desde un punto de partida.
- Genera hasta 5 rutas distintas basadas en criterios como:
  - Mayor calificación
  - Mayor número de destinos
  - Ruta más económica
  - Ruta más cercana
  - Ruta equilibrada
- Muestra las rutas en un mapa interactivo.
- Permite cargar/exportar lugares desde archivos CSV.
- Visualiza el Árbol B y las conexiones como grafo.

/*************************************************** INSTALACIÓN Y EJECUCIÓN ******************************************/



1. Requisitos

- Python 3.10 o superior
- pip
- Navegador web (Chrome, Firefox, Edge)
- Windows 10 en adelante

2. Instalación

1. Clona o descarga este repositorio.
2. Abre una terminal en la carpeta del proyecto.
3. Instala las dependencias:

   pip install -r requirements.txt

3. Ejecución

Desde la terminal:

   python app.py

Una vez iniciado el servidor, abrí tu navegador y entra a:

   http://127.0.0.1:5000/

/****************************************************** CÓMO USAR *******************************************************/


Buscar rutas
1. Ingresá tu presupuesto, número de horas disponibles y nombre exacto del lugar de inicio.
2. El sistema generará y mostrará hasta 5 rutas en un mapa interactivo.

Filtro por departamento
- Seleccioná un departamento para ver los destinos disponibles en ese lugar.

Insertar lugar
- Completá el formulario con los datos exactos del nuevo lugar (nombre, coordenadas, calificación).
- Verificá que las coordenadas estén correctas para que se guarde.

Cargar/descargar CSV
- Cargar lugares: subí un archivo CSV con los lugares.
- Cargar conexiones: subí un CSV con las distancias entre lugares.
- Descargar CSV: exportá la información actual.
- Ver Árbol B: descarga una imagen con la estructura del Árbol B y sus conexiones.

/********************************** ESTRUCTURA DEL PROYECTO (MODULOS PRINCIPALES) ***************************************/

- app.py: Controlador principal del sistema y rutas Flask.
- arbol_b.py: Implementación del Árbol B para los lugares.
- grafo.py: Conexiones entre lugares y cálculo de rutas.
- generador_mapa.py: Visualización del mapa usando Folium.
- recomendador.py: Algoritmo que genera las rutas turísticas.
- /templates/: HTMLs que componen la interfaz.

/************************************************** TECNOLOGÍAS UTILIZADAS ************************************************/

- Python + Flask
- Pandas (procesamiento de CSV)
- Folium (mapas interactivos)
- HTML + CSS (interfaz)
- Árbol B y Grafos implementados desde cero

/******************************************************* DESARROLLADO POR **************************************************/

Estudiantes de la Universidad Mariano Gálvez
Proyecto final de Programación III – Sección B

Nombre: Dayna Marianne Meza Maltez
Carnet:	9490-23-3808

Nombre: Edilson Enrique García Villeda
Carnet:	9490-23-2637

Nombre: Luis Samuel Menchú Tun 
Carnet: 9490-23-6285

***** PARTICIPACIÓN DE CADA MIEMBRO ****
Dayna Meza 	--> 	100%
Edilson García 	--> 	100%
Luis Samuel -->   100%
