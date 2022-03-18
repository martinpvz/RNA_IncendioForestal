from ast import For
from copyreg import constructor
from hashlib import new
from msilib.schema import Class
from tkinter import *
from tkinter import filedialog
from PIL import Image
from PIL import ImageTk
import cv2
import imutils
import numpy as np
import os

instanciasImagen = []

class Instancia:
  def __init__(self, x, y) -> None:
    self.clase = "N"
    self.valorX = x
    self.valorY = y


def guardar_datos():
  file = open("./datos/etiquetado.txt", "a")
  for instancia in instanciasImagen:
    file.write(instancia.clase + "\n")
  file.write(os.linesep)
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
        global image

        # Leer la imagen de entrada y la redimensionamos
        image = cv2.imread(path_image)
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
            instanciasImagen.append(Instancia(xPos, yPos))
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
        print(xLeft)
        print(yLeft)
        xInstancia = int(xLeft/10)
        yInstancia = int(yLeft/10)
        #izquierdo humo
        for instancia in instanciasImagen:
          if instancia.valorX == xInstancia and instancia.valorY == yInstancia:
            instancia.clase = "H"
            print(instancia.clase, instancia.valorX, instancia.valorY)


    if event == cv2.EVENT_RBUTTONDOWN:
        cv2.circle(imagen,(x,y),1,(0,0,255),2)
        xRight = x
        yRight = y
        print(xRight)
        print(yRight)
        #derecho incendio
        xInstancia = int(xRight/10)
        yInstancia = int(yRight/10)
        for instancia in instanciasImagen:
          if instancia.valorX == xInstancia and instancia.valorY == yInstancia:
            instancia.clase = "I"
            print(instancia.clase, instancia.valorX, instancia.valorY)


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
