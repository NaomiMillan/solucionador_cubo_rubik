import tkinter as tk
from tkinter import Label, Button
from tkinter.ttk import Combobox
from tkinter import filedialog
from tkinter import messagebox
from tkinter import simpledialog
import cv2
import numpy as np
import statistics
import util.util_imagenes as util_img 
from logica.funcionesCV2 import f

# Variables auxiliares
nivelBinB, nivelBinG, nivelBinR = 0, 0, 0
flag, flag2, mensaje = True, True, 0

# Listas para cada cuadro 
cuadro1 = []
cuadro2 = []
cuadro3 = []
cuadro4 = []
cuadro5 = []
cuadro6 = []
cuadro7 = []
cuadro8 = []
cuadro9 = []

# Listas para almacenar el cubo
cuboDesorden = []
cuboOrden = [None,None,None,None, None, None]
cuboString = ""

# Mapa para colores detectados
colores_label={
            0: "#E6DB2F",  # amarillo
            1: "#1EAB1E",  # verde
            2: "#F17824",   # naranja
            3: "#2240DA",  # azul
            4: "#EE0603",  # rojo 
            5: "#FFFFFF"  # blanco
        }

# Rangos de colores en HSV 
azulB=np.array([100,100,20], np.uint8)
azulA=np.array([125,255,255], np.uint8)

amarilloB=np.array([16,100,20], np.uint8)
amarilloA=np.array([30,255,255], np.uint8)

verdeB=np.array([40,50,0], np.uint8)
verdeA=np.array([70,255,255], np.uint8)

blancoB=np.array([0,0,0], np.uint8)
blancoA=np.array([179,49,255], np.uint8)

rojoB1=np.array([170,150,0], np.uint8)
rojoA1=np.array([179,255,255], np.uint8)
rojoB2 = np.array([0, 100, 0], np.uint8)
rojoA2 = np.array([0, 255, 255], np.uint8)

naranjaB1 = np.array([3, 100, 100], np.uint8)
naranjaA1 = np.array([15, 255, 255], np.uint8)

# Funciones auxiliares

def limpiar(): # Limpia las listas de los cuadros en cada iteración 
    cuadro1.clear()
    cuadro2.clear()
    cuadro3.clear()
    cuadro4.clear()
    cuadro5.clear()
    cuadro6.clear()
    cuadro7.clear()
    cuadro8.clear()
    cuadro9.clear()

def asociar(claveColor): # Asocia la clave de color en número a la letra de su color correspondiente
    match claveColor:
        case 0: #Y
            return "Y"
        case 1: #G
            return "G"
        case 2: #O
            return "O"
        case 3: #B
            return "B"
        case 4: #R
            return "R"
        case 5: #W
            return "W"

def trackBarB(val): # Actualizar valor de la trakbar azul
    global nivelBinB
    nivelBinB = val

def trackBarG(val): # Actualizar valor de la trakbar verde
    global nivelBinG
    nivelBinG = val

def trackBarR(val): # Actualizar valor de la trakbar roja
    global nivelBinR
    nivelBinR = val

# Función principal

