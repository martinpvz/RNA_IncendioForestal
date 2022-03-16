# from tkinter import *
# from tkinter import ttk


# root = Tk()
# root.title('RNA para identificar incendios forestales')

# frame = Frame(root)
# frame.pack()
# frame.config(width=480, height= 320)

# myLabel = Label(frame, text='Ingresar una imagen')
# myLabel.place(x=150, y=10)

# select_button = ttk.Button(
#     frame,
#     text='Seleccionar',
#     command=lambda: root.quit()
# )

# select_button.pack(
#     ipadx=5,
#     ipady=5,
#     expand=True
# )


# root.mainloop()

import tkinter as tk
from tkinter import ttk
from tkinter.ttk import Label

# root window
root = tk.Tk()
root.geometry('300x200')
root.resizable(False, False)
root.title('Seleccionar imagenes para la RNA')

# show a label
label = Label(root, text='Seleccionar una imagen')
label.pack(ipadx=10, ipady=10)

# exit button
exit_button = ttk.Button(
    root,
    text='Seleccionar imagen',
    command=lambda: root.quit()
)

exit_button.pack(
    ipadx=5,
    ipady=5,
    expand=True
)

root.mainloop()