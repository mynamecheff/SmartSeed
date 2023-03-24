# SmartSeed
SmartSeed is an IoT project that utilizes an ESP32 to collect moisture and water data for plants, and waters them if necessary. The data collected by the ESP32 is sent to a Raspberry Pi, which hosts a website displaying the collected data using Flask. The website contains basic information about the project, a CRUD database, and a graph displaying the collected data. 

# How to run
Inside the website directory, ```run pip install -r requirements``` <br />
then ```python app.py``` <br />
Access the website on 127.0.0.1:5000
