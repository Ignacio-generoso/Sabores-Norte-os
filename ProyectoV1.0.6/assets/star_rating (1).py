# star_rating.py

import tkinter as tk

class StarRating(tk.Frame):
    def __init__(self, master, num_stars=5, callback=None):
        super().__init__(master)
        self.num_stars = num_stars
        self.callback = callback
        self.selected_stars = 0  # Estado inicial: ninguna estrella seleccionada

        self.create_widgets()
        self.pack()

    def create_widgets(self):
        self.stars = []
        for i in range(self.num_stars):
            star = tk.Label(self, text="★", font=("Arial", 20))
            star.bind("<Enter>", self.on_enter(i))
            star.bind("<Leave>", self.on_leave)
            star.bind("<Button-1>", self.on_click(i))
            self.stars.append(star)
            star.grid(row=0, column=i)

    def on_enter(self, star_index):
        def enter_handler(event):
            if self.selected_stars == 0:
                for i in range(star_index + 1):
                    self.stars[i].config(foreground="orange")

        return enter_handler

    def on_leave(self, event):
        if self.selected_stars == 0:
            for star in self.stars:
                star.config(foreground="black")

    def on_click(self, star_index):
        def click_handler(event):
            self.selected_stars = star_index + 1
            for i in range(len(self.stars)):
                star = self.stars[i]
                if i < self.selected_stars:
                    star.config(foreground="orange")
                else:
                    star.config(foreground="black")

            if self.callback:
                self.callback(self.selected_stars)

        return click_handler

import tkinter as tk
from star_rating import StarRating

def handle_rating(rating):
    print(f"Calificación: {rating} estrellas")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Calificación por Estrellas")

    # Añade el sistema de calificación por estrellas en tu interfaz
    star_rating = StarRating(root, num_stars=5, callback=handle_rating)
    star_rating.pack()

    root.mainloop()
