import RPi.GPIO as GPIO
from time import time
from time import sleep


class UltraSonicSensor(object):
    def __init__(self, db):
        self.trig = db['trig']
        self.echo = db['echo']
        self.setup()

    def setup(self):
        GPIO.setup(self.trig, GPIO.OUT)
        GPIO.setup(self.echo, GPIO.IN)

    def getDistance(self):
        GPIO.output(self.trig, False)
        sleep(0.5)
        GPIO.output(self.trig, True)
        sleep(0.00001)
        GPIO.output(self.trig, False)
        while GPIO.input(self.echo) == 0:
            pulse_start = time()
        while GPIO.input(self.echo) == 1:
            pulse_end = time()
        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17000
        distance = round(distance, 2)
        return distance
