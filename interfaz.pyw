from tkinter import *
from tkinter import filedialog
from PIL import Image
from PIL import ImageTk
import cv2
import imutils
import numpy as np

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
        while( x <= width ):
          x += incrementoX
          imageToShow3 = cv2.line(imageToShow3, (x, 0), (x, height), green)
        while( y <= height ):
          y += incrementoY
          imageToShow3 = cv2.line(imageToShow3, (0, y), (width, y), green)
        # imageToShow3 = cv2.line(imageToShowTwo, (int(width/2), 0), (int(width/2), height), green)

        im = Image.fromarray(imageToShow3)
        img = ImageTk.PhotoImage(image=im)
        lblOutputImage.configure(image=img)
        lblOutputImage.image = img

        # Label IMAGEN DE SALIDA
        lblInfo3 = Label(root, text="IMAGEN A ANALIZAR:", font="bold")
        lblInfo3.grid(column=1, row=0, padx=5, pady=5)
        #----------------TERMINA--------------------------------#

        # Al momento que leemos la imagen de entrada, vaciamos
        # la iamgen de salida y se limpia la selección de los
        # radiobutton
        lblOutputImage.image = ""
        selected.set(0)

# Creamos la ventana principal
root = Tk()

# Label donde se presentará la imagen de entrada
lblInputImage = Label(root)
lblInputImage.grid(column=0, row=2)

# Label donde se presentará la imagen de salida
lblOutputImage = Label(root)
lblOutputImage.grid(column=1, row=1, rowspan=6)

# # Label ¿Qué color te gustaría resaltar?
# lblInfo2 = Label(root, text="¿Qué color te gustaría resaltar?", width=25)
# lblInfo2.grid(column=0, row=3, padx=5, pady=5)

# def deteccion_color():
#     global image
#     if selected.get() == 1:
#         # Rojo
#         rangoBajo1 = np.array([0, 140, 90], np.uint8)
#         rangoAlto1 = np.array([8, 255, 255], np.uint8)
#         rangoBajo2 = np.array([160, 140, 90], np.uint8)
#         rangoAlto2 = np.array([180, 255, 255], np.uint8)

#     if selected.get() == 2:
#         # Amarillo
#         rangoBajo = np.array([10, 98, 0], np.uint8)
#         rangoAlto = np.array([25, 255, 255], np.uint8)

#     if selected.get() == 3:
#         # Azul celeste
#         rangoBajo = np.array([88, 104, 121], np.uint8)
#         rangoAlto = np.array([99, 255, 243], np.uint8)
        
#     imageGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     imageGray = cv2.cvtColor(imageGray, cv2.COLOR_GRAY2BGR)
#     imageHSV = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

#     if selected.get() == 1:
#         # Detectamos el color rojo
#         maskRojo1 = cv2.inRange(imageHSV, rangoBajo1, rangoAlto1)
#         maskRojo2 = cv2.inRange(imageHSV, rangoBajo2, rangoAlto2)
#         mask = cv2.add(maskRojo1, maskRojo2)
#     else:
#         # Detección para el color Amarillo y Azul celeste
#         mask = cv2.inRange(imageHSV, rangoBajo, rangoAlto)

#     mask = cv2.medianBlur(mask, 7)
#     colorDetected = cv2.bitwise_and(image, image, mask=mask)

#     # Fondo en grises
#     invMask = cv2.bitwise_not(mask)
#     bgGray = cv2.bitwise_and(imageGray, imageGray, mask=invMask)

#     # Sumamos bgGray y colorDetected
#     finalImage = cv2.add(bgGray, colorDetected)
#     imageToShowOutput = cv2.cvtColor(finalImage, cv2.COLOR_BGR2RGB)

#     # Para visualizar la imagen en lblOutputImage en la GUI
#     im = Image.fromarray(imageToShowOutput)
#     img = ImageTk.PhotoImage(image=im)
#     lblOutputImage.configure(image=img)
#     lblOutputImage.image = img

#     # Label IMAGEN DE SALIDA
#     lblInfo3 = Label(root, text="IMAGEN DE SALIDA:", font="bold")
#     lblInfo3.grid(column=1, row=0, padx=5, pady=5)

# # Creamos los radio buttons y la ubicación que estos ocuparán
# selected = IntVar()
# rad1 = Radiobutton(root, text='Rojo', width=25,value=1, variable=selected, command= deteccion_color)
# rad2 = Radiobutton(root, text='Amarillo',width=25, value=2, variable=selected, command= deteccion_color)
# rad3 = Radiobutton(root, text='Azul celeste',width=25, value=3, variable=selected, command= deteccion_color)
# rad1.grid(column=0, row=4)
# rad2.grid(column=0, row=5)
# rad3.grid(column=0, row=6)

# Creamos el botón para elegir la imagen de entrada
btn = Button(root, text="Elegir imagen", width=25, command=elegir_imagen)
btn.grid(column=0, row=0, padx=5, pady=5)

# Creamos el botón para procesar la imagen
btnProcesar = Button(root, text="Procesar la imagen", width=25)
btnProcesar.grid(column=0, row=3, padx=5, pady=5)

# Creamos el botón salir
btnProcesar = Button(root, text="Salir", width=25, command=root.destroy)
btnProcesar.grid(column=0, row=4, padx=5, pady=5)

root.mainloop()