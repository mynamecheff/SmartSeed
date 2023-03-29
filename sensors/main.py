import paho.mqtt.client as mqtt

# Define callback functions for MQTT events
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("test")

def on_message(client, userdata, msg):
    print(msg.topic + "hey " + str(msg.payload))

# Connect to MQTT broker
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("192.168.173.156", 1883, 60)

# Publish a message
client.publish("test", "Hello from Raspberry Pi!")

# Keep the client running to receive messages
client.loop_forever()
