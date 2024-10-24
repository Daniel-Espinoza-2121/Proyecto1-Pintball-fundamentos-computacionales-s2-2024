
from machine import Pin, UART
import time

uart = UART(0, baudrate=9600)

registro = Pin(24, Pin.OUT)
clock = Pin(25, Pin.Out)

anotacion1 = Pin(7, Pin.IN)
anotacion2 = Pin(8, Pin.IN)
anotacion3 = Pin(9, Pin.IN)
anotacion4 = Pin(10, Pin.IN)
anotacion_esp = Pin(11, Pin.IN)

leds = [0, 0, 0, 0, 0, 0]

visitante = Pin(22, Pin.OUT)
local = Pin(23, Pin.OUT)

boton = Pin(5, Pin.IN)
potenciometro = Pin(26, Pin.IN)

def escribir_registro():
    for i in range(-1, len(leds)-1, -1):
        registro.value(leds[i])
        clock.value(1)
        time.sleep_us(10)
        clock.value(0)

while True:
    if uart.any():
        data = uart.read()
        command = data.decode('utf-8').strip()
        
    time.sleep(0.1)