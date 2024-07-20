import cv2
import numpy as np

class f(): # Funciones de OpenCV sin OpenCV  xd

    def f_THRESH_OTSU(canal): # cv2.THRESH_OTSU
        # Umbralización automática
        
        # Hacer histograma
        histograma, _ = np.histogram(canal.flatten(), 256, [0, 256])
        totalPixeles=canal.size
        
        varianzaMax, umbral = 0, 0
        sumaTotal, sumaPixelesFondo, sumaPixelesCubo = 0, 0, 0
        frecuenciaPixelesFondo, frecuenciaPixelesCubo = 0, 0
        
        for i in range(256):
            sumaTotal += i*histograma[i]

        # Se calcula cada umbral posible
        for i in range(256):
            frecuenciaPixelesFondo+=histograma[i]
            if frecuenciaPixelesFondo==0:
                continue
            frecuenciaPixelesCubo=totalPixeles-frecuenciaPixelesFondo
            if frecuenciaPixelesCubo==0:
                break
            
            sumaPixelesFondo+=i*histograma[i]
            sumaPixelesCubo=sumaTotal-sumaPixelesFondo
            
            mediaPixelesFondo=sumaPixelesFondo/frecuenciaPixelesFondo
            mediaPixelesCubo=sumaPixelesCubo/frecuenciaPixelesCubo
            
            varianzaEntreClases=frecuenciaPixelesFondo*frecuenciaPixelesCubo * (mediaPixelesFondo-mediaPixelesCubo) ** 2
            
            # Se selecciona el umbral óptimo
            if varianzaEntreClases > varianzaMax:
                varianzaMax=varianzaEntreClases
                umbral=i
                
        return umbral

    def f_threshold(canal, umbral): # cv2.threshold / cv2.THRESH_BINARY

        imgBinaria=np.where(canal > umbral, 255, 0).astype(np.uint8)
        return imgBinaria

    def BGRaHSV(imagenBGR): # cv2.COLOR_BGR2HSV
        B=imagenBGR[:,:,0]
        G=imagenBGR[:,:,1]
        R=imagenBGR[:,:,2]

        R_norm = R / 255.0
        G_norm = G / 255.0
        B_norm = B / 255.0
        
        Cmax=np.maximum(R_norm, np.maximum(G_norm, B_norm))
        Cmin=np.minimum(R_norm, np.minimum(G_norm, B_norm))
        delta=Cmax-Cmin

        V=Cmax

        # Epsilon para evitar errores de división entre cero
        epsilon=1e-10

        S=np.where(Cmax != 0, delta / (Cmax + epsilon), 0)
        H=np.zeros_like(S)

        mask_R=(Cmax==R_norm) & (delta!=0)
        mask_G=(Cmax==G_norm) & (delta!=0)
        mask_B=(Cmax==B_norm) & (delta!=0)

        H[mask_R] = 60 * ((G_norm[mask_R] - B_norm[mask_R]) / (delta[mask_R] + epsilon) % 6)
        H[mask_G] = 60 * ((B_norm[mask_G] - R_norm[mask_G]) / (delta[mask_G] + epsilon) + 2)
        H[mask_B] = 60 * ((R_norm[mask_B] - G_norm[mask_B]) / (delta[mask_B] + epsilon) + 4)

        # Normalizar H (0-179)
        escalarH = (H % 360) / 2 
        
        imagenHSV=np.dstack((escalarH, S*255, V*255)).astype(np.uint8)
        
        return imagenHSV

    def f_add(image1, image2): # cv2.add

        # Sumar  pixel a pixel
        imagenSuma=np.clip(image1.astype(np.int32) + image2.astype(np.int32), 0, 255).astype(np.uint8)
        return imagenSuma

    def f_inRange(frame, rangoInf, rangoSup): # cv2.inRange
        # Umbralización por rangos
        if len(frame.shape)==3:  # Imagen a color 
            # Aplica la máscara a cada canal
            mascara=np.all((frame >= rangoInf) & (frame <= rangoSup), axis=2)
        elif len(frame.shape) == 2:  # Imagen en gris
            mascara=(frame >= rangoInf) & (frame <= rangoSup)

        # Convertir la máscara lógica a una máscara binaria (0 o 255)
        mascara = mascara.astype(np.uint8) * 255

        return mascara

    def f_boundingRect(contorno): # cv2.boundingRect
        # Encuentra el cuadrado delimitador del contorno
        contorno=np.array(contorno)
        minX=np.min(contorno[:, 0, 0])
        minY=np.min(contorno[:, 0, 1])
        maxX=np.max(contorno[:, 0, 0])
        maxY=np.max(contorno[:, 0, 1])

        # Calcular el ancho y la altura del rectángulo que lo delimita
        anchoR=maxX-minX
        altoR=maxY-minY
        return minX, minY, anchoR, altoR

    def f_arcLength(contorno, cerrado): # cv2.arcLength
        # Calcula el perimetro del contorno (cuadrado)
        length=0
        # Se recorren los pixeles adyacentes
        for i in range(len(contorno)):
            p1=contorno[i][0]
            p2=contorno[(i+1) % len(contorno)][0]
            # Se calcula la distancia euclidiana de los puntos (perimetro)
            length+=np.linalg.norm(np.array(p1)-np.array(p2))
        return length

    def f_contourArea(contorno): # cv2.contourArea
        # Calcula el área del contorno (cuadrado) con la fórmula del polígono de Shoelace (fórmula de Gauss).
        area=0
        # Se recorren los pixeles adyacentes
        for i in range(len(contorno)):
            x1, y1=contorno[i][0]
            x2, y2=contorno[(i+1) % len(contorno)][0]
            # S calcula la contribución de cada par de puntos al área total del polígono con la fórmula de Shoelace
            area+= x1*y2 - x2*y1
        return abs(area)/2.0

    def f_BGRaRGB(frame): # cv2.COLOR_BGR2RGB
        B=frame[:, :, 0]
        G=frame[:, :, 1]
        R=frame[:, :, 2]
        
        frameRGB = np.stack([R, G, B], axis=2)
        return frameRGB

    def f_RGBaBGR(frameRGB): # cv2.COLOR_RGB2BGR
        B1=frameRGB[:, :, 2]
        G1=frameRGB[:, :, 1]
        R1=frameRGB[:, :, 0]

        frameBGR = np.stack([B1, G1, R1], axis=2)
        return frameBGR

    def f_BGRaGRAY(frame): # cv2.COLOR_BGR2GRAY
        B=frame[:, :, 0] 
        G=frame[:, :, 1] 
        R=frame[:, :, 2]

        gris= 0.114 * B + 0.587 * G + 0.299 * R
        gris=gris.astype(np.uint8)
        return gris

    def f_GRAYaRGB(frameGris): # cv2.COLOR_GRAY2RGB
        frameRGB = np.stack((frameGris,) * 3, axis=-1)
        return frameRGB

    def f_resize(cuadro, anchoNew, alturaNew): # cv2.resize
        altura, ancho, canales = cuadro.shape
        ratioX = np.linspace(0, ancho - 1, anchoNew)
        ratioY = np.linspace(0, altura - 1, alturaNew)

        vecinosInfX = np.floor(ratioX).astype(np.int32)
        vecinosInfY = np.floor(ratioY).astype(np.int32)
        vecinosSupX = np.ceil(ratioX).astype(np.int32)
        vecinosSupY = np.ceil(ratioY).astype(np.int32)

        pesoInfX=ratioX-vecinosInfX
        pesoInfY=ratioY-vecinosInfY

        pesoSupX=1-pesoInfX
        pesoSupY=1-pesoInfY

        imagenRZ=np.zeros((alturaNew, anchoNew, canales), dtype=np.uint8)

        for c in range(canales):
            # Obtener los valores de los vecinos en las cuatro esquinas
            esquinaSupIzq = cuadro[vecinosInfY[:, None], vecinosInfX, c]
            esquinaSupDer = cuadro[vecinosInfY[:, None], vecinosSupX, c]
            esquinaInfIzq = cuadro[vecinosSupY[:, None], vecinosInfX, c]
            esquinaInfDer = cuadro[vecinosSupY[:, None], vecinosSupX, c]

            # Interpolación en X
            sup = esquinaSupIzq * pesoSupX + esquinaSupDer * pesoInfX
            inf = esquinaInfIzq * pesoSupX + esquinaInfDer * pesoInfX

            # Interpolación en Y
            imagenRZ[:, :, c] = sup*pesoSupY[:, None] + inf*pesoInfY[:, None]

        return imagenRZ

    def f_bitwise_not(frame): # cv2.bitwise_not
        imagenInvertida = 255-frame
        return imagenInvertida

    def f_bitwise_and(imagen1, imagen2, mascara): # cv2.bitwise_and
        mascaraBinaria=mascara.astype(bool)
        imagenAND=np.zeros_like(imagen1)
        imagenAND[mascaraBinaria] = np.bitwise_and(imagen1[mascaraBinaria], imagen2[mascaraBinaria])
        return imagenAND

    def f_getRotationMatrix2D(centro, angulo): # cv2.getRotationMatrix2D
        anguloRad = math.radians(angulo)
        cx, cy = centro
        # Calcular las componentes de la matriz de rotación
        cos_theta = math.cos(anguloRad)
        sin_theta = math.sin(anguloRad)
        # Construir la matriz de rotación 2x3
        matrizRotacion=np.array([
            [cos_theta, -sin_theta, cx * (1-cos_theta) + cy * sin_theta],
            [sin_theta, cos_theta, cy * (1-cos_theta) - cx * sin_theta]
        ])
        return matrizRotacion

    def f_warpAffine(frame, M, ancho, altura): # cv2.warpAffine
        # Imagen de salida
        y_indices, x_indices = np.indices((altura, ancho))
        # Aplanar las matrices de coordenadas y agregar una dimensión para realizar la multiplicación de matrices
        x_flat = x_indices.ravel()
        y_flat = y_indices.ravel()
        ones = np.ones_like(x_flat)
        coords_flat = np.vstack((x_flat, y_flat, ones))
        # Multiplicar matrices
        coords_rotado_flat = M.dot(coords_flat)
        # Descomprimir las coordenadas a sus dimensiones originales
        x_rotado = coords_rotado_flat[0].reshape((altura, ancho)).astype(int)
        y_rotado = coords_rotado_flat[1].reshape((altura, ancho)).astype(int)
        # Crear una imagen vacía con las mismas dimensiones que la imagen de entrada
        imagen_rotada = np.zeros_like(frame)
        # Sólo los índices válidos (del mismo tamaño)
        validID = (0 <= x_rotado) & (x_rotado < ancho) & (0 <= y_rotado) & (y_rotado < altura)
        imagen_rotada[validID] = frame[y_rotado[validID], x_rotado[validID]]
        return imagen_rotada

    



















