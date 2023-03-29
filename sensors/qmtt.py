import network
from umqtt.simple2 import MQTTClient

# Set up WiFi connection
ssid = "Martin"
password = "123456798"
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

# Set up MQTT client
broker_ip = "192.168.173.156" # Replace with Raspberry Pi's IP address
port = 1883
client_id = "esp32_client"
topic = b"test"
message = b"Hello from ESP32!"

def main(server=broker_ip, port=port):
    c = MQTTClient(client_id, server, port)
    c.connect()
    c.publish(topic, message)
    c.disconnect()

if __name__ == "__main__":
    main()
