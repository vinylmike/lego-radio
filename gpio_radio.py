from gpiozero import Button, LED
from time import sleep, time
from radio_controller import RadioController

power_button = Button(20)
tune_button = Button(2)
power_led = LED(21)

radio = RadioController()
last_power_press = 0
last_tune_press = 0
cool_off_seconds = 1.0

print("📻 GPIO Radio Controller Ready")

while True:
    if power_button.is_pressed:
        now = time()
        if now - last_power_press > cool_off_seconds:
            last_power_press = now
            if not radio.radio_on:
                radio.power_on()
                power_led.on()
            else:
                power_led.off()
                radio.power_off()
        sleep(0.2)

    if tune_button.is_pressed and radio.radio_on:
        now = time()
        if now - last_tune_press > cool_off_seconds:
            last_tune_press = now
            radio.next_station()
        sleep(0.2)

    sleep(0.1)
