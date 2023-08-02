import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk
from PIL import Image, ImageTk
import json

class App:
    def __init__(self, root):
        # setting title
        root.title("undefined")
        # setting window size
        width = 600
        height = 500
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        # Cargar los datos del archivo JSON
        with open("data/datos.json") as f:
            self.datos = json.load(f)
        
        self.restaurantes = self.datos['restaurantes']

        # Crear el menú en la parte superior
        menu_frame = tk.Frame(root, bg="#90ee90")
        menu_frame.pack(side="top", fill="x")

        GLabel_105 = tk.Label(menu_frame)
        ft = tkFont.Font(family='Times', size=10)
        GLabel_105["font"] = ft
        GLabel_105["fg"] = "#333333"
        GLabel_105["justify"] = "center"
        GLabel_105["text"] = "Inicio"
        GLabel_105.pack(side="left", padx=10, pady=10)

        GButton_483 = tk.Button(menu_frame, bg="#e9e9ed")
        ft = tkFont.Font(family='Times', size=10)
        GButton_483["font"] = ft
        GButton_483["fg"] = "#000000"
        GButton_483["justify"] = "center"
        GButton_483["text"] = "Quienes somos"
        GButton_483.pack(side="left", padx=10, pady=10)

        GButton_435 = tk.Button(menu_frame, bg="#e9e9ed")
        ft = tkFont.Font(family='Times', size=10)
        GButton_435["font"] = ft
        GButton_435["fg"] = "#000000"
        GButton_435["justify"] = "center"
        GButton_435["text"] = "Eventos"
        GButton_435.pack(side="left", padx=10, pady=10)

        GButton_961 = tk.Button(menu_frame, bg="#e9e9ed")
        ft = tkFont.Font(family='Times', size=10)
        GButton_961["font"] = ft
        GButton_961["fg"] = "#000000"
        GButton_961["justify"] = "center"
        GButton_961["text"] = "Contacto"
        GButton_961.pack(side="left", padx=10, pady=10)

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
        self.imagenes = ["assets/resto01.png", "./assets/resto02.png", "./assets/resto03.png", "./assets/resto04.png"]
        # Crear una variable para almacenar el índice de la imagen actual
        self.indice_imagen = 0

        # Cargar la imagen
        imagen_actual = Image.open(self.imagenes[self.indice_imagen])
        imagen_tk = ImageTk.PhotoImage(imagen_actual)

        # Crear etiqueta para la imagen
        self.GLabel_298 = tk.Label(root, image=imagen_tk)
        self.GLabel_298.image = imagen_tk
        self.GLabel_298.pack(fill="x")

        # Crear botones de "adelante" y "atrás"
        GButton_adelante = tk.Button(root, text=">", command=self.cambiar_imagen_adelante)
        GButton_adelante.place(relx=0.95, rely=0.5, anchor="center")

        GButton_atras = tk.Button(root, text="<", command=self.cambiar_imagen_atras)
        GButton_atras.place(relx=0.05, rely=0.5, anchor="w")

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
        # Obtener el elemento correspondiente a ese índice
        elemento_seleccionado = self.datos[indice_seleccionado]
        # Actualizar la etiqueta de la información detallada con los datos del elemento seleccionado
        texto_info_elemento = f"Nombre: {elemento_seleccionado['nombre']}\n" \
                              f"Descripción: {elemento_seleccionado['descripcion']}\n" \
                              f"Precio: {elemento_seleccionado['precio']}\n" \
                              f"Disponibilidad: {elemento_seleccionado['disponibilidad']}"
        self.label_info_elemento.configure(text=texto_info_elemento)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()