def detectar(mascara, color, framePam, color2, xi, yi, intervalos, clave, frame2): # Detecta el color en cada cuadro
    # Para identificar a que cuadrante pertenece
    for i, (intervaloX, intervaloY) in enumerate(intervalos):
        if intervaloX[0]<=xi<intervaloX[1] and intervaloY[0]<=yi<intervaloY[1]:
            cuad=i+1

    # Muestra el color de cada cuadro
    contornos, _ = cv2.findContours(mascara, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for c in contornos:
        area = cv2.contourArea(c)
        if area>1000:
            cv2.putText(frame2, color2, (xi, yi), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
            # Guarda el color detectado en su cuadrante (lista de cuadros)
            match cuad:
                case 1:
                    cuadro1.append(clave)
                case 2:
                    cuadro2.append(clave)
                case 3:
                    cuadro3.append(clave)
                case 4:
                    cuadro4.append(clave)
                case 5:
                    cuadro5.append(clave)
                case 6:
                    cuadro6.append(clave)
                case 7:
                    cuadro7.append(clave)
                case 8:
                    cuadro8.append(clave)
                case 9:
                    cuadro9.append(clave)

class Resolver: # Clase para detectar los colores del cubo Rubik
    
    def __init__(self, panel_principal, controlador): # Constructor
        self.panel_principal = panel_principal
        self.controlador = controlador
        self.fondo = util_img.leer_imagen("./imagenes/fondo.png", (1300, 850)) 

        self.bg_label = tk.Label(self.panel_principal, image=self.fondo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.bg_label.image = self.fondo 
        
        self.barra_menu=tk.Frame(panel_principal, bg="#800080")
        self.barra_menu.pack(side=tk.TOP, fill=tk.X, expand=False)

        self.panel_cubo=tk.Frame(panel_principal, bg="#0F0404")
        self.panel_cubo.place(x=175, y=480, width=205, height=200)

        self.componentes()
        self.iniciar()
           
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
       
       # Label para el video principal (frame)
       self.frame_label = tk.Label(self.panel_principal)
       self.frame_label.place(x=150, y=40) 

       # ------------------------------------------------------------------------------------------------------
       # Panel y labels para mostrar los colores detectados

       self.frameCubo_label = tk.Label(self.panel_principal)
       self.frameCubo_label.place(x=480, y=440)  

       self.labelCol=tk.Label(self.panel_principal, text="Colores detectados", bg="#F17824")
       self.labelCol.config(fg="#FFFFFF", font=("Roboto", 15))
       self.labelCol.place(x=185, y=440)

       self.labelC1=tk.Label(self.panel_cubo, text="OII", bg="#0F0404") 
       self.labelC1.config(fg="#0F0404", font=("Roboto", 26))
       self.labelC1.place(x=10, y=10)

       self.labelC2=tk.Label(self.panel_cubo, text="OII", bg="#0F0404") 
       self.labelC2.config(fg="#0F0404", font=("Roboto", 26))
       self.labelC2.place(x=75, y=10)

       self.labelC3=tk.Label(self.panel_cubo, text="OII", bg="#0F0404") 
       self.labelC3.config(fg="#0F0404", font=("Roboto", 26))
       self.labelC3.place(x=140, y=10)

       self.labelC4=tk.Label(self.panel_cubo, text="OII", bg="#0F0404") 
       self.labelC4.config(fg="#0F0404", font=("Roboto", 26))
       self.labelC4.place(x=10, y=75)

       self.labelC5=tk.Label(self.panel_cubo, text="OII", bg="#0F0404") 
       self.labelC5.config(fg="#0F0404", font=("Roboto", 26))
       self.labelC5.place(x=75, y=75)

       self.labelC6=tk.Label(self.panel_cubo, text="OII", bg="#0F0404") 
       self.labelC6.config(fg="#0F0404", font=("Roboto", 26))
       self.labelC6.place(x=140, y=75)

       self.labelC7=tk.Label(self.panel_cubo, text="OII", bg="#0F0404") 
       self.labelC7.config(fg="#0F0404", font=("Roboto", 26))
       self.labelC7.place(x=10, y=140)

       self.labelC8=tk.Label(self.panel_cubo, text="OII", bg="#0F0404") 
       self.labelC8.config(fg="#0F0404", font=("Roboto", 26))
       self.labelC8.place(x=75, y=140)

       self.labelC9=tk.Label(self.panel_cubo, text="OII", bg="#0F0404")
       self.labelC9.config(fg="#0F0404", font=("Roboto", 26))
       self.labelC9.place(x=140, y=140)

       # ------------------------------------------------------------------------------------------------------

       # Label para los videos con imagenes binarizadas (R, G, B)

       self.binB_label = tk.Label(self.panel_principal)
       self.binB_label.place(x=840, y=40)

       self.binG_label = tk.Label(self.panel_principal)
       self.binG_label.place(x=840, y=263)

       self.binR_label = tk.Label(self.panel_principal)
       self.binR_label.place(x=840, y=490)

       # Texto y trackbar para cada imágen binarizada (R, G, B)

       self.labelB=tk.Label(self.panel_principal, text="Plano Azul", bg="#2240DA")
       self.labelB.config(fg="#FFFFFF", font=("Roboto", 15))
       self.labelB.place(x=1090, y=50)

       self.labelG=tk.Label(self.panel_principal, text="Plano Verde", bg="#1EAB1E")
       self.labelG.config(fg="#FFFFFF", font=("Roboto", 15))
       self.labelG.place(x=1090, y=273)

       self.labelR=tk.Label(self.panel_principal, text="Plano Rojo", bg="#EC3C24")
       self.labelR.config(fg="#FFFFFF", font=("Roboto", 15))
       self.labelR.place(x=1090, y=500)

       self.trackbarB = tk.Scale(self.panel_principal, from_=0, to=255, orient=tk.HORIZONTAL, label='Umbral Azul')
       self.trackbarB.set(nivelBinB)  
       self.trackbarB.place(x=1090, y=100)

       self.trackbarG = tk.Scale(self.panel_principal, from_=0, to=255, orient=tk.HORIZONTAL, label='Umbral Verde')
       self.trackbarG.set(nivelBinB) 
       self.trackbarG.place(x=1090, y=323)

       self.trackbarR = tk.Scale(self.panel_principal, from_=0, to=255, orient=tk.HORIZONTAL, label='Umbral Rojo')
       self.trackbarR.set(nivelBinB) 
       self.trackbarR.place(x=1090, y=550)

    def mostrarColores(self, arr): # Actualizar los label con los colores detectados
        global colores_label
        clave=arr[0]
        color=colores_label.get(clave, "#000000")
        self.labelC1.config(bg=color, fg=color)  

        clave1=arr[1]
        color1=colores_label.get(clave1, "#000000")
        self.labelC2.config(bg=color1, fg=color1)

        clave2=arr[2]
        color2=colores_label.get(clave2, "#000000")
        self.labelC3.config(bg=color2, fg=color2)

        clave3=arr[3]
        color3=colores_label.get(clave3, "#000000")
        self.labelC4.config(bg=color3, fg=color3)

        clave4=arr[4]
        color4=colores_label.get(clave4, "#000000")
        self.labelC5.config(bg=color4, fg=color4)

        clave5=arr[5]
        color5=colores_label.get(clave5, "#000000")
        self.labelC6.config(bg=color5, fg=color5)

        clave6=arr[6]
        color6=colores_label.get(clave6, "#000000")
        self.labelC7.config(bg=color6, fg=color6)

        clave7=arr[7]
        color7=colores_label.get(clave7, "#000000")
        self.labelC8.config(bg=color7, fg=color7)

        clave8=arr[8]
        color8=colores_label.get(clave8, "#000000")
        self.labelC9.config(bg=color8, fg=color8) 

    def borrarColores(self): # Reiniciar los label en negro
        self.labelC1.config(bg="#0F0404", fg="#0F0404")
        self.labelC2.config(bg="#0F0404", fg="#0F0404")
        self.labelC3.config(bg="#0F0404", fg="#0F0404")
        self.labelC4.config(bg="#0F0404", fg="#0F0404")
        self.labelC5.config(bg="#0F0404", fg="#0F0404")
        self.labelC6.config(bg="#0F0404", fg="#0F0404")
        self.labelC7.config(bg="#0F0404", fg="#0F0404")
        self.labelC8.config(bg="#0F0404", fg="#0F0404")
        self.labelC9.config(bg="#0F0404", fg="#0F0404")

    def funcion_boton1(self, event): # evento - movimientos
        self.controlador.mostrar_movimientos()

    def funcion_boton2(self, event): # evento - algoritmo
        pass
        
    def funcion_boton4(self, event): # evento - acerca del proyecto
        self.controlador.mostrar_proyecto2()

    def funcion_boton5(self, event): # evento - instrucciones
        self.controlador.mostrar_instrucciones()

    def iniciar(self): # Inicia la captura de video
        self.cap = cv2.VideoCapture(3) 
        self.mostrar_video()

    def mostrar_video(self): # Algoritmo
        global nivelBinB, nivelBinG, nivelBinR, flag, flag2, mensaje, cuboString, cuboDesorden, cuboOrden

        # Si es la primera cara que se detecta:
        if mensaje == 0 and flag2:
            messagebox.showinfo("Comienza la Detección", "Primero muestra la cara con el CENTRO VERDE, y que el CENTRO AMARILLO quede ARRIBA")
            flag2=False  
        # Si se han detectado los colores de todas las caras:
        if mensaje == 6:
            cuboString = ""
            messagebox.showinfo("Detección Completada", "Todos los colores han sido detectados correctamente.")
            # Ordena las caras del cubo de acuerdo con el orden del algoritmo
            
            for cara in cuboDesorden:
                centro=cara[4]
                match centro:
                    case 0: #Y
                        cuboOrden[0]=cara
                    case 1: #G
                        cuboOrden[2]=cara
                    case 2: #O
                        cuboOrden[3]=cara
                    case 3: #B
                        cuboOrden[4]=cara
                    case 4: #R
                        cuboOrden[1]=cara
                    case 5: #W
                        cuboOrden[5]=cara
                
            # Devuelve la cadena con los colores detectados en el formato necesario para el algoritmo
            try:
                for cara in cuboOrden:
                    for color in cara:
                        colorSTR=asociar(color)
                        cuboString+=colorSTR
            except TypeError as e:
                tk.messagebox.showinfo("Error", "Escaneaste una cara de forma incorrecta, ya que hay centros repetidos.\n Inicia de nuevo")
                limpiar()
                self.borrarColores()
                nivelBinB, nivelBinG, nivelBinR = 0, 0, 0
                flag, flag2, mensaje = True, True, 0
                cuboDesorden = []
                cuboOrden = [None,None,None,None, None, None]
                print("limpiando error")
                self.controlador.mostrar_resolver()


            #print("cubo orden: ",cuboOrden)
            #print("cubo desorden: ",cuboDesorden)
            print("CUBO: ",cuboString)
            
            limpiar()
            self.borrarColores()
            nivelBinB, nivelBinG, nivelBinR = 0, 0, 0
            flag, flag2, mensaje = True, True, 0
            cuboDesorden = []
            cuboOrden = [None,None,None,None, None, None]
            

            # Se abre el panel para la segunda parte del algoritmo
            self.controlador.mostrar_resolver2(cuboString)
            return

        ret, frame = self.cap.read()
        if ret:

            # Marcar un cuadrado en el centro de la pantalla
            alto, ancho, _ = frame.shape
            esquina1 = ancho // 2 - 125
            esquina2 = alto // 2 - 125
            esquina3 = ancho // 2 + 125
            esquina4 = alto // 2 + 125

            cv2.rectangle(frame, (esquina1, esquina2), (esquina3, esquina4), (0, 255, 0), 2)
            cv2.putText(frame, 'Centra el cubo aqui:', (esquina1, esquina2 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
            frameCubo = frame[esquina2:esquina4, esquina1:esquina3]

            # Separa por canales R, G, B el frame del cubo
            b = frameCubo[:, :, 0]
            g = frameCubo[:, :, 1]
            r = frameCubo[:, :, 2]

            # Al inicio aplica una umbralización automática OTSU a cada canal
            if flag:
                umbralOtsuB = f.f_THRESH_OTSU(b)
                umbralOtsuG = f.f_THRESH_OTSU(g)
                umbralOtsuR = f.f_THRESH_OTSU(r)
                
                nivelBinB = int(umbralOtsuB)
                nivelBinG = int(umbralOtsuG)
                nivelBinR = int(umbralOtsuR)

                self.trackbarB.set(nivelBinB)
                self.trackbarG.set(nivelBinG)
                self.trackbarR.set(nivelBinR)

                flag = False

            # Se actualiza el nivel de umbralización con las trackbar
            nivelBinB=self.trackbarB.get()
            nivelBinG=self.trackbarG.get()
            nivelBinR=self.trackbarR.get()
        
            # Binarizar los canales con las trackbars
            binB = f.f_threshold(b, nivelBinB)
            binG = f.f_threshold(g, nivelBinG)
            binR = f.f_threshold(r, nivelBinR)

            # Convertir de gris a color para mostrarlo en la interfaz ************** FUNCION?
            binB1=f.f_GRAYaRGB(binB)
            binG1=f.f_GRAYaRGB(binG)
            binR1=f.f_GRAYaRGB(binR)

            # Conversión de los frames binarizados por compatibilidad con tkinter
            binB1=f.f_resize(binB1, 210, 210)
            img_binB = cv2.imencode('.ppm', binB1)[1].tobytes()
            imgtk_binB = tk.PhotoImage(data=img_binB)
            self.binB_label.imgtk = imgtk_binB
            self.binB_label.configure(image=imgtk_binB)

            binG1=f.f_resize(binG1, 210, 210)
            img_binG = cv2.imencode('.ppm', binG1)[1].tobytes()
            imgtk_binG = tk.PhotoImage(data=img_binG)
            self.binG_label.imgtk = imgtk_binG
            self.binG_label.configure(image=imgtk_binG)

            binR1=f.f_resize(binR1, 210, 210)
            img_binR = cv2.imencode('.ppm', binR1)[1].tobytes()
            imgtk_binR = tk.PhotoImage(data=img_binR)
            self.binR_label.imgtk = imgtk_binR
            self.binR_label.configure(image=imgtk_binR)

            # Buscar contornos en las imágenes binarizadas
            contornosB, _=cv2.findContours(binB, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            contornosG, _=cv2.findContours(binG, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            contornosR, _=cv2.findContours(binR, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            # Filtrar contornos que parezcan cuadrados, con un tamaño mínimo en cada canal
            cuadrados = []

            # Detectar cuadrados en canal azul
            for contorno in contornosB:
                perim = f.f_arcLength(contorno, True)
                epsilon = 0.02 * perim
                approx = cv2.approxPolyDP(contorno, 0.02 * perim, True)

                if len(approx) == 4:
                    # Verificar que los ángulos entre los lados sean aproximadamente de 90 grados
                    angulos = []
                    for i in range(4):
                        p1 = approx[i][0]
                        p2 = approx[(i + 1) % 4][0]
                        p3 = approx[(i + 2) % 4][0]
                        v1 = np.array(p1) - np.array(p2)
                        v2 = np.array(p3) - np.array(p2)
                        productoPunto = np.dot(v1, v2)
                        productoNom = np.linalg.norm(v1) * np.linalg.norm(v2)
                        angulo = np.arccos(productoPunto / productoNom) * (180 / np.pi)
                        angulos.append(angulo)
                    if all(abs(angulo - 90) < 10 for angulo in angulos):
                        # Establecer un mínimo en el área del cuadrado
                        area = f.f_contourArea(approx)
                        if area>50 and area <7000:   
                            cuadrados.append(approx)

            # Detectar cuadrados en canal verde
            for contorno in contornosG:
                perim = f.f_arcLength(contorno, True)
                approx = cv2.approxPolyDP(contorno, 0.02 * perim, True)

                if len(approx) == 4:
                    # Verificar que los ángulos entre los lados sean aproximadamente de 90 grados
                    angulos = []
                    for i in range(4):
                        p1 = approx[i][0]
                        p2 = approx[(i + 1) % 4][0]
                        p3 = approx[(i + 2) % 4][0]
                        v1 = np.array(p1) - np.array(p2)
                        v2 = np.array(p3) - np.array(p2)
                        productoPunto = np.dot(v1, v2)
                        productoNom = np.linalg.norm(v1) * np.linalg.norm(v2)
                        angulo = np.arccos(productoPunto / productoNom) * (180 / np.pi)
                        angulos.append(angulo)
                    if all(abs(angulo - 90) < 10 for angulo in angulos):
                        # Establecer un mínimo en el área del cuadrado
                        area = f.f_contourArea(approx)
                        if area>50 and area <7000:    
                            cuadrados.append(approx)

            # Detectar cuadrados en canal rojo
            for contorno in contornosR:
                perim = f.f_arcLength(contorno, True)
                approx = cv2.approxPolyDP(contorno, 0.02 * perim, True)

                if len(approx) == 4:
                    # Verificar que los ángulos entre los lados sean aproximadamente de 90 grados
                    angulos = []
                    for i in range(4):
                        p1 = approx[i][0]
                        p2 = approx[(i + 1) % 4][0]
                        p3 = approx[(i + 2) % 4][0]
                        v1 = np.array(p1) - np.array(p2)
                        v2 = np.array(p3) - np.array(p2)
                        productoPunto = np.dot(v1, v2)
                        productoNom = np.linalg.norm(v1) * np.linalg.norm(v2)
                        angulo = np.arccos(productoPunto / productoNom) * (180 / np.pi)
                        angulos.append(angulo)
                    if all(abs(angulo - 90) < 10 for angulo in angulos):
                        # Establecer un mínimo en el área del cuadrado
                        area = f.f_contourArea(approx)
                        if area>50 and area <7000:   
                            cuadrados.append(approx)
            
            # Se crea el frame para la detección de color y para dibujar los cuadrados
            frame2 = frameCubo.copy()
            alto, ancho, _ = frame2.shape
            alto1 = alto/3
            alto2 = alto1*2
            ancho1 = ancho/3
            ancho2 = ancho1*2

            # Se establecen intervalos del frame2 para determinar los cuadrantes
            intervalos = [
                ((0, ancho1), (0, alto1)),   # Cuadro 1
                ((ancho1, ancho2), (0, alto1)), # Cuadro 2
                ((ancho2, ancho), (0, alto1)), # Cuadro 3
                ((0, ancho1), (alto1, alto2)),   # Cuadro 4
                ((ancho1, ancho2), (alto1, alto2)), # Cuadro 5
                ((ancho2, ancho), (alto1, alto2)), # Cuadro 6
                ((0, ancho1), (alto2, alto)),   # Cuadro 7
                ((ancho1, ancho2), (alto2, alto)), # Cuadro 8
                ((ancho2, ancho), (alto2, alto)), # Cuadro 9
            ]

            # Detectar el color en cada cuadro
            for cuadrado in cuadrados:
                # Dibujar los cuadrados en el frame
                cv2.drawContours(frame2, [cuadrado], -1, (0, 0, 0), 3)
                x, y, w, h = f.f_boundingRect(cuadrado)

                # Crear frameX con las mismas dimensiones que el cuadrado
                frameX = frameCubo[y:y + h, x:x + w]
                vx = int(x + (w / 2))
                vy = int(y + (h / 2))
                
                # Detectar color del frame
                frameHSV = f.BGRaHSV(frameX)
                maskAzul =f.f_inRange(frameHSV, azulB, azulA)
                maskAmarillo =f.f_inRange(frameHSV, amarilloB, amarilloA)
                maskRed1 =f.f_inRange(frameHSV, rojoB1, rojoA1)
                maskRed2 =f.f_inRange(frameHSV, rojoB2, rojoA2)
                maskRed = f.f_add(maskRed1, maskRed2)
                maskVerde =f.f_inRange(frameHSV, verdeB, verdeA)
                maskBlanco =f.f_inRange(frameHSV, blancoB, blancoA)
                maskNaranja =f.f_inRange(frameHSV, naranjaB1, naranjaA1)
                detectar(maskAmarillo, (0, 255, 255), frameX, "amarillo", vx, vy, intervalos, 0, frame2)
                detectar(maskVerde, (0, 255, 0), frameX, "verde", vx, vy, intervalos, 1, frame2)
                detectar(maskNaranja, (0, 128, 255), frameX, "naranja", vx, vy, intervalos, 2, frame2)
                detectar(maskAzul, (255, 0, 0), frameX, "azul", vx, vy, intervalos, 3, frame2)
                detectar(maskRed, (0, 0, 255), frameX, "rojo", vx, vy, intervalos, 4, frame2)
                detectar(maskBlanco, (0, 0, 0), frameX, "blanco", vx, vy, intervalos, 5, frame2)

            # Hasta que se detecte n veces el color en cada cuadro se puede pasar a la siguiente cara
            cuadros_completados = all([len(cuadro) > 50 for cuadro in [cuadro1, cuadro2, cuadro3, cuadro4, cuadro5, cuadro6, cuadro7, cuadro8, cuadro9]])
            
            if cuadros_completados:
                root = tk.Tk()
                root.withdraw()

                # Calcular la moda de cada lista de cuadros para saber cuál es el color predominante (detectado más veces)
                cuadro1Arr = np.array(cuadro1)
                modaC1 = statistics.mode(cuadro1)

                cuadro2Arr = np.array(cuadro2)
                modaC2 = statistics.mode(cuadro2)

                cuadro3Arr = np.array(cuadro3)
                modaC3 = statistics.mode(cuadro3)

                cuadro4Arr = np.array(cuadro4)
                modaC4 = statistics.mode(cuadro4)

                cuadro5Arr = np.array(cuadro5)
                modaC5 = statistics.mode(cuadro5)

                cuadro6Arr = np.array(cuadro6)
                modaC6 = statistics.mode(cuadro6)

                cuadro7Arr = np.array(cuadro7)
                modaC7 = statistics.mode(cuadro7)

                cuadro8Arr = np.array(cuadro8)
                modaC8 = statistics.mode(cuadro8)

                cuadro9Arr = np.array(cuadro9)
                modaC9 = statistics.mode(cuadro9)


                # Mostrar los colores detectados en el panel
                self.mostrarColores([modaC1, modaC2, modaC3, modaC4, modaC5, modaC6, modaC7, modaC8, modaC9 ])
                
                # Verificar si la detección fue correcta
                valor = simpledialog.askinteger("Confirmación", "Ingresa: \n0. Si la deteccion es correcta. \n1. Para hacerla de nuevo                                 ")
                if valor==1:
                    tk.messagebox.showinfo("Intentalo de nuevo", "Escanea la misma cara")
                else:
                    # Agregar los colores detectados a una cara del cubo
                    cuboDesorden.append([modaC1, modaC2, modaC3, modaC4, modaC5, modaC6, modaC7, modaC8, modaC9 ])
                    print([modaC1, modaC2, modaC3, modaC4, modaC5, modaC6, modaC7, modaC8, modaC9 ])

                    # Controlar el orden de ingresar caras 
                    mensaje = mensaje+1
                    if mensaje==1:
                        messagebox.showinfo("Detección Completada", "Todos los colores han sido detectados.\n\nAhora muestra la cara con el CENTRO NARANJA, y que el CENTRO AMARILLO quede ARRIBA")
                    if mensaje==2:
                        messagebox.showinfo("Detección Completada", "Todos los colores han sido detectados.\n\nAhora muestra la cara con el CENTRO AZUL, y que el CENTRO AMARILLO quede ARRIBA")
                    if mensaje==3:
                        messagebox.showinfo("Detección Completada", "Todos los colores han sido detectados.\n\nAhora muestra la cara con el CENTRO ROJO, y que el CENTRO AMARILLO quede ARRIBA")
                    if mensaje==4:
                        messagebox.showinfo("Detección Completada", "Todos los colores han sido detectados.\n\nAhora muestra la cara con el CENTRO AMARILLO, y que el CENTRO AZUL quede ARRIBA")
                    if mensaje==5:
                        messagebox.showinfo("Detección Completada", "Todos los colores han sido detectados.\n\nAhora muestra la cara con el CENTRO BLANCO, y que el CENTRO VERDE quede ARRIBA")
                
                cuadros_completados=False
                limpiar()
                self.borrarColores()

            # Conversión del frame con la detección de color por compatibilidad con tkinter
            frameCubo=f.f_resize(frame2, 250, 250)
            img_cubo = cv2.imencode('.ppm', frameCubo)[1].tobytes()
            imgtk_cubo = tk.PhotoImage(data=img_cubo)
            self.frameCubo_label.imgtk = imgtk_cubo
            self.frameCubo_label.configure(image=imgtk_cubo)
            
        # Conversión del frame principal por compatibilidad con tkinter
        frame=f.f_resize(frame, 540, 390)
        img = cv2.imencode('.ppm', frame)[1].tobytes()
        imgtk = tk.PhotoImage(data=img)
        self.frame_label.imgtk = imgtk 
        self.frame_label.configure(image=imgtk)

        # Actualización constante del video
        self.frame_label.after(10, self.mostrar_video)

            