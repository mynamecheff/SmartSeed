from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import paho.mqtt.client as mqtt
import sqlite3 as sql


app = Flask(__name__, static_url_path='/static')

# MQTT configurations
MQTT_HOST = "192.168.4.5"
MQTT_PORT = 1883
MQTT_TOPIC = "test"

# SQLite configuration
DB_NAME = "db_plants.db"

def on_message(client, userdata, message):
    # This function is called when a new message is received
    msg = message.payload.decode('utf-8')
    data = msg.split(",")
    if len(data) != 2:
        print("Invalid data received:", msg)
        return
    conn = sql.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO sensor_data (value1, value2) VALUES (?, ?)", (data[0], data[1]))
    conn.commit()
    conn.close()
    print("Data saved to database:", msg)

def on_connect(client, userdata, flags, rc):
    # This function is called when the client connects to the broker
    client.subscribe(MQTT_TOPIC)
    print("Connected to broker")

client = mqtt.Client()
client.on_message = on_message
client.on_connect = on_connect
client.connect(MQTT_HOST, MQTT_PORT, 60)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/data")
def get_sensor_data():
    conn = sql.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT value1, value2 FROM sensor_data")
    rows = cursor.fetchall()
    conn.close()
    return {"data": rows}

@app.route("/chart")
def chart():
    data = get_sensor_data()["data"]
    values1 = []
    values2 = []
    for row in data:
        values1.append(row[0])
        values2.append(row[1])
    return render_template("chart.html", values1=values1, values2=values2)


@app.route("/setup")
def setup():
    return render_template("setup.html")


@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/science")
def science():
    return render_template("plant_science.html")


@app.route("/sustainability")
def sustainability():
    return render_template("sustainability.html")


@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/dashboard")
def dashboard():
    con = sql.connect(DB_NAME)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select * from plants")
    data = cur.fetchall()
    return render_template("dashboard.html", datas=data)


@app.route("/add_plant", methods=['POST', 'GET'])
def add_plant():
    if request.method == 'POST':
        sort = request.form['Sort']
        planted = request.form['Planted']
        harvested = request.form['Harvested']
        location = request.form['Location']
        description = request.form['Description']
        con = sql.connect(DB_NAME)
        cur = con.cursor()
        cur.execute("insert into plants(Sort, Planted, Harvested, Location, Description) values (?,?,?,?,?)",
                    (sort, planted, harvested, location, description))
        con.commit()
        flash('Plants Updated', 'success')
        return redirect(url_for("dashboard"))
    return render_template("add_plant.html")


@app.route("/edit_plant/<string:ID>", methods=['POST', 'GET'])
def edit_plant(ID):
    if request.method == 'POST':
        sort = request.form['Sort']
        planted = request.form['Planted']
        harvest = request.form['Harvested']
        location = request.form['Location']
        description = request.form['Description']
        con = sql.connect(DB_NAME)
        cur = con.cursor()
        cur.execute("update plants set Sort=?,Planted=?,Harvested=?,Location=?,Description=? where ID=?",
                     (sort, planted, harvest, location, description, ID))
        con.commit()
        flash('Plants Updated', 'success')
        return redirect(url_for("dashboard"))
    con = sql.connect(DB_NAME)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select * from plants where ID=?", (ID,))
    data = cur.fetchone()
    return render_template("edit_plant.html", datas=data)


@app.route("/delete_plant/<string:ID>", methods=['GET'])
def delete_plant(ID):
    con = sql.connect(DB_NAME)
    cur = con.cursor()
    cur.execute("delete from plants where ID=?", (ID,))
    con.commit()
    flash('Plant Deleted', 'warning')
    return redirect(url_for("dashboard"))


if __name__ == '__main__':
 #   client.loop_start()
    app.secret_key = 'admin123'
    app.run(debug=True)
