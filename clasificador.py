from ast import For, While
# from asyncio.windows_events import NULL
# from asyncio.windows_events import NULL
from copyreg import constructor
from email.mime import base
from hashlib import new
# from msilib.schema import Class
from skimage.feature import graycomatrix, graycoprops
from scipy.stats import entropy
from skimage import io, color, img_as_ubyte
from statistics import median
from tkinter import *
from tkinter import filedialog
from PIL import Image
from PIL import ImageTk
import cv2
import imutils
import numpy as np
import os

instanciasImagen = []
image = []

class Instancia:
  def __init__(self, x, y, media, desviacion, contraste, disimilaridad, homogeneiedad, energia, correlacion, entropia) -> None:
    self.clase = "N"
    self.valorX = x
    self.valorY = y
    self.mediaR = media[0]
    self.mediaG = media[1]
    self.mediaB = media[2]
    self.desviacionR = desviacion[0]
    self.desviacionG = desviacion[1]
    self.desviacionB = desviacion[2]
    self.contraste0 = contraste[0]
    self.contraste45 = contraste[1]
    self.contraste90 = contraste[2]
    self.contraste135 = contraste[3]
    self.dissimilarity0 = disimilaridad[0]
    self.dissimilarity45 = disimilaridad[1]
    self.dissimilarity90 = disimilaridad[2]
    self.dissimilarity135 = disimilaridad[3]
    self.homogeneidad0 = homogeneiedad[0]
    self.homogeneidad45 = homogeneiedad[1]
    self.homogeneidad90 = homogeneiedad[2]
    self.homogeneidad135 = homogeneiedad[3]
    self.energia0 = energia[0]
    self.energia45 = energia[1]
    self.energia90 = energia[2]
    self.energia135 = energia[3]
    self.correlacion0 = correlacion[0]
    self.correlacion45 = correlacion[1]
    self.correlacion90 = correlacion[2]
    self.correlacion135 = correlacion[3]
    self.entropia = entropia

def obtenerDesviacion(xInstancia, yInstancia):
  valorTotalR = []
  valorTotalG = []
  valorTotalB = []
  xPixel = xInstancia*10
  yPixel = yInstancia*10
  filas = xPixel
  columnas = yPixel
  while filas < xPixel+10:
    while columnas < yPixel+10:
      (b, g, r) = image[filas, columnas]
      # print("Pixel at ({}, {}) - Red: {}, Green: {}, Blue: {}".format(filas,columnas,r,g, b))
      valorTotalR.append(r)
      valorTotalG.append(g)
      valorTotalB.append(b)
      columnas += 1
    if columnas >= yPixel+10:
      columnas = yPixel
    filas+=1
  desviacionR = round(np.std(valorTotalR),4)
  desviacionG = round(np.std(valorTotalG),4)
  desviacionB = round(np.std(valorTotalB),4)
  return (desviacionR, desviacionG, desviacionB)

def obtenerMedia(xInstancia,yInstancia):
  valorTotalR = []
  valorTotalG = []
  valorTotalB = []
  xPixel = xInstancia*10
  yPixel = yInstancia*10
  filas = xPixel
  columnas = yPixel
  while filas < xPixel+10:
    while columnas < yPixel+10:
      (b, g, r) = image[filas, columnas]
      # print("Pixel at ({}, {}) - Red: {}, Green: {}, Blue: {}".format(filas,columnas,r,g, b))
      valorTotalR.append(r)
      valorTotalG.append(g)
      valorTotalB.append(b)
      columnas += 1
    if columnas >= yPixel+10:
      columnas = yPixel
    filas+=1
  mediaR = np.mean(valorTotalR)
  mediaG = np.mean(valorTotalG)
  mediaB = np.mean(valorTotalB)
  # print(mediaR, mediaG, mediaB)
  return (mediaR, mediaG, mediaB)

def obtener_matriz(y, x):
  global image
  imagePartition = image[y:y+10, x:x+10]
  gray = cv2.cvtColor(imagePartition, cv2.COLOR_BGR2GRAY)
  matrix_coocurrence = graycomatrix(gray, [1], [0, 45, 90, 135], levels=256, normed=True, symmetric=True)
  return matrix_coocurrence

