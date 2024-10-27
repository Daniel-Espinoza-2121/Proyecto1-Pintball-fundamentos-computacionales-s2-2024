from tkinter import Tk, Label, Button, Canvas, Radiobutton, StringVar, Entry
import socket
import time
from random import randint

# Configuración inicial
fuente = ("Arial", 8)
turno_actual = 0

# Configuración de la ventana principal
root = Tk()
root.title("Paintball")
root.geometry("300x300")
root.configure(bg="grey")
root.resizable(width=False, height=False)

# Dirección IP y puerto de la Raspberry Pi Pico W
IP_PICO = "192.168.41.219"  # Cambia esta IP a la IP asignada a la Pico
PUERTO_PICO = 8888

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((IP_PICO, PUERTO_PICO))
except Exception as e:
    print("Error al conectar con la Pico:", e)

# Función para enviar comandos a la Raspberry Pi Pico W
def enviar_comando(comando):
    s.sendall(comando.encode('utf-8'))

# Clase para cada jugador
class Jugador:
    def __init__(self, name, color):
        self.name_label = Label(root, text=name, font=fuente)
        self.points = 0
        self.label_points = Label(root, text=f"{self.points}", font=fuente)
        self.bandera = Canvas(root, width=50, height=30, bg=color)

    def anotacion_normal(self):
        self.points += 100
        self.actualizar_puntos()
        enviar_comando("anotacion_normal")

    def anotacion_especial(self):
        self.points = 500
        self.actualizar_puntos()
        enviar_comando("anotacion_especial")

    def actualizar_puntos(self):
        self.label_points.config(text=f"{self.points}")

# Lista de jugadores
jugadores = [Jugador("Jugador 1", "blue"), Jugador("Jugador 2", "red")]

# Ventana de configuración de juego
label_intro = Label(
    root,
    text="Bienvenidos a mi interfaz de Paintball,\npor favor escoja el modo de juego y\ncómo quiere cambiar de turno",
    font=fuente,
    height=3
)

boton_siguiente_inicio = Button(root, text="Siguiente", font=fuente, command=lambda: [ocultar_inicio(), mostrar_custom()])

modo_cambio = StringVar(value="Manual")
boton_manual = Radiobutton(root, text="Manual", variable=modo_cambio, value="Manual", font=fuente)
boton_automatico = Radiobutton(root, text="Automático", variable=modo_cambio, value="Automático", font=fuente)

# Mostrar la ventana de configuración de juego
def mostrar_inicio():
    label_intro.pack(pady=10)
    boton_siguiente_inicio.pack(pady=5)
    boton_manual.pack(anchor="w")
    boton_automatico.pack(anchor="w")

def ocultar_inicio():
    label_intro.pack_forget()
    boton_siguiente_inicio.pack_forget()
    boton_manual.pack_forget()
    boton_automatico.pack_forget()

# Ventana de personalización de jugadores
boton_siguiente_jugador = Button(root, text="Inicio", font=fuente, command=lambda: [ocultar_custom(), cambiar_name(), mostrar_juego()])

entry_jugador_1 = Entry(root, font=fuente)
entry_jugador_2 = Entry(root, font=fuente)

def mostrar_custom():
    enviar_comando("automatico")
    Label(root, text="Nombre del Jugador 1:", font=fuente).pack()
    entry_jugador_1.pack()
    Label(root, text="Nombre del Jugador 2:", font=fuente).pack()
    entry_jugador_2.pack()
    boton_siguiente_jugador.pack(pady=10)

def ocultar_custom():
    entry_jugador_1.pack_forget()
    entry_jugador_2.pack_forget()
    boton_siguiente_jugador.pack_forget()

# Cambiar nombres de los jugadores según los valores de entrada
def cambiar_name():
    new_name_1 = entry_jugador_1.get().strip()
    new_name_2 = entry_jugador_2.get().strip()
    if new_name_1:
        jugadores[0].name_label.config(text=new_name_1)
    if new_name_2:
        jugadores[1].name_label.config(text=new_name_2)

# Mostrar la interfaz de juego
def mostrar_juego():
    turno_actual = randint(0, 1)
    for jugador in jugadores:
        jugador.name_label.pack()
        jugador.bandera.pack(pady=2)
        jugador.label_points.pack()
    enviar_comando("juego")
    juego()

def juego():
    turnos = 0
    while True:
        # Espera a recibir datos
        data = s.recv(1024)  # Recibe hasta 1024 bytes
        if not data:
            print("El servidor ha cerrado la conexión.")
            break
        comando = data.decode('utf-8')
        if comando == "cambio":
            turnos += 1
            enviar_comando("juego")
        elif turnos > 3:
            turnos = 0
            cambiar_turno()
        elif comando == "anotacion_normal":
            jugadores[turno_actual].anotacion_normal()
        elif comando == "anotacion_esp":
            jugadores[turno_actual].anotacion_especial()
        time.sleep(0.1)
# Función para cambiar el turno
def cambiar_turno():
    global turno_actual
    turno_actual = 1 if turno_actual == 0 else 0

# Iniciar interfaz de inicio
mostrar_inicio()
root.mainloop()
