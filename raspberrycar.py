import RPi.GPIO as GPIO
from time import sleep
from motor import LeftMotor, RightMotor
from sensors.track import TrackSensor
from sensors.ultrasonic import UltraSonicSensor
from setup import db


class RaspberryCar(object):
    def __init__(self, db):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        self.leftMotor = LeftMotor(db)
        self.rightMotor = RightMotor(db)
        self.ultraSonicSensor = UltraSonicSensor(db)
        self.trackSensor = TrackSensor(db)

    def any_go_forward(self, speed):
        self.leftMotor.go_forward(speed)
        self.rightMotor.go_forward(speed)

    def any_go_backward(self, speed):
        self.leftMotor.go_backward(speed)
        self.rightMotor.go_backward(speed)

    def go_forward(self, speed, time):
        self.leftMotor.go_forward(speed)
        self.rightMotor.go_forward(speed)
        sleep(time)
        self.stop()

    def go_backward(self, speed, time):
        self.leftMotor.go_backward(speed)
        self.rightMotor.go_backward(speed)
        sleep(time)
        self.stop()

    def stop(self):
        self.leftMotor.stop()
        self.rightMotor.stop()

    def leftSwingTurn(self, speed, time):
        self.rightMotor.go_forward(speed)
        sleep(time)
        self.stop()

    def rightSwingTurn(self, speed, time):
        self.leftMotor.go_forward(speed)
        sleep(time)
        self.stop()

    def leftPointTurn(self, speed, time):
        self.rightMotor.go_forward(speed)
        self.leftMotor.go_backward(speed)
        sleep(time)
        self.stop()

    def rightPointTurn(self, speed, time):
        self.leftMotor.go_forward(speed)
        self.rightMotor.go_backward(speed)
        sleep(time)
        self.stop()

    def get_distance(self):
        return self.ultraSonicSensor.getDistance()


if __name__ == "__main__":
    myCar = RaspberryCar(db)
    try:
        while True:
            myCar.any_go_forward(30)
            if myCar.get_distance() < 22:
                myCar.stop()
                break
        myCar.leftPointTurn(30, 1)
        sleep(1)
        while True:
            myCar.any_go_forward(30)
            if myCar.get_distance() < 20:
                myCar.stop()
                break
        myCar.leftSwingTurn(60, 1.4)
        sleep(1)
        myCar.go_forward(50, 1)
        myCar.stop()
        GPIO.cleanup()

    except KeyboardInterrupt as e:
        myCar.stop()
        GPIO.cleanup()