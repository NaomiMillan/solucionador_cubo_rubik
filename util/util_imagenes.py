from PIL import ImageTk, Image
import os

def leer_imagen(path, size): # Función para poner imágenes de fondo
    return ImageTk.PhotoImage(Image.open(path).resize(size, Image.ADAPTIVE))

