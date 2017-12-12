import RPi.GPIO as GPIO
from time import time
from time import sleep


class UltraSonicSensor(object):
    def __init__(self, db):
        """
        setting ultrasonic sensor's pin nums to variable.
        :param db: setup.py's pin numbers
        """
        self.trig = db['trig']
        self.echo = db['echo']
        self.setup()

    def setup(self):
        """
        Just setup the ultrasonic sensor using pin numbers.
        :return:
        """
        GPIO.setup(self.trig, GPIO.OUT)
        GPIO.setup(self.echo, GPIO.IN)

    def getDistance(self):
        """
        this code can measure distance between obstacle and machine
        :return: the distance between obstacle and machine
        """
        GPIO.output(self.trig, False)
        sleep(0.15)
        GPIO.output(self.trig, True)
        sleep(0.0001)
        GPIO.output(self.trig, False)
        while GPIO.input(self.echo) == 0:
            pulse_start = time()
        while GPIO.input(self.echo) == 1:
            pulse_end = time()
        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17000
        distance = round(distance, 2)
        return distance


if __name__ == '__main__':
    try:
        import setup
        sensor = UltraSonicSensor(setup.db)
        while True:
            print sensor.getDistance()
            sleep(0.1)
    except KeyboardInterrupt:
        GPIO.cleanup()