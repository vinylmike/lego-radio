from flask import Flask, render_template, request, jsonify
import requests
import json
import os

app = Flask(__name__)

PRESETS_FILE = os.path.join(os.path.dirname(__file__), '..', 'presets.json')
RADIO_BROWSER_API = "https://de1.api.radio-browser.info/json"

# Load current presets (UUIDs)
def load_presets():
    if not os.path.exists(PRESETS_FILE):
        return []
    with open(PRESETS_FILE, 'r') as f:
        return json.load(f)

# Save updated presets (UUIDs)
def save_presets(presets):
    with open(PRESETS_FILE, 'w') as f:
        json.dump(presets, f, indent=2)

@app.route("/stations")
def station_manager():
    return render_template("stations.html")

@app.route("/api/search")
def search_stations():
    term = request.args.get("q", "")
    r = requests.get(f"{RADIO_BROWSER_API}/stations/search", params={"name": term})
    return jsonify(r.json())

@app.route("/api/presets")
def get_presets():
    return jsonify(load_presets())

@app.route("/api/presets/add", methods=["POST"])
def add_preset():
    data = request.get_json()
    uuid = data.get("stationuuid")
    presets = load_presets()
    if uuid and len(presets) < 10 and uuid not in [p['stationuuid'] for p in presets]:
        presets.append({"stationuuid": uuid})
        save_presets(presets)
        return jsonify({"status": "added"})
    return jsonify({"status": "error"})

@app.route("/api/presets/remove", methods=["POST"])
def remove_preset():
    data = request.get_json()
    uuid = data.get("stationuuid")
    presets = load_presets()
    updated = [p for p in presets if p["stationuuid"] != uuid]
    save_presets(updated)
    return jsonify({"status": "removed"})
