import json
import tkinter as tk
import folium
from folium import IFrame
import webbrowser
import requests
import polyline

def cargar_json(archivo):
    """
    Carga datos desde un archivo JSON.
    
    :param archivo: Ruta del archivo JSON.
    :return: Datos cargados desde el archivo JSON o None si ocurre un error.
    """
    try:
        with open(archivo, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
            return datos
    except FileNotFoundError:
        print(f"El archivo {archivo} no fue encontrado.")
        return None
    except json.JSONDecodeError:
        print(f"Error al decodificar el archivo {archivo}.")
        return None

def mostrar_destinos():
    """
    Muestra la lista de destinos en la interfaz de usuario.
    """
    for i, restaurante in enumerate(datos_culinarios["restaurantes"]):
        lista_destinos.insert(i, restaurante["nombre"])
        
def mostrar_detalles_mapa(restaurante):
    """
    Muestra los detalles de un restaurante en el mapa.
    
    :param restaurante: Diccionario con información del restaurante.
    """
    mensaje = f"""
    {restaurante['nombre']}\n
    Tipo de Cocina: {', '.join(restaurante['tipo_cocina'])}
    Dirección: {restaurante['direccion']}
    Popularidad: {restaurante['popularidad']}
    Disponibilidad: {restaurante['disponibilidad']}
    """
    
restaurante_seleccionado = None
coordenadas_seleccionadas = []

def on_select(event):
    """
    Manejador de eventos para cuando se selecciona un elemento en la lista de destinos.
    
    :param event: Objeto de evento generado por tkinter.
    """
    global restaurante_seleccionado
    indices = lista_destinos.curselection()
    if indices:
        coordenadas_seleccionadas.clear()
        for index in indices:
            restaurante_seleccionado = datos_culinarios["restaurantes"][index]
            mostrar_detalles_mapa(restaurante_seleccionado)
            
            # Almacenar las coordenadas del restaurante seleccionado
            latitud = restaurante_seleccionado["latitud"]
            longitud = restaurante_seleccionado["longitud"]
            coordenadas_seleccionadas.append((latitud, longitud))

def abrir_mapa():
    """
    Abre el mapa en el navegador web predeterminado.
    """
    if restaurante_seleccionado:
        latitud = restaurante_seleccionado["latitud"]
        longitud = restaurante_seleccionado["longitud"]
        mapa = folium.Map(location=[latitud, longitud], zoom_start=16)
        
        for restaurante in datos_culinarios["restaurantes"]:
            latitud = restaurante["latitud"]
            longitud = restaurante["longitud"]
            # Crear un elemento Popup personalizado para cada marcador
            popup_html = f"""
            <div style="width: 250px;">
                <h3 style="color: red;">{restaurante['nombre']}</h3>
                <p><strong>Tipo de Cocina:</strong> {', '.join(restaurante['tipo_cocina'])}</p>
                <p><strong>Dirección:</strong> {restaurante['direccion']}</p>
                <p><strong>Popularidad:</strong> {restaurante['popularidad']}</p>
                <p><strong>Disponibilidad:</strong> {restaurante['disponibilidad']}</p>
                <h4>Platos</h4>
                <ul>
            """
            for plato in restaurante["platos"]:
                popup_html += f"<li>{plato['nombre']} - Ars {plato['precio']} ({plato['calificacion']})</li>"
            popup_html += """
                </ul>
            </div>
            """
            iframe = IFrame(popup_html, width=270, height=300)
            popup = folium.Popup(iframe, max_width=2650)
            folium.Marker([latitud, longitud], popup=popup).add_to(mapa)
        
        mapa.save("mapa.html")
        webbrowser.open("mapa.html")

def get_route(lat_a, lon_a, lat_b, lon_b, url="https://router.project-osrm.org/route/v1/driving/"):
    """
    Obtiene una ruta entre dos puntos utilizando el servicio de enrutamiento OSRM.
    
    :param lat_a: Latitud del punto de origen.
    :param lon_a: Longitud del punto de origen.
    :param lat_b: Latitud del punto de destino.
    :param lon_b: Longitud del punto de destino.
    :param url: URL del servicio de enrutamiento OSRM.
    :return: Lista de coordenadas que representan la ruta entre los puntos de origen y destino.
    """
    location = f"{lon_a},{lat_a};{lon_b},{lat_b}"
    response = requests.get(url + location)
    if response.status_code != 200:
        print(f"Error en la solicitud con código de estado {response.status_code}")
        return None
    response_json = response.json()
    route = polyline.decode(response_json['routes'][0]['geometry'])
    return route

def trazar_ruta(lat_a, lon_a, lat_b, lon_b):
    """
    Traza una ruta entre dos puntos en el mapa.
    
    :param lat_a: Latitud del punto de origen.
    :param lon_a: Longitud del punto de origen.
    :param lat_b: Latitud del punto de destino.
    :param lon_b: Longitud del punto de destino.
    """
    # Obtener la ruta entre los puntos de origen y destino
    route = get_route(lat_a, lon_a, lat_b, lon_b)

    # Crear un objeto mapa con Folium
    mapa = folium.Map(location=[lat_a, lon_a], zoom_start=16)

    # Agregar la ruta al mapa
    folium.PolyLine(route, color="blue").add_to(mapa)

    # Agregar marcadores para el origen y el destino
    folium.Marker([lat_a, lon_a], popup="Origen").add_to(mapa)
    folium.Marker([lat_b, lon_b], popup="Destino").add_to(mapa)
    
    for restaurante in datos_culinarios["restaurantes"]:
        latitud = restaurante["latitud"]
        longitud = restaurante["longitud"]
        # Crear un elemento Popup personalizado para cada marcador
        popup_html = f"""
        <div style="width: 250px;">
            <h3 style="color: red;">{restaurante['nombre']}</h3>
            <p><strong>Tipo de Cocina:</strong> {', '.join(restaurante['tipo_cocina'])}</p>
            <p><strong>Dirección:</strong> {restaurante['direccion']}</p>
            <p><strong>Popularidad:</strong> {restaurante['popularidad']}</p>
            <p><strong>Disponibilidad:</strong> {restaurante['disponibilidad']}</p>
            <h4>Platos</h4>
            <ul>
        """
        for plato in restaurante["platos"]:
            popup_html += f"<li>{plato['nombre']} - Ars {plato['precio']} ({plato['calificacion']})</li>"
        popup_html += """
            </ul>
        </div>
        """
        iframe = IFrame(popup_html, width=270, height=300)
        popup = folium.Popup(iframe, max_width=2650)
        folium.Marker([latitud, longitud], popup=popup).add_to(mapa)
    
    mapa.save("mapa.html")
    webbrowser.open("mapa.html")

def on_boton_ruta_click():
    """
    Manejador de eventos para cuando se hace clic en el botón "Trazar Ruta".
    """
    if len(coordenadas_seleccionadas) >= 2:
        lat_a, lon_a = coordenadas_seleccionadas[0]
        lat_b, lon_b = coordenadas_seleccionadas[-1]
        trazar_ruta(lat_a, lon_a, lat_b, lon_b)

datos_json = "./data/datos.json"
datos_culinarios = cargar_json(datos_json)

if datos_culinarios:
    # Crear la ventana principal de la interfaz de usuario
    ventana = tk.Tk()
    ventana.title("Restaurantes Salteños")

    # Crear la lista de destinos
    lista_destinos = tk.Listbox(ventana, height=10, selectmode=tk.EXTENDED)
    lista_destinos.pack()
    
    # Asociar el manejador de eventos a la lista de destinos
    lista_destinos.bind("<ButtonRelease-1>", on_select)

    # Crear el botón para abrir el mapa
    boton_mapa = tk.Button(ventana, text="Abrir Mapa")
    boton_mapa.pack()
    boton_mapa.config(command=abrir_mapa)

    # Crear el botón para trazar la ruta
    boton_ruta = tk.Button(ventana, text="Trazar Ruta")
    boton_ruta.pack()
    boton_ruta.config(command=on_boton_ruta_click)

    # Mostrar la lista de destinos
    mostrar_destinos()

    # Iniciar el bucle principal de la interfaz de usuario
    ventana.mainloop()

else:
    print("Error al intentar cargar los datos.")
    