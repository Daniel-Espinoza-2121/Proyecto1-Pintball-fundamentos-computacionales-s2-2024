from tkinter import Tk, Label, Button, Image, OptionMenu, StringVar, Entry, messagebox
import time

root = Tk()
root.title("Pintball")
root.geometry("300x300")
root.configure(bg="grey")
root.resizable(width=False, height=False)

#ventana configuracion
label_intro = Label(
text="""Binevenidos a mi interfaz de mi pintball,
por favor escoja el modo de juego y
como quiere cambiar de turno""",
font=("Arial", 8),
height=3)

modo_juego = StringVar()
modos_juego = ["Un jugador", "Dos jugadores"]
modo_juego.set(modos_juego[0])
menu_modo_juego = OptionMenu(root, modo_juego, *modos_juego)

modo_cambio = StringVar()
modos_cambio = ["Manual", "Automático"]
modo_cambio.set(modos_cambio[0])
menu_modo_cambio = OptionMenu(root, modo_cambio, *modos_cambio)

label_intro.pack()
menu_modo_juego.pack()
menu_modo_cambio.pack()


root.mainloop()