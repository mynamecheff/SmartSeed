import time
from machine import Pin, ADC
import neopixel
import machine
import utime
import ssd1306
import dht
import network
from umqtt.simple2 import MQTTClient

rtc = machine.RTC()

# Set up WiFi connection
ssid = "ESPNET" #your 802.11 name
password = "123456789" #802.11 password
wlan = network.WLAN(network.STA_IF)
if not wlan.isconnected():
    wlan.connect(ssid)


# Set up MQTT client
broker_ip = "192.168.4.5" # raspberry pi ip adresse
port = 1883
client_id = "esp32_client"
topic = "test"


# DHT11 sensor setup
d = dht.DHT11(Pin(26))

# Setup the soil moisture sensors
soil_moisture_pin = 32
soil_moisture_adc = ADC(Pin(soil_moisture_pin))
soil_moisture_adc.atten(ADC.ATTN_11DB)

soil_moisture_pin_2 = 33
soil_moisture_adc_2 = ADC(Pin(soil_moisture_pin_2))
soil_moisture_adc_2.atten(ADC.ATTN_11DB)

# Setup the water sensor
water_pin = 35
water_adc = ADC(Pin(water_pin))
water_adc.atten(ADC.ATTN_11DB)

# Setup the relay
relay_pin = 14
relay = Pin(relay_pin, Pin.OUT)

# Setup the neopixel board
neopixel_pin = 25
num_pixels = 8
pixels = neopixel.NeoPixel(Pin(neopixel_pin), num_pixels)

# Set the threshold value for soil moisture percentage
soil_moisture_threshold = 60

# Set up the I2C interface for the display (pin numbers may vary depending on your setup)
i2c = machine.I2C(scl=machine.Pin(22), sda=machine.Pin(21))
display = ssd1306.SSD1306_I2C(128, 64, i2c)

d.measure()
temp = d.temperature()
hum = d.humidity()

year, month, day, weekday, hour, minute, second, subsecond = rtc.datetime()

soil_moisture_raw = soil_moisture_adc.read()
soil_moisture_percentage = int((soil_moisture_raw / 4095) * 100)

soil_moisture_raw_2 = soil_moisture_adc_2.read()
soil_moisture_percentage_2 = int((soil_moisture_raw_2 / 4095) * 100)


water_raw = water_adc.read()
water_percentage = int((water_raw / 4095) * 100)


# Control neopixel board based on water percentage
def control_neopixel(water_percentage):
    if water_percentage >= 70:
        print("Green light is ON")
        pixels.fill((0, 20, 0))  # Green
        pixels.write()
    elif water_percentage >= 50:
        print("Yellow light is ON")
        pixels.fill((20, 20, 0))  # Yellow
        pixels.write()
    elif water_percentage >= 10:
        print("Red light is ON")
        pixels.fill((20, 0, 0))  # Red
        pixels.write()
    else:
        print("Test light is ON")
        pixels.fill((7, 3, 7))  # Off
        pixels.write()



#### OLED Display ####

# Display tid og dato
display.text("Date: {}-{}-{}".format(day, month, year), 0, 0)
display.text("Time: {}:{}:{}".format(hour, minute, second), 0, 10)

# Display gennemsnitlig jordfugtighed og vandmængde i procent
display.text("avg. moist: {}%".format(soil_moisture_percentage), 0, 20)
display.text("Water Level: {}%".format(water_percentage), 0, 30)

# Display temperatur og humidity
display.text("Temp: {}C".format(temp), 0, 40)
display.text("Hum:{}%".format(temp), 0, 50)

# Opdatér OLED displayet
display.show()


def main(data, server=broker_ip, port=port):
    c = MQTTClient(client_id, server, port)
    c.connect()
    c.publish(topic, data)
    c.disconnect()


while True:

    # Print "READING" og tilføj et stigende nummer hver gang der printes
    i = 0
    i = i + 1
    print("READING: " + str(i))

    # Hent nuværende tid og dato fra RTC (Real Time Clock)   
    print("Date: {}-{}-{}".format(day, month, year))
    print("Time: {}:{}:{}".format(hour, minute, second))

    # Aflæs jordfugtighedsdataen fra sensor 1 og 2 og print procentdelen i shell
    print("Soil moisture percentage:", soil_moisture_percentage)
    print("Soil moisture percentage 2:", soil_moisture_percentage_2)

    # Aflæs vandsensordataen og print procentdelen i shell
    print("Water percentage:", water_percentage)

    # Aflæs dataen fra DHT11 sensoren og print resultaterne i shell

    print("Temperature: ", temp, "°C")
    print("Humidity: ", hum, "%")

    #Kontrollér neopixel farverne baseret på udregningen af vandsensorens data i procent
    control_neopixel(water_percentage)

    time.sleep(2)

    # Check if either sensor is below the threshold
    if soil_moisture_percentage < soil_moisture_threshold or soil_moisture_percentage_2 < soil_moisture_threshold:
        print("pump is ON")
        control_neopixel
        relay.value(1)
        time.sleep(3)
        relay.value(0)
    else:
        relay.value(0)
        print("Pump is OFF")
        time.sleep(10)

    soil = (soil_moisture_percentage + soil_moisture_percentage_2)/2
    data = str(soil) + ", " + str(water_percentage)
    print(data)
    main(data)
    time.sleep(4)
