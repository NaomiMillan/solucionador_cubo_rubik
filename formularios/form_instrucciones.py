import tkinter as tk
from tkinter import Label, Button
from tkinter.ttk import Combobox
from tkinter import filedialog
import cv2
import util.util_imagenes as util_img 

class Instrucciones: # Clase para mostrar las instrucciones
    
    def __init__(self, panel_principal, controlador): # Constructor

        self.panel_principal = panel_principal
        self.controlador = controlador
        self.fondo = util_img.leer_imagen("./imagenes/instrucciones.png", (1270, 700))

        self.bg_label = tk.Label(self.panel_principal, image=self.fondo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.bg_label.image = self.fondo 
        
        self.barra_menu=tk.Frame(panel_principal, bg="#800080")
        self.barra_menu.pack(side=tk.TOP, fill=tk.X, expand=False)

        self.componentes()
           
    def componentes(self): # Posicionar componentes
 
       #menu_botones

       # Botón 5 - instrucciones 
       self.boton5 = tk.Button(self.barra_menu, text="Instrucciones", bg="#1EAB1E", fg="#FFFFFF", font=("Roboto", 13), height=1)
       self.boton5.pack(side=tk.LEFT, fill=tk.X, expand=True)
       self.boton5.bind("<Button-1>", self.funcion_boton5)

       # Botón 1 - movimientos
       self.boton1 = tk.Button(self.barra_menu, text="Aprender Movimientos", bg="#F17824", fg="#FFFFFF", font=("Roboto", 13), height=1)
       self.boton1.pack(side=tk.LEFT, fill=tk.X, expand=True)
       self.boton1.bind("<Button-1>", self.funcion_boton1)

        # Botón 2 - algoritmo
       self.boton2 = tk.Button(self.barra_menu, text="Resolver Cubo", bg="#2240DA", fg="#FFFFFF", font=("Roboto", 13), height=1)
       self.boton2.pack(side=tk.LEFT, fill=tk.X, expand=True)
       self.boton2.bind("<Button-1>", self.funcion_boton2)

       # Botón 4 - acerca del proyecto
       self.boton4 = tk.Button(self.barra_menu, text="Acerca del Proyecto", bg="#EC3C24", fg="#FFFFFF", font=("Roboto", 13), height=1)
       self.boton4.pack(side=tk.LEFT, fill=tk.X, expand=True)
       self.boton4.bind("<Button-1>", self.funcion_boton4)

    def funcion_boton1(self, event): # evento - movimientos
        self.controlador.mostrar_movimientos()

    def funcion_boton2(self, event): # evento - algoritmo
        #self.controlador.mostrar_resolver2("OOYGYBYROYYBRRRRRRRYYGGGGGGGYROOOOOOGYBBBBBBBWWWWWWWWW")
        self.controlador.mostrar_resolver()

    def funcion_boton4(self, event): # evento - acerca del proyecto
        self.controlador.mostrar_proyecto2()

    def funcion_boton5(self, event): # evento - instrucciones
        pass


