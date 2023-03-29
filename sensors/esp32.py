import network
from umqtt.simple2 import MQTTClient

# Set up WiFi connection
ssid = "Martin"
password = "123456798"
wlan = network.WLAN(network.STA_IF)
if not wlan.isconnected():
    wlan.connect(ssid, password)

# Set up MQTT client
broker_ip = "192.168.173.156" # raspberry pi ip adresse
port = 1883
client_id = "esp32_client"
topic = "test"
message = "Hello from ESP32!"

def main(server=broker_ip, port=port):
    c = MQTTClient(client_id, server, port)
    c.connect()
    c.publish(topic, message)
    c.disconnect()

main()