def contrast_feature(matrix_coocurrence):
    contrast = graycoprops(matrix_coocurrence, 'contrast')
    return contrast[0]

def dissimilarity_feature(matrix_coocurrence):
    dissimilarity = graycoprops(matrix_coocurrence, 'dissimilarity')    
    return dissimilarity[0]

def homogeneity_feature(matrix_coocurrence):
    homogeneity = graycoprops(matrix_coocurrence, 'homogeneity')
    return homogeneity[0]

def energy_feature(matrix_coocurrence):
    energy = graycoprops(matrix_coocurrence, 'energy')
    return energy[0]

def asm_feature(matrix_coocurrence):
    asm = graycoprops(matrix_coocurrence, 'asm')
    return asm[0]

def correlation_feature(matrix_coocurrence):
    correlation = graycoprops(matrix_coocurrence, 'correlation')
    return correlation[0]

def entropy_feature(y,x):
  global image
  imagePartition = image[y:y+10, x:x+10]
  # entropia = entropy(gray, base=2)
  gray = cv2.cvtColor(imagePartition, cv2.COLOR_BGR2GRAY)
  glcm = np.squeeze(graycomatrix(gray, distances=[1], angles=[0], symmetric=True, normed=True))
  entropy = -np.sum(glcm*np.log2(glcm + (glcm==0)))
  return entropy

def guardar_datos():
  # Se guarda la información en el archivo
  file = open("./datos/etiquetado.txt", "a")
  for instancia in instanciasImagen:
    file.write(str(instancia.mediaR) + "," + str(instancia.mediaG)+ "," + str(instancia.mediaB) + "," + str(instancia.desviacionR) + "," + str(instancia.desviacionG) + "," + str(instancia.desviacionB) + "," + str(round(instancia.contraste0,4)) + "," + str(round(instancia.contraste45,4)) + "," + str(round(instancia.contraste90,4)) + "," + str(round(instancia.contraste135,4)) + "," + str(round(instancia.dissimilarity0,4)) + "," + str(round(instancia.dissimilarity45,4)) + "," + str(round(instancia.dissimilarity90,4)) + "," + str(round(instancia.dissimilarity135,4)) + "," + str(round(instancia.homogeneidad0,4)) + "," + str(round(instancia.homogeneidad45,4)) + "," + str(round(instancia.homogeneidad90,4)) + "," + str(round(instancia.homogeneidad135,4)) + "," + str(round(instancia.energia0,4)) + "," + str(round(instancia.energia45,4)) + "," + str(round(instancia.energia90,4)) + "," + str(round(instancia.energia135,4)) + "," + str(round(instancia.correlacion0,4)) + "," + str(round(instancia.correlacion45,4)) + "," + str(round(instancia.correlacion90,4)) + "," + str(round(instancia.correlacion135,4)) + "," + str(round(instancia.entropia, 4)) + "," + instancia.clase + "\n")
  file.close()
  # vaciar arreglo de instancias imagen
  instanciasImagen.clear()

