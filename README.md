# SmartSeed
SmartSeed is an IoT project that utilizes an ESP32 to collect moisture and water data for plants, and waters them if necessary. The data collected by the ESP32 is sent to a Raspberry Pi, which hosts a website displaying the collected data using Flask. The website contains basic information about the project, a CRUD database and a graph displaying the collected data. 

# Running the Website
Inside the website directory, ```pip install -r requirements``` <br />
then ```python app.py``` <br />
Access the website on 127.0.0.1:5000

# Using Docker to run the website
Create image: ```sudo docker build -t flask-app .```  <br />
Run docker ```sudo docker run -it -p 5000:5000 -d flask-app```   <br />


# Running the Microcontroller Code
To reproduce our solution, you will need to install several modules and configure the Raspberry Pi. You will also need to install various libraries and applications.
- Install the following modules using pip:
```pip install mosquitto mosquitto-clients paho-mqtt```
- Open the Mosquitto configuration file using the following command:
```sudo nano /etc/mosquitto/mosquitto.conf```
- Add the following line to the bottom of the file, replacing "raspberry ip address" with the IP address of your Raspberry Pi:
```bind_address "raspberry ip address"```
- To ensure that the ESP32 can maintain a wireless connection, you can disable the firewall by running the following command:
```sudo ufw disable```

Note: Please make sure to replace "name of file" with the actual name of the file containing your Flask app code. Additionally, ensure that your ESP32 is properly connected to the Raspberry Pi and that you have the necessary code running on it to communicate with the Raspberry Pi via MQTT.

We hope this README helps you set up our SmartSeed project successfully! If you have any questions or encounter any issues, please feel free to reach out to us.
