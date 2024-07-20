import tkinter as tk
from formularios.form_proyecto2 import Proyecto2
from formularios.form_proyecto3 import Proyecto3
from formularios.form_resolver import Resolver
from formularios.form_resolver2 import Resolver2
from formularios.form_instrucciones import Instrucciones
from formularios.form_movimientos import Movimientos
from formularios.form_movimientos2 import Movimientos2

class Controlador: # Clase para controlar los accesos a todos los paneles

    cad=""

    def __init__(self, panel_principal): # Constructor
        self.panel_principal = panel_principal
        self.mostrar_instrucciones()

    def mostrar_instrucciones(self): # Panel instrucciones
        self.limpiar_panel()
        Instrucciones(self.panel_principal, self)

    def mostrar_proyecto2(self): # Panel acerca de: detector de color
        self.limpiar_panel()
        Proyecto2(self.panel_principal, self)

    def mostrar_proyecto3(self): # Panel acerca de: posicionar flechas
        self.limpiar_panel()
        Proyecto3(self.panel_principal, self)

    def mostrar_resolver(self): # Panel algoritmo de detección
        self.limpiar_panel()
        Resolver(self.panel_principal, self)

    def mostrar_resolver2(self, cad): # Panel algoritmo de solución
        self.limpiar_panel()
        Resolver2(self.panel_principal, self, cad)

    def mostrar_movimientos(self): # Panel movimientos: explicación
        self.limpiar_panel()
        Movimientos(self.panel_principal, self)

    def mostrar_movimientos2(self): # Panel movimientos: imágenes
        self.limpiar_panel()
        Movimientos2(self.panel_principal, self)

    def limpiar_panel(self): # Limpiar paneles
        for widget in self.panel_principal.winfo_children():
            widget.destroy()

