import RPi.GPIO as GPIO
from time import sleep
from motor import LeftMotor, RightMotor
from sensors.track import TrackSensor
from sensors.ultrasonic import UltraSonicSensor


class RaspberryCar(object):
    def __init__(self, db):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        self.leftMotor = LeftMotor(db)
        sleep(0.001)
        self.rightMotor = RightMotor(db)
        sleep(0.001)
        self.ultraSonicSensor = UltraSonicSensor(db)
        sleep(0.001)
        self.trackSensor = TrackSensor(db)
        sleep(0.001)

    def differentialForward(self, leftSpeed, rightSpeed):
        self.leftMotor.go_forward(leftSpeed)
        self.rightMotor.go_forward(rightSpeed)

    def goForward(self, speed):
        self.leftMotor.go_forward(speed)
        self.rightMotor.go_forward(speed)

    def goBackward(self, speed):
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

    def clear(self):
        self.stop()
        GPIO.cleanup()


if __name__ == "__main__":
    from setup import db
    myCar = RaspberryCar(db)
    try:
        while True:
            print myCar.trackSensor.getStatus()
            sleep(0.5)
    except KeyboardInterrupt as e:
        myCar.clear()
