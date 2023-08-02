import pip

print("Cargando Modulos:")
try:
    from PIL import Image, ImageTk, ImageDraw, ImageFont
    print("-Pillow")
    import webbrowser
    print("-Webbrowser")
    import cv2
    print("-OpenCV")
    import folium
    print("-Folium")
except ModuleNotFoundError:
    if "Pillow" not in pip.get_installed_distributions():
        pip.main(["install", "Pillow"])
    else:
        print("Module Pillow already installed")
    if "webbrowser" not in pip.get_installed_distributions():
        pip.main(["install", "webbrowser"])
    else:
        print("Module WebBrowser already installed.")
    if "opencv-python" not in pip.get_installed_distributions():
        pip.main(["install", "opencv-python"])
    else:
        print("Module OpenCV already installed.")
    if "folium" not in pip.get_installed_distributions():
        pip.main(["install", "folium"])
    else:
        print("Module Folium already installed.")
        
    from PIL import Image, ImageTk, ImageDraw, ImageFont
    import webbrowser 
    import cv2  
    import folium

print("-Otros Modulos")
import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk
from PIL import Image, ImageTk
import json
import webbrowser
import subprocess
print("Ok.")
print("::Iniciando App::")


class SplashScreen2:
    def __init__(self, parent, filename, timeout=10):
        self.parent = parent
        self.filename = filename
        self.timeout = timeout
        self.top = None
        self.timer = None

    def show(self):
        # Crear la ventana emergente
        self.top = tk.Toplevel(self.parent)
        self.top.overrideredirect(True)
        self.top.geometry("+{}+{}".format(self.parent.winfo_screenwidth()//2, self.parent.winfo_screenheight()//2))

        # Crear un canvas para mostrar el video
        self.canvas = tk.Canvas(self.top, width=640, height=360)
        self.canvas.pack()

        # Cargar el video y reproducirlo en un loop
        self.video = cv2.VideoCapture(self.filename)
        self.after_id = None
        self.play()


    def play(self):
        print("-Muestra Splash Screen")
        cap = cv2.VideoCapture("assets/video.mp4")
        speed = 2 # Speed factor. 0.5 means playback at half speed.
        
        while(cap.isOpened()):
           ret, frame = cap.read()
           cv2.putText(frame, "RESTAURANTES", (10,100), cv2.FONT_HERSHEY_SIMPLEX, 3, (255,200,225), 3)
           cv2.putText(frame, "REGIONALES", (10,200), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2)
           if ret == True:
               cv2.imshow('frame',frame)  
               key = cv2.waitKey(int(speed*10)) 
               if key & 0xFF == ord('q'): # Wait for `speed` second(s).
                   break
               if key % 256 == 27 or key % 256 == 32 or key % 256 == 13:
                    # ESC, space or enter pressed, exit loop
                   break                   
           else: 
               break
        cap.release()
        cv2.destroyWindow('frame')           

    def close(self):
        # Detener el temporizador si todavía está activo
        if self.timer is not None:
            self.top.after_cancel(self.timer)
        # Detener la reproducción del video
        self.video.release()
        if self.after_id is not None:
            self.canvas.after_cancel(self.after_id)
        # Cerrar la ventana
        if self.top is not None:
            self.top.destroy()



class App:
    def __init__(self, root):
    
        root.title("Restaurantes")
        # setting window size
        width = 800
        height = 800
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)
        # Crear un frame para la ventana de comentario
        comentario_frame = tk.Frame(root, bg="#90ee90")
        comentario_frame.pack(side="bottom", fill="x")

        # Cargar los datos del archivo JSON
        with open("data/datos.json") as f:
            self.datos = json.load(f)
        
        self.restaurantes = self.datos['restaurantes']

        # Crear el menú en la parte superior
        menu_frame = tk.Frame(root, bg="#90ee90")
        menu_frame.pack(side="top", fill="x")

        boton_inicio = tk.Label(menu_frame)
        ft = tkFont.Font(family='Times', size=10)
        boton_inicio["font"] = ft
        boton_inicio["fg"] = "#333333"
        boton_inicio["justify"] = "center"
        boton_inicio["text"] = "Inicio"
        boton_inicio.pack(side="left", padx=10, pady=10)

        boton_40 = tk.Button(menu_frame, bg="#e9e9ed", text="eventos", command=self.mostrar_quienes_somos)
        boton_40.pack(side="left", padx=10, pady=10)

        boton_48 = tk.Button(menu_frame, bg="#e9e9ed", text="Quienes somos", command=self.mostrar_quienes_somos)
        boton_48.pack(side="left", padx=10, pady=10)

        # Crear el botón "Contacto" en el menú
        boton_84 = tk.Button(menu_frame, bg="#e9e9ed", text="Contacto", command=self.mostrar_contacto)
        boton_84.pack(side="left", padx=10, pady=10)
        
        # Crear el botón "Contacto" en el menú
        boton_84 = tk.Button(menu_frame, bg="#e9e9ed", text="Mapa", command=self.mostrar_mapa)
        boton_84.pack(side="left", padx=10, pady=10)
    

        # Crear el cuadro de búsqueda
        search_frame = tk.Frame(root, bg="#999999")
        search_frame.pack(fill="x")

        GEntry_1 = tk.Entry(search_frame)
        GEntry_1.pack(side="left", padx=10, pady=10)

        GButton_2 = tk.Button(search_frame, bg="#e9e9ed")
        ft = tkFont.Font(family='Times', size=10)
        GButton_2["font"] = ft
        GButton_2["fg"] = "#000000"
        GButton_2["justify"] = "center"
        GButton_2["text"] = "Buscar"
        GButton_2.pack(side="left", padx=10, pady=10)

        # Crear una lista de elementos a partir de los datos cargados desde el archivo JSON
        self.lista_elementos = tk.Listbox(root, selectmode=tk.SINGLE)
        #for elemento in self.datos:
        #    self.lista_elementos.insert(tk.END, elemento["nombre"])

        for restaurante in self.restaurantes:
                    self.lista_elementos.insert(tk.END, restaurante['nombre'])

        self.lista_elementos.pack(side="left", fill="y")

        # Agregar un controlador de eventos para el evento de selección de elemento de la lista
        self.lista_elementos.bind("<<ListboxSelect>>", self.mostrar_info_elemento_seleccionado)

        # Crear una etiqueta para mostrar la información detallada del elemento seleccionado
        self.label_info_elemento = tk.Label(root, text="", anchor="nw", justify="left")
        self.label_info_elemento.pack(side="left", fill="both", expand=True)

        # Crear una lista de imágenes
        self.imagenes = ["assets/img01.png", "./assets/img02.png", "./assets/img03.png", "./assets/img04.png"]
        # Crear una variable para almacenar el índice de la imagen actual
        self.indice_imagen = 0

        # Cargar la imagen
        imagen_actual = Image.open(self.imagenes[self.indice_imagen])
        imagen_tk = ImageTk.PhotoImage(imagen_actual)

        # Crear etiqueta para la imagen
        self.imagen_actual = Image.open(self.imagenes[self.indice_imagen])
        imagen_tk = ImageTk.PhotoImage(self.imagen_actual)
        self.GLabel_298 = tk.Label(root, image=imagen_tk)
        self.GLabel_298.image = imagen_tk
        self.GLabel_298.pack(fill="x")

        # Agregar un enlace al clickear en la imagen
        def abrir_enlace(event):
            indice_seleccionado = self.lista_elementos.curselection()[0]
            elemento_seleccionado = self.restaurantes[indice_seleccionado] 
            link=elemento_seleccionado['link']
            webbrowser.open_new(link)

        self.GLabel_298.bind("<Button-1>", abrir_enlace)

        # Crear botones de "adelante" y "atrás"
        GButton_adelante = tk.Button(root, text=">", command=self.cambiar_imagen_adelante)
        GButton_adelante.place(relx=0.95, rely=0.5, anchor="center")

        GButton_atras = tk.Button(root, text="<", command=self.cambiar_imagen_atras)
        GButton_atras.place(relx=0.05, rely=0.5, anchor="w")

        # Botón para abrir la ventana de comentarios
        boton_abrir_comentarios = ttk.Button(comentario_frame, text="Agregar Comentario", command=self.ventana_comentarios)
        boton_abrir_comentarios.pack(side="right", padx=10, pady=10)

        self.nombre_restaurante = ""

    # Función para guardar comentarios en el archivo JSON
    def guardar_comentario(self, nombre_restaurante, usuario, comentario, calificacion):
        with open("data/comentarios.json", "r") as archivo:
            data = json.load(archivo)

        nuevo_comentario = {
            "restaurante": nombre_restaurante,
            "usuario": usuario,
            "comentario": comentario,
            "calificacion": calificacion
        }
        data["comentarios"].append(nuevo_comentario)

        with open("data/comentarios.json", "w") as archivo:
            json.dump(data, archivo, indent=4)

    # Función para mostrar los comentarios en una tabla de Tkinter
    def mostrar_comentarios(self, nombre_restaurante=None):  # Argumento opcional
        ventana_comentarios = tk.Toplevel()
        if nombre_restaurante:
            ventana_comentarios.title(f"Comentarios - {nombre_restaurante}")
        else:
            ventana_comentarios.title("Comentarios")

        # Crear tabla
        tabla = ttk.Treeview(ventana_comentarios, columns=("Usuario", "Comentario", "Calificación"), show="headings")
        tabla.heading("Usuario", text="Usuario")
        tabla.heading("Comentario", text="Comentario")
        tabla.heading("Calificación", text="Calificación")
        tabla.pack()

        # Leer datos del archivo JSON y cargar los comentarios del restaurante en la tabla
        with open("data/comentarios.json", "r") as archivo:
            data = json.load(archivo)

        for comentario in data["comentarios"]:
            if not nombre_restaurante or comentario["restaurante"] == nombre_restaurante:
                tabla.insert("", "end", values=(comentario["usuario"], comentario["comentario"], comentario["calificacion"]))


    # Ventana principal para agregar comentarios
    def ventana_comentarios(self):
        def enviar_comentario():
            usuario = entry_usuario.get()
            comentario = entry_comentario.get()
            calificacion = calificacion_var.get()

            self.guardar_comentario(self.nombre_restaurante, usuario, comentario, calificacion)
            ventana_comentarios.destroy()

        ventana_comentarios = tk.Toplevel()
        ventana_comentarios.title("Agregar Comentario")

        # Restaurante seleccionado (nombre del restaurante en esta variable)
        nombre_restaurante = self.nombre_restaurante  # Aquí puedes cambiar el restaurante seleccionado

        # Etiquetas y campos de entrada
        label_usuario = ttk.Label(ventana_comentarios, text="Usuario:")
        label_usuario.pack(pady=5)

        label_comentario = ttk.Label(ventana_comentarios, text="Comentario:")
        label_comentario.pack(pady=5)

        entry_usuario = ttk.Entry(ventana_comentarios)
        entry_usuario.pack(pady=5)

        entry_comentario = ttk.Entry(ventana_comentarios)
        entry_comentario.pack(pady=5)

        # Calificación en estrellas interactivas
        calificacion_var = tk.IntVar()
        calificacion_var.set(1)  # Valor inicial

        calificacion_frame = ttk.LabelFrame(ventana_comentarios, text="Calificación:")
        calificacion_frame.pack(pady=5)

        # Lista para almacenar las etiquetas de estrellas
        estrellas = []

        def calificar_estrella(estrella):
            calificacion_var.set(estrella + 1)
            for i in range(estrella + 1):
                estrellas[i].config(image=estrella_llena_img)
            for i in range(estrella + 1, 5):
                estrellas[i].config(image=estrella_vacia_img)

        # Cargar las imágenes de estrellas llena y vacía (reemplaza 'ruta_estrella_llena' y 'ruta_estrella_vacia' con las rutas de tus imágenes)
        estrella_llena_img = tk.PhotoImage(file="assets/Estrella.png")
        estrella_vacia_img = tk.PhotoImage(file="assets/Estrella2.png")

        for i in range(5):
            estrella_label = tk.Label(calificacion_frame, image=estrella_vacia_img)
            estrella_label.grid(row=0, column=i, padx=5)
            estrella_label.bind("<Enter>", lambda event, estrella=i: calificar_estrella(estrella))
            estrella_label.bind("<Leave>", lambda event, estrella=i: calificar_estrella(calificacion_var.get() - 1))
            estrella_label.bind("<Button-1>", lambda event, estrella=i: calificacion_var.set(estrella + 1))

            estrellas.append(estrella_label)

        boton_enviar = ttk.Button(ventana_comentarios, text="Enviar comentario", command=enviar_comentario)
        boton_enviar.pack(pady=10)

        # Botón para mostrar los comentarios
        boton_mostrar_comentarios = ttk.Button(ventana_comentarios, text="Mostrar Comentarios",
                                              command=lambda: self.mostrar_comentarios(nombre_restaurante))
        boton_mostrar_comentarios.pack(pady=10, padx=5)

    def cambiar_imagen_adelante(self):
        # Actualizar el índice de la imagen
        self.indice_imagen += 1
        # Si se ha llegado al final de la lista, volver al principio
        if self.indice_imagen == len(self.imagenes):
            self.indice_imagen = 0
        # Cargar la nueva imagen
        imagen_actual = Image.open(self.imagenes[self.indice_imagen])
        imagen_tk = ImageTk.PhotoImage(imagen_actual)
        # Actualizar la etiqueta de la imagen
        self.GLabel_298.configure(image=imagen_tk)
        self.GLabel_298.image = imagen_tk

    def cambiar_imagen_atras(self):
        # Actualizar el índice de la imagen
        self.indice_imagen -= 1
        # Si se ha llegado al principio de la lista, volver al final
        if self.indice_imagen < 0:
            self.indice_imagen = len(self.imagenes) - 1
        # Cargar la nueva imagen
        imagen_actual = Image.open(self.imagenes[self.indice_imagen])
        imagen_tk = ImageTk.PhotoImage(imagen_actual)
        # Actualizar la etiqueta de la imagen
        self.GLabel_298.configure(image=imagen_tk)
        self.GLabel_298.image = imagen_tk

    def mostrar_info_elemento_seleccionado(self, event):
        # Obtener el índice del elemento seleccionado en la lista
        indice_seleccionado = self.lista_elementos.curselection()[0]
        print (indice_seleccionado)
        self.imagen_actual = Image.open(self.imagenes[indice_seleccionado])
        imagen_tk = ImageTk.PhotoImage(self.imagen_actual)
        # Actualizar la etiqueta de la imagen
        self.GLabel_298.configure(image=imagen_tk)
        self.GLabel_298.image = imagen_tk


        # Obtener el elemento correspondiente a ese índice
        elemento_seleccionado = self.restaurantes[indice_seleccionado]
        # Actualizar la variable nombre_restaurante
        self.nombre_restaurante = elemento_seleccionado["nombre"]
        # Actualizar la etiqueta de la información detallada con los datos del elemento seleccionado
        texto_info_elemento = f"Nombre: {elemento_seleccionado['nombre']}\n" \
                              f"Direccion: {elemento_seleccionado['direccion']}\n" \
                              f"Popularidad: {elemento_seleccionado['popularidad']}\n" \
                              f"Link: {elemento_seleccionado['link']}"
        #self.label_info_elemento.configure(text=texto_info_elemento)
        print (texto_info_elemento)
        
    def mostrar_comentarios_seleccionado(self):
        # Verificar que se haya seleccionado un restaurante antes de mostrar los comentarios
        if self.nombre_restaurante:
            self.mostrar_comentarios(self.nombre_restaurante)
        else:
            # Mostrar un mensaje de error si no se ha seleccionado un restaurante
            messagebox.showerror("Error", "Por favor, selecciona un restaurante antes de mostrar los comentarios.")


    def mostrar_quienes_somos(self):
        # Crear una nueva ventana emergente para "Quienes somos"
        quienes_somos_window = tk.Toplevel()
        quienes_somos_window.title("Quienes somos")

        # Agregar etiquetas con la información de "Quienes somos"
        tk.Label(quienes_somos_window, text="Este programa esta diseñado.").pack()
        tk.Label(quienes_somos_window, text="Nombre de los integrantes").pack()

        # Agregar un botón "Cerrar" para cerrar la ventana emergente
        tk.Button(quienes_somos_window, text="Cerrar", command=quienes_somos_window.destroy).pack()

        # Establecer la posición y el tamaño de la ventana emergente
        quienes_somos_window.geometry("300x200+500+200")

    def mostrar_contacto(self):
        # Crear una nueva ventana emergente para "Contacto"
        contacto_window = tk.Toplevel()
        contacto_window.title("Contacto")

        # Agregar etiquetas con la información de "Contacto"
        tk.Label(contacto_window, text="Por consulta o sugerencia te comunicas al:").pack()
        tk.Label(contacto_window, text="Telefono: 387 4578615").pack()
        tk.Label(contacto_window, text="Correo electrónico: sabores_norteño@empresa.com").pack()

        # Agregar un botón "Cerrar" para cerrar la ventana emergente
        tk.Button(contacto_window, text="Cerrar", command=contacto_window.destroy).pack()

        # Establecer la posición y el tamaño de la ventana emergente
        contacto_window.geometry("300x200+500+200")

    def mostrar_mapa(self):
        # Crear una nueva ventana para Mapas
        print('Ejecutando Mapas')
        subprocess.Popen(['python', 'mapa.py'])

  

if __name__ == "__main__":
    root = tk.Tk()

    # Crear una instancia del splash screen
    #splash = SplashScreen(root, "assets/splash.jpg", timeout=10)
    splash = SplashScreen2(root, "splash.mp4", timeout=10)

    # Mostrar el splash screen
    splash.show()

    # Iniciar la aplicación principal
    app = App(root)
    root.mainloop()


