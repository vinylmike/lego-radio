from flask import Flask, render_template, redirect
import sys
import os

# Add the parent directory to sys.path so we can import radio_controller
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