def elegir_imagen():
    # Especificar los tipos de archivos, para elegir solo a las imágenes
    path_image = filedialog.askopenfilename(filetypes = [
        ("image", ".jpeg"),
        ("image", ".png"),
        ("image", ".jpg")])

    if len(path_image) > 0:
        # global image

        # Leer la imagen de entrada y la redimensionamos
        global image
        image = cv2.imread(path_image)
        imagePartition = image[0:10, 0:10]
        gray = cv2.cvtColor(imagePartition, cv2.COLOR_BGR2GRAY)
        glcm = np.squeeze(graycomatrix(gray, distances=[1], angles=[0,45,90,135], symmetric=True, normed=True))
        entropy = -np.sum(glcm*np.log2(glcm + (glcm==0)))
        # matrix = obtener_matriz(0,0)
        print(entropy)
        # print(dissimilarity_feature(matrix))
        # print(homogeneity_feature(matrix))
        # print(energy_feature(matrix))
        # print(correlation_feature(matrix))
        # image= imutils.resize(image, height=250)
        # Para visualizar la imagen de entrada en la GUI
        imageToShow= imutils.resize(image, width=150)
        imageToShow = cv2.cvtColor(imageToShow, cv2.COLOR_BGR2RGB)
        imageToShowTwo = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        im = Image.fromarray(imageToShow )
        img = ImageTk.PhotoImage(image=im)

        lblInputImage.configure(image=img)
        lblInputImage.image = img

        # Label IMAGEN DE ENTRADA
        lblInfo1 = Label(root, text="IMAGEN SELECCIONADA:")
        lblInfo1.grid(column=0, row=1, padx=5, pady=5)

        #---------------MIS MODIFICACIONES-----------------#
        # Visualizar la imagen a modificar
        # Para visualizar la imagen en lblOutputImage en la GUI
        green = (0, 255, 0)
        width = int(image.shape[1])
        incrementoX = int(width/25)
        height = int(image.shape[0])
        incrementoY = int(height/25)
        x = 0
        y = 0
        imageToShow3 = imageToShowTwo
        print(width)
        print(height)

        while( x <= width and y <= height ):
          x += incrementoX
          imageToShow3 = cv2.line(imageToShow3, (x, 0), (x, height), green)
          y += incrementoY
          imageToShow3 = cv2.line(imageToShow3, (0, y), (width, y), green)

        xPos = 0
        yPos = 0
        while( xPos < 25 ):
          while( yPos < 25 ):
            matriz = obtener_matriz(yPos*10, xPos*10)
            instanciasImagen.append(Instancia(xPos, yPos, obtenerMedia(xPos, yPos), obtenerDesviacion(xPos, yPos), contrast_feature(matriz), dissimilarity_feature(matriz), homogeneity_feature(matriz), energy_feature(matriz), correlation_feature(matriz), entropy_feature(yPos*10, xPos*10)))
            yPos += 1
          if yPos >= 24:
            yPos = 0
          xPos+= 1

        cv2.namedWindow('Imagen')
        cv2.setMouseCallback('Imagen',dibujando)
        global imagen
        imagen = cv2.cvtColor(imageToShow3, cv2.COLOR_BGR2RGB)
        while True:
          cv2.imshow('Imagen',imagen)
    
          k = cv2.waitKey(1) & 0xFF
          if k == ord('l'): # Limpiar el contenido de la imagen
            imagen = np.zeros((480,640,3),np.uint8)
          elif k == 27:
            break
        cv2.destroyAllWindows()
        # return imageToShow3



def dibujando(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.circle(imagen,(x,y),1,(255,255,255),2)
        xLeft = x
        yLeft = y
        xInstancia = int(xLeft/10)
        yInstancia = int(yLeft/10)
        #izquierdo humo
        for instancia in instanciasImagen:
          if instancia.valorX == xInstancia and instancia.valorY == yInstancia:
            instancia.clase = "H"
            # print(instancia.clase, instancia.valorX, instancia.valorY, instancia.pixelX, instancia.pixelY)


    if event == cv2.EVENT_RBUTTONDOWN:
        cv2.circle(imagen,(x,y),1,(0,0,255),2)
        xRight = x
        yRight = y
        #derecho incendio
        xInstancia = int(xRight/10)
        yInstancia = int(yRight/10)
        for instancia in instanciasImagen:
          if instancia.valorX == xInstancia and instancia.valorY == yInstancia:
            instancia.clase = "I"
            # print(instancia.clase, instancia.valorX, instancia.valorY, instancia.pixelX, instancia.pixelY)


root = Tk()

# Label donde se presentará la imagen de entrada
lblInputImage = Label(root)
lblInputImage.grid(column=0, row=2)

# Creamos el botón para elegir la imagen de entrada
btn = Button(root, text="Elegir imagen", width=25, command=elegir_imagen)
btn.grid(column=0, row=0, padx=5, pady=5)

# Creamos el botón para procesar la imagen
btnProcesar = Button(root, text="Procesar la imagen", width=25, command=guardar_datos)
btnProcesar.grid(column=0, row=3, padx=5, pady=5)

# Creamos el botón salir
btnProcesar = Button(root, text="Salir", width=25, command=root.destroy)
btnProcesar.grid(column=0, row=4, padx=5, pady=5)

root.mainloop()
