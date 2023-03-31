import paho.mqtt.client as mqtt
from flask import Flask
import plotly.graph_objs as go
from plotly.subplots import make_subplots

app = Flask(__name__)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Subscribe to the topic where you expect to receive data
    client.subscribe("test")

def on_message(client, userdata, msg):
    print(msg.topic+" "+msg.payload.decode())
    # Parse the received data and create a graph
    data_values = msg.payload.decode().split(",")
    graph_data = go.Scatter(x=[1, 2], y=[int(data_values[0]), int(data_values[1])])
    fig = make_subplots(rows=1, cols=1)
    fig.add_trace(graph_data, row=1, col=1)
    # Store the figure in a global variable so it can be displayed in the Flask app
    global graph_fig
    graph_fig = fig

# Set up the MQTT client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("192.168.4.5", 1883, 60)

# Start the MQTT client in a separate thread
client.loop_start()

@app.route("/")
def index():
    # Render the HTML template and pass the Plotly figure to it
    return render_template("graph.html", graphJSON=graph_fig.to_json())



if __name__ == "__main__":
    app.run(debug=True)
    