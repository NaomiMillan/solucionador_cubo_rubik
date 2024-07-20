import tkinter as tk
from tkinter import font
import util.util_imagenes as util_img
from formularios.form_control import Controlador

class FormularioDesign2(tk.Tk): # Página de Inicio
    
    def __init__(self): # Constructor
        super().__init__()
        self.logo = util_img.leer_imagen("./imagenes/i4R.png", (1364, 750))
        self.config_window()
        self.paneles()
        self.control_cuerpo()
        
    def config_window(self): # Configuración de la ventana (tamaño, icono, etc.)
        self.title('Rubik Solver')
        self.iconbitmap("./imagenes/ic.ico")
        w, h = 1300, 850
        self.geometry(f"{w}x{h}")
      
    def paneles(self): # Panel
        self.cuerpo_principal = tk.Frame(
            self, bg="#000000", width=150)
        self.cuerpo_principal.pack(side=tk.RIGHT, fill='both', expand=True)
        
    def control_cuerpo(self): # Posicionar Componentes
        label = tk.Label(self.cuerpo_principal, image=self.logo, bg="#000000")
        label.place(x=0, y=0, relwidth=1, relheight=1)

        self.button = tk.Button(self.cuerpo_principal, text="Iniciar", command=self.on_button_click, bg='#26272A', fg='white', font=('Helvetica', 10, 'bold'))
        self.button.place(relx=0.5, rely=0.85, anchor='center', width=100, height=35)
        
    def limpiar_panel(self, panel): # Limpiar panel
        for widget in panel.winfo_children():
            widget.destroy()

    def on_button_click(self): # Evento del botón
        self.limpiar_panel(self.cuerpo_principal)
        Controlador(self.cuerpo_principal)
        

# Ejecutar 
if __name__ == "__main__":
    app = FormularioDesign2()
    app.mainloop()
    
