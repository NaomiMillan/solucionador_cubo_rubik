import magiccube
from magiccube.solver.basic.basic_solver import BasicSolver
import cv2
import numpy as np
import mediapipe as mp
import time

def crearCubo():
    cube = magiccube.Cube(3,"YYYYYYYYYRRRRRRRRRGGGGGGGGGOOOOOOOOOBBBBBBBBBWWWWWWWWW")
    #cube = magiccube.Cube(3,"YYYYYYYYYRRRRRRWRRGGGGGWGGWOOOBOOOOBBBBBBBWORWWGWWGBWO")
    print(cube)
    return cube

def rotarCubo(cubo, instrucciones):
    cubo.rotate(instrucciones)
    print(cubo)

def resolver(cubo):
    # Resolver el cubo 3x3x3
    solver = BasicSolver(cubo)
    #Guardar los pasos
    steps = solver.solve()

    arreglo=[]
    for step in steps:
        cadena = str(step)
        arreglo.append(cadena)
    return arreglo

def darPasos(cubo, pasos):
    contador=0
    for mov in pasos:
        print("paso: ",contador,mov)  
        cubo.rotate(mov)
        print(cubo)
        contador=contador+1



cubo = crearCubo()
instrucciones="F R L B R L"
rotarCubo(cubo,instrucciones)
pasos = resolver(cubo)

start_time = time.time()


# Inicializar MediaPipe Hands y el dibujador de resultados
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Inicia la captura de video desde la cámara.
cap = cv2.VideoCapture(1)

# Lee la imagen de la flecha con el canal alfa
imagen = cv2.imread("flechita.png", cv2.IMREAD_UNCHANGED)
imagen360 = cv2.imread("flecha360.png", cv2.IMREAD_UNCHANGED)
imagenCurv = cv2.imread("flechaCurv.png", cv2.IMREAD_UNCHANGED)

# Define el ángulo de rotación en grados
anguloU = 0  # Puedes cambiar este valor al ángulo deseado
anguloUU = 180  # Puedes cambiar este valor al ángulo deseado
anguloR = 90  # Puedes cambiar este valor al ángulo deseado
anguloRR = 270  # Puedes cambiar este valor al ángulo deseado
anguloU = 0  # Puedes cambiar este valor al ángulo deseado
anguloUU = 180  # Puedes cambiar este valor al ángulo deseado
anguloL = 270  # Puedes cambiar este valor al ángulo deseado
anguloLL = 90  # Puedes cambiar este valor al ángulo deseado
anguloD = 0
anguloDD = 180 
anguloB = -30
anguloBB = 30
noPasos=0

texto= ""
posicion = (200, 400)
fuente = cv2.FONT_HERSHEY_SIMPLEX
escala_fuente = 1.2
color = (0, 0, 255)
grosor = 3
contInicio = 0
contFinal = 5


texto2= ""
posicion2 = (50, 50)
fuente2 = cv2.FONT_HERSHEY_SIMPLEX
escala_fuente2 = 2
color2 = (0, 0, 255)
grosor2 = 5
contInicio2 = 0
contFinal2 = 5

with mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:

    while True:
        pas = pasos[noPasos]
        # Captura un fotograma de la cámara.
        ret, frame = cap.read()
        if not ret:
            print("Ignorando frame vacío de la cámara.")
            continue

        # Convertir la imagen a RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Voltear la imagen horizontalmente para una vista tipo espejo (opcional)
        #frame = cv2.flip(frame, 1)

        # Procesar la imagen y detectar manos
        results = hands.process(frame)

        # Convertir de nuevo la imagen a BGR
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

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




        if len(texto)<5:
            for i in range(contInicio,contFinal):
                texto += pasos[i] + " "

        elif noPasos == contFinal:
            texto = ""
            contInicio = contFinal
            contFinal += 5
            if noPasos > len(pasos):
                contFinal = contFinal - len(pasos)
        


        cv2.putText(frame, texto, posicion, fuente, escala_fuente, color, grosor)


        texto2 = str(noPasos) + ":" + pasos[noPasos] 


        cv2.putText(frame, texto2, posicion2, fuente2, escala_fuente2, color2, grosor2)

        # Escala la imagen de la flecha al mismo ancho que el fotograma
        tamamaX = x_max - x_min
        tamamaY = y_max - y_min
        redimenX = tamamaX/3
        redimenY = tamamaY/3
        imagenRedi = cv2.resize(imagen, (tamamaX, tamamaY))
        imagenRediCurv = cv2.resize(imagenCurv, (tamamaX, tamamaY))
        imagenRediCurv360 = cv2.resize(imagen360, (tamamaX, tamamaY))

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

        # Redimensiona la máscara inversa para que coincida con las dimensiones de otraFrame
        try:
            maskIn = cv2.resize(maskIn, (otraFrame.shape[1], otraFrame.shape[0]))
            # Aplica la máscara a imagenRedi y a otraFrame
            maskAnd = cv2.bitwise_and(imagenRedi, imagenRedi, mask=mask)
            frameMasked = cv2.bitwise_and(otraFrame, otraFrame, mask=maskIn)
        except cv2.error as e:
            print("Error al redimensionar la imagen:", e)



        # Combina maskAnd y frameMasked_resized
        result = cv2.add(maskAnd[:, :, 0:3], frameMasked)


        # Asegúrate de que las dimensiones coincidan
        if (maxY - minY) == result.shape[0] and (maxX - minX) == result.shape[1]:
            frame[minY:maxY, minX:maxX] = result
        else:
            print(f"Dimensiones incompatibles: región del frame ({maxY - minY}, {maxX - minX}) vs result {result.shape}")
            print(result.shape[0])
            print(result.shape[1])

        frame = cv2.resize(frame, (1200, 700))

        # Muestra el fotograma resultante
        cv2.imshow("frame", frame)

        # Espera la pulsación de la tecla 'Esc' para salir del bucle
        c = cv2.waitKey(1)

        # Verificar si han pasado 5 segundos
        if noPasos < len(pasos)-1:
            if time.time() - start_time >= 1 :
                noPasos += 1
                print(f"Incremento automático: {noPasos}")
                start_time = time.time()  # Reiniciar el temporizador
        if(noPasos == len(pasos)):
            break
        if c == 27:
            break
        elif c == 115:  # Tecla 's'
            if(noPasos < len(pasos)-1):
                noPasos += 1    #Sig paso
            else:
                break
        elif c == 97:  # Tecla 'a'
            if(noPasos > 0):
                noPasos -= 1    #Paso anterior
            
print("fin")

# Libera la captura de video y cierra todas las ventanas.
cap.release()
cv2.destroyAllWindows()
