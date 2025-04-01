from flask import Flask, render_template, redirect
from radio_controller import RadioController

radio = RadioController()
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html", station=radio.get_station_name(), status=radio.radio_on)

@app.route("/power")
def toggle_power():
    if radio.radio_on:
        radio.power_off()
    else:
        radio.power_on()
    return redirect("/")

@app.route("/next")
def next_station():
    if radio.radio_on:
        radio.next_station()
    return redirect("/")
