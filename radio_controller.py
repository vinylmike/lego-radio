import os
import random
import subprocess
from pathlib import Path

class RadioController:
    def __init__(self):
        self.stations = [
            ("BBC Radio 1", "http://stream.live.vc.bbcmedia.co.uk/bbc_radio_one"),
            ("NPR News", "https://npr-ice.streamguys1.com/live.mp3"),
            ("KEXP", "http://live-mp3-128.kexp.org:8000"),
            ("Jazz24", "https://live.wostreaming.net/direct/ppm-jazz24mp3-ibc1"),
            ("80s Radio", "http://uk4.internet-radio.com:8276/"),
        ]
        self.current_index = 0
        self.station_file = str(Path.home() / "lego_radio" / "last_station.txt")
        self.radio_on = False
        self.process = None
        self.load_last_station()

    def load_last_station(self):
        if os.path.exists(self.station_file):
            with open(self.station_file, "r") as f:
                try:
                    self.current_index = int(f.read().strip())
                except:
                    self.current_index = 0

    def save_last_station(self):
        with open(self.station_file, "w") as f:
            f.write(str(self.current_index))

    def get_station_name(self):
        return self.stations[self.current_index][0]

    def play_station(self):
        if self.process:
            self.process.terminate()
        name, url = self.stations[self.current_index]
        print(f"Playing: {name}")
        self.process = subprocess.Popen(["mpv", "--no-video", url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def stop_station(self):
        if self.process:
            self.process.terminate()
            self.process = None

    def next_station(self):
        if len(self.stations) > 1:
            self.current_index += 1
            if self.current_index >= len(self.stations):
                self.stations.reverse()
                self.current_index = 1
        self.save_last_station()
        self.play_station()

    def power_on(self):
        if not self.radio_on:
            self.radio_on = True
            self.play_station()

    def power_off(self):
        if self.radio_on:
            self.radio_on = False
            self.stop_station()
