import tkinter as tk

# Variable global para almacenar la tecla presionada
current_key = None

# Función para manejar el evento de pulsación de teclas
def on_key_press(event):
    global current_key
    current_key = event.keysym
    print(f"Tecla presionada: {current_key}")

# Función para evaluar la tecla presionada
def evaluate_key():
    global current_key
    if current_key:
        print(f"Evaluando tecla: {current_key}")
        if current_key == 'e':
            print("Se ha presionado la tecla 'e'")
        else:
            print("No se ha presionado la tecla 'e'")
    else:
        print("No hay tecla presionada actualmente")

# Crear la ventana principal de Tkinter
root = tk.Tk()
root.title("Captura de Teclas con Tkinter en un Panel")

# Crear un frame dentro de la ventana principal
frame = tk.Frame(root, width=400, height=300, bg="lightgrey")
frame.pack_propagate(False)  # Evitar que el frame cambie de tamaño
frame.pack()

# Configurar el frame para que capture eventos de teclado
frame.bind("<KeyPress>", on_key_press)
frame.focus_set()  # Asegurar que el frame tiene el foco para capturar eventos de teclado

# Etiqueta para indicar dónde capturar las teclas
label = tk.Label(frame, text="Presiona cualquier tecla", bg="lightgrey")
label.pack(pady=20)

# Botón para evaluar la tecla presionada
button = tk.Button(frame, text="Evaluar tecla", command=evaluate_key)
button.pack(pady=20)

# Iniciar el bucle principal de la ventana
root.mainloop()
