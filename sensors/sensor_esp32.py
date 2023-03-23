import machine
import time
import neopixel

#setup av pin connections
relay = machine.Pin(14, machine.Pin.OUT)
sensor_fugtighed = machine.ADC(machine.Pin(32))
sensor_vand = machine.ADC(machine.Pin(35))
pixel_pin = machine.Pin(27)
num_pixels = 8
pixels = neopixel.NeoPixel(pixel_pin, num_pixels)

#definere funksjon for å lese vand nivå
def vandlesning():
    avg = 0
    avgNumber = 100
    for x in range(avgNumber):
        avg += sensor_vand.read()
    avg /= avgNumber
    return avg

#definere funksjon for å lese fugtigheds nivå
def fugtighedslesning():
    avg = 0
    avgNumber = 100
    for x in range(avgNumber):
        avg += sensor_fugtighed.read()
    avg /= avgNumber
    return avg

#definere funksjon for å skru relæ av/på
def on():
    relay.value(0)

def off():
    relay.value(1)

#definere funksjon for å sette neopixel lys basert på vand nivå
def set_pixels(n):
    if n <= 1:
        pixels.fill((255, 0, 0))
    elif n <= 2:
        pixels.fill((255, 0, 0))
        pixels[0] = (255, 0, 0)
    elif n <= 4:
        pixels.fill((255, 255, 0))
        for i in range(n-2):
            pixels[i] = (255, 0, 0)
    elif n <= 6:
        pixels.fill((0, 255, 0))
        for i in range(n-2):
            pixels[i] = (255, 255, 0)
    else:
        pixels.fill((0, 255, 0))
        for i in range(n-2):
            pixels[i] = (255, 255, 0)
        pixels[num_pixels-1] = (0, 255, 0)

#while loop som leser av begge sensorer og setter pixel lys udifra vand nivå
while True:
    vand = vandlesning()
    fugtighed = fugtighedslesning()
    if fugtighed < 30:
        on()
        time.sleep(30)
        off()
    if vand < 10:
        set_pixels(1)
    elif vand < 20:
        set_pixels(2)
    elif vand < 50:
        set_pixels(4)
    elif vand < 60:
        set_pixels(6)
    elif vand < 80:
        set_pixels(7)
    else:
        set_pixels(8)
    time.sleep(1)