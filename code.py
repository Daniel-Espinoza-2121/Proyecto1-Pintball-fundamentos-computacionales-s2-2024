import network
import socket
from machine import Pin, ADC
import time

# Configuración de Pines y demás hardware
registro = Pin(24, Pin.OUT)
clock = Pin(25, Pin.OUT)
anotacion1 = Pin(7, Pin.IN, Pin.PULL_DOWN)
anotacion2 = Pin(8, Pin.IN, Pin.PULL_DOWN)
anotacion3 = Pin(9, Pin.IN, Pin.PULL_DOWN)
anotacion4 = Pin(10, Pin.IN, Pin.PULL_DOWN)
anotacion_esp = Pin(11, Pin.IN, Pin.PULL_DOWN)
visitante = Pin(22, Pin.OUT)
local = Pin(23, Pin.OUT)
boton = Pin(5, Pin.IN)
potenciometro_pin = ADC(Pin(26))

modo_cambio = "manual"

# Configuración Wi-Fi
ssid = 'Daniel realme C55'          # Cambia por el nombre de tu red Wi-Fi
password = 'gatubelo.2121'  # Cambia por la contraseña de tu red Wi-Fi

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

while not wlan.isconnected():
    print("Conectando a Wi-Fi...")
    time.sleep(1)

print("Conectado a Wi-Fi con IP:", wlan.ifconfig()[0])

# Configuración de Socket para escuchar conexiones
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((wlan.ifconfig()[0], 8888))
server_socket.listen(1)

def escribir_pc(comando):
    conn.send((comando + "\n").encode('utf-8'))

def escribir_registro(leds):
    for i in range(len(leds)-1, -1, -1):
        registro.value(leds[i])
        clock.value(1)
        time.sleep_us(10)
        clock.value(0)

def calcular_points(bits):
    for i in range(4):
        if bits[i]:
            escribir_pc("anotacion_normal")
    if bits[4]:
        escribir_pc("anotacion_esp")

def juego():
    bits = [0] * 8
    tiempo_inicio = time.time()
    while True:
        if anotacion1.value():
            bits[0] = 1
        elif anotacion2.value():
            bits[1] = 1
        elif anotacion3.value():
            bits[2] = 1
        elif anotacion4.value():
            bits[3] = 1
        elif anotacion_esp.value():
            bits[4] = 1
            bits[5] = 1
        escribir_registro(bits)
        if (modo_cambio == "automatico" and time.time() - tiempo_inicio >= 60) or (modo_cambio == "manual" and boton.value()):
                calcular_points(bits)
                bits = [0] * 8
                escribir_registro(bits)
                escribir_pc("cambio")
                break

print("Esperando conexión...")
conn, addr = server_socket.accept()
print("Conectado por", addr)

# Bucle principal para recibir y procesar comandos
while True:
    try:
        data = conn.recv(1024).decode('utf-8').strip()
        if data:
            print("Comando recibido:", data)
            if data == "manual":
                modo_cambio = data
            elif data == "automatico":
                modo_cambio = data
            elif data == "inicio":
                juego()
            elif data == "local":
                local.on()
                visitante.off()
            elif data == "visitante":
                local.off()
                visitante.on()
            elif data == "apagar":
                break
            elif data == "A":
                print(f"primera anotación: {anotacion1.value()}")
            elif data == "B":
                print(f"segunda anotación: {anotacion2.value()}")
            elif data == "C":
                print(f"tercera anotación: {anotacion3.value()}")
            elif data == "D":
                print(f"cuarta anotación: {anotacion4.value()}")
            elif data == "E":
                print(f"anotación especial: {anotacion_esp.value()}")
            elif data == "F":
                escribir_registro([0, 0, 0, 0, 0, 0, 0, 1])
                time.sleep(3)
                escribir_registro([0] * 8)
            elif data == "G":
                escribir_registro([0, 0, 0, 0, 0, 0, 1, 0])
                time.sleep(3)
                escribir_registro([0] * 8)
            elif data == "H":
                escribir_registro([0, 0, 0, 0, 0, 1, 0, 0])
                time.sleep(3)
                escribir_registro([0] * 8)
            elif data == "I":
                escribir_registro([0, 0, 0, 0, 1, 0, 0, 0])
                time.sleep(3)
                escribir_registro([0] * 8)
            elif data == "J":
                escribir_registro([0, 0, 1, 1, 0, 0, 0, 0])
                time.sleep(3)
                escribir_registro([0] * 8)
            elif data == "K":
                local.on()
                time.sleep(3)
                local.off()
            elif data == "L":
                visitante.on()
                time.sleep(3)
                visitante.off()
            elif data == "M":
                print(boton.value())
            elif data == "N":
                print(potenciometro_pin.read_u16() // 4096)
            else:
                print("Comando no reconocido")
    except Exception as e:
        print("Error:", e)
        break

print("Cerrando conexión")
conn.close()
server_socket.close()
