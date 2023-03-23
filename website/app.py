# Description: This is the main file of the website
from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3 as sql
app = Flask(__name__, static_url_path='/static')


@app.route("/")
def index():
    return render_template("index.html")


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
    con = sql.connect("db_plants.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select * from plants")
    data = cur.fetchall()
    return render_template("dashboard.html", datas=data)


@app.route("/add_user", methods=['POST', 'GET'])
def add_user():
    if request.method == 'POST':
        sort = request.form['Sort']
        planted = request.form['Planted']
        harvested = request.form['Harvested']
        location = request.form['Location']
        description = request.form['Description']
        con = sql.connect("db_plants.db")
        cur = con.cursor()
        cur.execute("insert into plants(Sort, Planted, Harvested, Location, Description) values (?,?,?,?,?)",
                    (sort, planted, harvested, location, description))
        con.commit()
        flash('Plants Updated', 'success')
        return redirect(url_for("dashboard"))
    return render_template("add_user.html")


@app.route("/edit_user/<string:ID>", methods=['POST', 'GET'])
def edit_user(ID):
    if request.method == 'POST':
        sort = request.form['Sort']
        planted = request.form['Planted']
        harvest = request.form['Harvested']
        location = request.form['Location']
        description = request.form['Description']
        con = sql.connect("db_plants.db")
        cur = con.cursor()
        cur.execute("update plants set Sort=?,Planted=?,Harvested=?,Location=?,Description where ID=?",
                    (sort, planted, harvest, location, description, ID))
        con.commit()
        flash('Plants Updated', 'success')
        return redirect(url_for("dashboard"))
    con = sql.connect("db_plants.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select * from plants where ID=?", (ID,))
    data = cur.fetchone()
    return render_template("edit_user.html", datas=data)


@app.route("/delete_user/<string:ID>", methods=['GET'])
def delete_user(ID):
    con = sql.connect("db_plants.db")
    cur = con.cursor()
    cur.execute("delete from plants where ID=?", (ID,))
    con.commit()
    flash('Plant Deleted', 'warning')
    return redirect(url_for("dashboard"))


if __name__ == '__main__':
    app.secret_key = 'admin123'
    app.run(debug=True)
