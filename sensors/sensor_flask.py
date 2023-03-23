import machine
import time
from flask import Flask, jsonify
import neopixel

app = Flask(__name__)

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

#setup av en route som blir aktivert når en bruger besøker root URL
@app.route('/')
def home():
    return 'Hello, World!'

#setup av ny route som blir aktivert når bruger går inn på /measure URL
@app.route('/measure')
def measure():
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
    return jsonify({"vand": vand, "fugtighed": fugtighed})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

