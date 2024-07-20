import tkinter as tk
from tkinter import Label, Button
from tkinter.ttk import Combobox
from tkinter import filedialog
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import ttk
import cv2
import numpy as np
import util.util_imagenes as util_img 
import magiccube
from magiccube.solver.basic.basic_solver import BasicSolver
import mediapipe as mp
import time
from logica.funcionesCV2 import f

flag3=True
# Define el ángulo de rotación en grados
anguloU = 0  
anguloUU = 180  
anguloR = 90  
anguloRR = 270  
anguloU = 0  
anguloUU = 180  
anguloL = 270  
anguloLL = 90  
anguloD = 0
anguloDD = 180 
anguloB = -30
anguloBB = 30
noPasos=0
start_time = time.time()
tiempo=3
texto=""
contInicio = 0
contFinal = 5
condicionF=False
flag2=True
imagen = cv2.imread("formularios/flechita.png", cv2.IMREAD_UNCHANGED)
imagen360 = cv2.imread("formularios/flecha360.png", cv2.IMREAD_UNCHANGED)
imagenCurv = cv2.imread("formularios/flechaCurv.png", cv2.IMREAD_UNCHANGED)
numContador = 5
texto3 =""
textoFinal = "FELICIDADES"


class Resolver2: # Clase para resolver el cubo Rubik
    
    def __init__(self, panel_principal, controlador, cadena_cubo): # Constructor
        self.panel_principal = panel_principal
        self.cadena_cubo=cadena_cubo
        self.controlador = controlador
        self.fondo = util_img.leer_imagen("./imagenes/fondo.png", (1300, 850)) 

        self.bg_label = tk.Label(self.panel_principal, image=self.fondo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.bg_label.image = self.fondo 
        
        self.barra_menu=tk.Frame(panel_principal, bg="#800080")
        self.barra_menu.pack(side=tk.TOP, fill=tk.X, expand=False)

        self.combo_var = tk.StringVar()

        #print("cadena CUBO",cadena_cubo)
        self.componentes()

    def componentes(self):
 
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
       self.frame_label.place(x=120, y=75) 

       self.label_combo = tk.Label(self.panel_principal, text="Velocidad de transición de los pasos:", font=("Roboto", 13), bg="#1EAB1E")
       self.label_combo.config(fg="#FFFFFF", font=("Roboto", 15))
       self.label_combo.place(x=980, y=75)

       # Combo Box Tiempo
       self.combo_box = ttk.Combobox(self.panel_principal, textvariable=self.combo_var, font=("Roboto", 13))
       self.combo_box['values'] = ("2 Segundos", "3 Segundos", "5 Segundos")
       self.combo_box.place(x=1020, y=125)
       self.combo_box.bind("<<ComboboxSelected>>", self.funcion_combo)

       # Botón Ant
       self.botonInicio = tk.Button(self.panel_principal, text="Comenzar", bg="#1C7FAC", fg="#FFFFFF", font=("Roboto", 13), height=1)
       self.botonInicio.place(x=1070, y=210)
       self.botonInicio.bind("<Button-1>", self.funcion_botonInicio)

       self.botonSig = tk.Button(self.panel_principal, text=">>", bg="#EC3C24", fg="#FFFFFF", font=("Roboto", 13), height=1)
       self.botonSig.place(x=750, y=635)
       self.botonSig.bind("<Button-1>", self.funcion_botonSig)

       self.botonAnt = tk.Button(self.panel_principal, text="<< ", bg="#1EAB1E", fg="#FFFFFF", font=("Roboto", 13), height=1)
       self.botonAnt.place(x=350, y=635)
       self.botonAnt.bind("<Button-1>", self.funcion_botonAnt)

    def funcion_boton1(self, event): # evento - movimientos
        self.controlador.mostrar_movimientos()

    def funcion_boton2(self, event): # evento - algoritmo
        self.controlador.mostrar_resolver()

    def funcion_boton4(self, event): # evento - acerca del proyecto
        self.controlador.mostrar_proyecto2()

    def funcion_boton5(self, event): # evento - instrucciones
        self.controlador.mostrar_instrucciones()

    def funcion_botonAnt(self, event): # evento - instrucciones
        print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaah     anterior")
        global noPasos
        if(noPasos > 0):
                noPasos -= 1 
        self.textito()

    def funcion_botonSig(self, event): # evento - movimientos
        print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaah     siguiente")
        global noPasos
        if(noPasos < len(self.pasos)-1):
                noPasos += 1    #Sig paso
        self.textito()


    def funcion_combo(self, event):
        global tiempo
        seleccion = self.combo_var.get()
        if seleccion == "2 Segundos":
            print("Seleccionado: 2 segundos")
            tiempo=2
            # Aquí puedes llamar a la función correspondiente para 2 segundos
        elif seleccion == "3 Segundos":
            print("Seleccionado: 3 segundos")
            tiempo=3
            # Aquí puedes llamar a la función correspondiente para 3 segundos
        elif seleccion == "5 Segundos":
            print("Seleccionado: 5 segundos")
            tiempo=5
            # Aquí puedes llamar a la función correspondiente para 5 segundos

    def funcion_botonInicio(self, event): # Iniciar
        self.obtenerSolucion()
        self.iniciar()

    def obtenerSolucion(self):
        self.cubo = self.crearCubo()
        self.pasos = self.resolver(self.cubo)
        print(self.pasos)

    def crearCubo(self):
        self.cube = magiccube.Cube(3,self.cadena_cubo)
        print(self.cube)
        return self.cube

    def resolver(self, cubo):
        solver = BasicSolver(cubo)
        steps = solver.solve()

        self.arreglo=[]
        for step in steps:
            cadena = str(step)
            self.arreglo.append(cadena)
        print("pasooooooooooooooooooos:",len(self.arreglo))
        return self.arreglo

    def iniciar(self): # Inicia la captura de video
        self.mostrar_video()
    
    def textito(self):
        global texto
        global contInicio
        global contFinal
        global condicionF
        if len(texto)<5:
            for i in range(contInicio,contFinal):
                texto += self.pasos[i] + " "
        elif noPasos == contFinal:
            texto = ""
            contInicio = contFinal
            contFinal += 5
            if contFinal >= len(self.pasos):
                residuo = (contFinal - len(self.pasos)) 
                contFinal= contFinal - residuo
        elif noPasos < contInicio:
            texto = ""
            contInicio -= 5
            contFinal -= 5
        if noPasos == len(self.pasos)-1:
            condicionF=True
           


            
    def mostrar_video(self): # Algoritmo
        global flag2
        
        # Si es la primera cara que se detecta:
        if flag2:
            print(len(self.pasos))
            messagebox.showinfo("Armar el Cubo :)", "Para armar el cubo manten la cara con el CENTRO VERDE frente a ti, y que el CENTRO AMARILLO quede ARRIBA")
            flag2=False  
            
        # Define el ángulo de rotación en grados
        anguloU = 0  
        anguloUU = 180  
        anguloR = 90  
        anguloRR = 270  
        anguloU = 0  
        anguloUU = 180  
        anguloL = 270  
        anguloLL = 90  
        anguloD = 0
        anguloDD = 180 
        anguloB = -30
        anguloBB = 30
        global noPasos, image, imagen360, imagenCurv

        # Lee la imagen de la flecha con el canal alfa

        #imagen = cv2.imread("formularios/flechita.png", cv2.IMREAD_UNCHANGED)
        #imagen360 = cv2.imread("formularios/flecha360.png", cv2.IMREAD_UNCHANGED)
        #imagenCurv = cv2.imread("formularios/flechaCurv.png", cv2.IMREAD_UNCHANGED)

        global texto
        posicion = (200, 400)
        fuente = cv2.FONT_HERSHEY_SIMPLEX
        escala_fuente = 1.2
        color = (0, 0, 255)
        grosor = 3
        global contInicio
        global contFinal
        global tiempo


        texto2= ""
        posicion2 = (50, 50)
        fuente2 = cv2.FONT_HERSHEY_SIMPLEX
        escala_fuente2 = 2
        color2 = (0, 0, 255)
        grosor2 = 5

        global texto3
        posicion3 = (250, 250)
        fuente3 = cv2.FONT_HERSHEY_SIMPLEX
        escala_fuente3 = 5
        color3 = (0, 0, 255)
        grosor3 = 10

        posicionF= (30, 250)
        fuenteF = cv2.FONT_HERSHEY_SIMPLEX
        escala_fuenteF = 3
        colorF = (0, 255, 255)
        grosorF = 8

        global numContador
        global start_time
        global flag3
        global condicionF

        if flag3:
            self.cap = cv2.VideoCapture(3) 
            flag3=False

            
        # Inicializar MediaPipe Hands y el dibujador de resultados
        mp_hands = mp.solutions.hands
        mp_drawing = mp.solutions.drawing_utils

        #self.cap = cv2.VideoCapture(0) 
    
        with mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as hands:

            pas = self.pasos[noPasos]
            # Captura un fotograma de la cámara.
            ret, frame = self.cap.read()
            
            if  ret:
                
                # Convertir la imagen a RGB
                #frame=f.f_BGRaRGB(frame)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # Voltear la imagen horizontalmente para una vista tipo espejo (opcional)
                #frame = cv2.flip(frame, 1)

                # Procesar la imagen y detectar manos
                results = hands.process(frame)

                # Convertir de nuevo la imagen a BGR
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                #frame=f.f_RGBaBGR(frame)

                x_min=40
                x_max=150
                y_min=40
                y_max=150
                # Dibujar las anotaciones de las manos
                if results.multi_hand_landmarks:
                    # Lista para almacenar las coordenadas de los puntos finales de los dedos
                    finger_tips = []

                    for hand_landmarks in results.multi_hand_landmarks:
                        for index in [4, 8, 12, 16, 20]:  # Índices de los puntos finales de los dedos
                            landmark = hand_landmarks.landmark[index]
                            h, w, _ = frame.shape
                            x, y = int(landmark.x * w), int(landmark.y * h)
                            finger_tips.append((x, y))
                        
                        #mp_drawing.draw_landmarks(
                            #frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                    # Calcular el rectángulo que encierra todos los puntos finales de los dedos
                    if finger_tips:
                        x_min = min([coord[0] for coord in finger_tips])
                        y_min = min([coord[1] for coord in finger_tips])
                        x_max = max([coord[0] for coord in finger_tips])
                        y_max = max([coord[1] for coord in finger_tips])

                        # Ajustar los límites para que no salgan de la imagen
                        x_min = max(0, x_min)
                        y_min = max(0, y_min)
                        x_max = min(w, x_max)
                        y_max = min(h, y_max)

                        

                        # Recortar la imagen alrededor de los puntos finales de los dedos
                        cropped_image = frame[y_min:y_max, x_min:x_max]

                        # Mostrar la imagen recortada
                        #cv2.imshow('Cropped Fingers', cropped_image)

                # Mostrar la imagen procesada original con anotaciones
                #cv2.imshow('MediaPipe Hands', frame)
                texto2 = str(noPasos) + ":" + self.pasos[noPasos] 
                cv2.putText(frame, texto2, posicion2, fuente2, escala_fuente2, color2, grosor2)
                cv2.putText(frame, texto3, posicion3, fuente3, escala_fuente3, color3, grosor3)

                self.textito()
                cv2.putText(frame, texto, posicion, fuente, escala_fuente, color, grosor)
                if condicionF:
                    cv2.putText(frame, textoFinal, posicionF, fuenteF, escala_fuenteF, colorF, grosorF)


                # Escala la imagen de la flecha al mismo ancho que el fotograma
                tamamaX = x_max - x_min
                tamamaY = y_max - y_min
                redimenX = tamamaX/3
                redimenY = tamamaY/3

                #imagenRedi = cv2.resize(imagen, (tamamaX, tamamaY))
                #imagenRediCurv = cv2.resize(imagenCurv, (tamamaX, tamamaY))
                #imagenRediCurv360 = cv2.resize(imagen360, (tamamaX, tamamaY))
                imagenRedi = imagen
                imagenRediCurv = imagenCurv
                imagenRediCurv360 = imagen360

                centro = (imagenRedi.shape[1] // 2, imagenRedi.shape[0] // 2)
                centroCurv = (imagenRediCurv.shape[1] // 2, imagenRediCurv.shape[0] // 2)
                

                if pas == "R":
                    M = cv2.getRotationMatrix2D(centro, anguloR, 1.0)
                    imagenRedi = cv2.warpAffine(imagen, M, (imagenRedi.shape[1], imagenRedi.shape[0]))
                    otraFrame = frame[y_min: y_max, x_max - int(redimenX):x_max]
                    imagenRedi = cv2.resize(imagenRedi, (int(redimenX), tamamaY))
                    minY=y_min
                    maxY=y_max
                    minX=x_max - int(redimenX)
                    maxX=x_max
                    print("R")
                elif pas == "R'":
                    otraFrame = frame[y_min: y_max, x_max - int(redimenX):x_max]
                    # Obtén la matriz de rotación
                    M = cv2.getRotationMatrix2D(centro, anguloRR, 1.0)
                    # Aplica la rotación a la imagen de la flecha
                    imagenRedi = cv2.warpAffine(imagenRedi, M, (imagenRedi.shape[1], imagenRedi.shape[0]))
                    imagenRedi = cv2.resize(imagenRedi, (int(redimenX), tamamaY))
                    minY=y_min
                    maxY=y_max
                    minX=x_max - int(redimenX)
                    maxX=x_max
                    print("R'")
                elif pas == "U'":
                    otraFrame = frame[y_min:y_min+int(redimenY), x_min:x_max]
                    # Obtén la matriz de rotación
                    M = cv2.getRotationMatrix2D(centro, anguloU, 1.0)
                    # Aplica la rotación a la imagen de la flecha
                    imagenRedi = cv2.warpAffine(imagen, M, (imagenRedi.shape[1], imagenRedi.shape[0]))
                    imagenRedi = cv2.resize(imagenRedi, (tamamaX, int(redimenY)))
                    minY=y_min
                    maxY=y_min+int(redimenY)
                    minX=x_min
                    maxX=x_max
                    print("U'")
                elif pas == "U":
                    otraFrame = frame[y_min:y_min+int(redimenY), x_min:x_max]
                    # Obtén la matriz de rotación
                    M = cv2.getRotationMatrix2D(centro, anguloUU, 1.0)
                    # Aplica la rotación a la imagen de la flecha
                    imagenRedi = cv2.warpAffine(imagenRedi, M, (imagenRedi.shape[1], imagenRedi.shape[0]))
                    imagenRedi = cv2.resize(imagenRedi, (tamamaX, int(redimenY)))
                    minY=y_min
                    maxY=y_min+int(redimenY)
                    minX=x_min
                    maxX=x_max
                    print("U")
                elif pas == "L":
                    # Obtén la matriz de rotación
                    M = cv2.getRotationMatrix2D(centro, anguloL, 1.0)
                    # Aplica la rotación a la imagen de la flecha
                    imagenRedi = cv2.warpAffine(imagen, M, (imagenRedi.shape[1], imagenRedi.shape[0]))
                    otraFrame = frame[y_min : y_max, x_min : int(x_min+redimenX)]
                    imagenRedi = cv2.resize(imagenRedi, (int(redimenX),tamamaY))
                    minY=y_min
                    maxY=y_max
                    minX=x_min
                    maxX=int(x_min+redimenX)
                    
                    print("L")
                elif pas == "L'":
                    otraFrame = frame[y_min : y_max, x_min : int(x_min+redimenX)]
                    # Obtén la matriz de rotación
                    M = cv2.getRotationMatrix2D(centro, anguloLL, 1.0)
                    # Aplica la rotación a la imagen de la flecha
                    imagenRedi = cv2.warpAffine(imagenRedi, M, (imagenRedi.shape[1], imagenRedi.shape[0]))
                    imagenRedi = cv2.resize(imagenRedi, (int(redimenX),tamamaY))
                    minY=y_min
                    maxY=y_max
                    minX=x_min
                    maxX=int(x_min+redimenX)
                    print("L'")
                elif pas == "D":
                    otraFrame = frame[y_max - int(redimenY): y_max, x_min : x_max]
                    # Obtén la matriz de rotación
                    M = cv2.getRotationMatrix2D(centro, anguloD, 1.0)
                    # Aplica la rotación a la imagen de la flecha
                    imagenRedi = cv2.warpAffine(imagenRedi, M, (imagenRedi.shape[1], imagenRedi.shape[0]))
                    imagenRedi = cv2.resize(imagenRedi, (tamamaX,int(redimenY)))
                    minY=y_max - int(redimenY)
                    maxY=y_max
                    minX=x_min
                    maxX=x_max
                    print("D")
                elif pas == "D'":
                    otraFrame = frame[y_max - int(redimenY): y_max, x_min : x_max]
                    # Obtén la matriz de rotación
                    M = cv2.getRotationMatrix2D(centro, anguloDD, 1.0)
                    # Aplica la rotación a la imagen de la flecha
                    imagenRedi = cv2.warpAffine(imagenRedi, M, (imagenRedi.shape[1], imagenRedi.shape[0]))
                    imagenRedi = cv2.resize(imagenRedi, (tamamaX,int(redimenY)))
                    minY=y_max - int(redimenY)
                    maxY=y_max
                    minX=x_min
                    maxX=x_max
                    print("D'")
                elif pas == "F":
                    otraFrame = frame[y_min:y_max, x_min : x_max]
                    imagenRedi = imagen360
                    imagenRedi = cv2.resize(imagenRedi, (tamamaX,tamamaY))
                    minY=y_min
                    maxY=y_max
                    minX=x_min
                    maxX=x_max            
                    print("F")
                elif pas == "F'":
                    otraFrame = frame[y_min:y_max, x_min : x_max]
                    # Aplica la rotación a la imagen de la flecha
                    imagenRedi = cv2.flip(imagenRediCurv360, 1)
                    imagenRedi = cv2.resize(imagenRedi, (tamamaX,tamamaY))
                    minY=y_min
                    maxY=y_max
                    minX=x_min
                    maxX=x_max
                    print("F'")
                elif pas == "B":
                    otraFrame = frame[y_min-50:y_min+int(redimenY), x_min : x_max]
                    imagenRedi = imagenRediCurv
                    M = cv2.getRotationMatrix2D(centro, anguloBB, 1.0)
                    # Aplica la rotación a la imagen de la flecha
                    imagenRedi = cv2.warpAffine(imagenRedi, M, (imagenRedi.shape[1], imagenRedi.shape[0]))
                    imagenRedi = cv2.resize(imagenRedi, (tamamaX,int(redimenY)+50))
                    minY=y_min-50
                    maxY=y_min+int(redimenY)
                    minX=x_min
                    maxX=x_max
                    print("B")
                elif pas == "B'":
                    otraFrame = frame[y_min-50:y_min+int(redimenY), x_min : x_max]
                    # Aplica la rotación a la imagen de la flecha
                    imagenRedi = cv2.flip(imagenRediCurv, 1)
                    M = cv2.getRotationMatrix2D(centro, anguloB, 1.0)
                    # Aplica la rotación a la imagen de la flecha
                    imagenRedi = cv2.warpAffine(imagenRedi, M, (imagenRedi.shape[1], imagenRedi.shape[0]))
                    imagenRedi = cv2.resize(imagenRedi, (tamamaX,int(redimenY)+50))
                    minY=y_min-50
                    maxY=y_min+int(redimenY)
                    minX=x_min
                    maxX=x_max
                    print("B'")
                
                # Extrae el canal alfa (máscara) y crea su inverso
                mask = imagenRedi[:, :, 3]
                maskIn = cv2.bitwise_not(mask)
                #maskIn = f.f_bitwise_not(mask)

                # Redimensiona la máscara inversa para que coincida con las dimensiones de otraFrame

                try:
                    maskIn = cv2.resize(maskIn, (otraFrame.shape[1], otraFrame.shape[0]))
                    # Aplica la máscara a imagenRedi y a otraFrame
                    maskAnd = cv2.bitwise_and(imagenRedi, imagenRedi, mask=mask)
                    frameMasked = cv2.bitwise_and(otraFrame, otraFrame, mask=maskIn)
                    #maskAnd = f.f_bitwise_and(imagenRedi, imagenRedi, mask)
                    #frameMasked = f.f_bitwise_and(otraFrame, otraFrame, maskIn)
                    result = cv2.add(maskAnd[:, :, 0:3], frameMasked)
                    #result = f.f_add(maskAnd[:, :, 0:3], frameMasked)
                    # Asegúrate de que las dimensiones coincidan
                    if (maxY - minY) == result.shape[0] and (maxX - minX) == result.shape[1]:
                        frame[minY:maxY, minX:maxX] = result
                    else:
                        print(f"Dimensiones incompatibles: región del frame ({maxY - minY}, {maxX - minX}) vs result {result.shape}")

                except cv2.error as e:
                    print("Error al redimensionar la imagen:", e)
                

                # Combina maskAnd y frameMasked_resized
                

                # Redimensiona la máscara inversa para que coincida con las dimensiones de otraFrame
        


                

                # Muestra el fotograma resultante
                #cv2.imshow("frame", frame)

                # Espera la pulsación de la tecla 'Esc' para salir del bucle
                #c = cv2.waitKey(1)

                # Verificar si han pasado 5 segundos
                if noPasos < len(self.pasos)-1:
                    if numContador == 0 :
                        texto3=""
                        if time.time() - start_time >= tiempo :
                            noPasos += 1
                            start_time = time.time()  # Reiniciar el temporizador

                    else:
                        if time.time() - start_time >= 1 :
                            texto3 = str(numContador)
                            numContador -= 1
                            start_time = time.time()  # Reiniciar el temporizador
                        

                
                
                #cv2.imshow("s", frame)
                
            
            
            # Conversión del frame principal por compatibilidad con tkinter
            frame = cv2.resize(frame, (830, 530))
            #frame = f.f_resize(frame, 830, 530)
            img = cv2.imencode('.ppm', frame)[1].tobytes()
            imgtk = tk.PhotoImage(data=img)

            self.frame_label.imgtk = imgtk 
            self.frame_label.configure(image=imgtk)

            # Actualización constante del video
        self.frame_label.after(10, self.mostrar_video)
            
                    
