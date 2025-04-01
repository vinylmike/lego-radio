import subprocess, os

stations = [
    ("BBC Radio 1", "http://stream.live.vc.bbcmedia.co.uk/bbc_radio_one"),
    ("NightRide LoFi", "https://stream.nightride.fm/lofi_ogg"),
    ("Jazz", "http://us4.internet-radio.com:8266/stream"),
    ("FIP France", "https://icecast.radiofrance.fr/fip-midfi.mp3"),
]

class RadioController:
    def __init__(self):
        self.radio_on = False
        self.current_index = 0
        self.going_forward = True
        self.player = None
        self.station_file = "/home/vinylmike/lego_radio/last_station.txt"
        self.load_station_index()

    def load_station_index(self):
        try:
            with open(self.station_file, "r") as f:
                self.current_index = int(f.read().strip())
        except:
            self.current_index = 0

    def save_station_index(self):
        with open(self.station_file, "w") as f:
            f.write(str(self.current_index))

    def play_station(self):
        name, url = stations[self.current_index]
        self.stop()
        self.player = subprocess.Popen(["mpv", url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"Playing: {name}")

    def stop(self):
        if self.player:
            self.player.terminate()
            self.player.wait()
            self.player = None

    def power_on(self):
        if not self.radio_on:
            self.radio_on = True
            self.play_station()

    def power_off(self):
        if self.radio_on:
            self.radio_on = False
            self.save_station_index()
            self.stop()
            os.system("sudo shutdown now")

    def next_station(self):
        if self.going_forward:
            if self.current_index < len(stations) - 1:
                self.current_index += 1
            else:
                self.going_forward = False
                self.current_index -= 1
        else:
            if self.current_index > 0:
                self.current_index -= 1
            else:
                self.going_forward = True
                self.current_index += 1

        self.play_station()
        self.save_station_index()

    def get_station_name(self):
        return stations[self.current_index][0]