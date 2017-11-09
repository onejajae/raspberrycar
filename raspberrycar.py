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
        self.rightMotor = RightMotor(db)
        self.ultraSonicSensor = UltraSonicSensor(db)
        self.trackSensor = TrackSensor(db)

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

    def lineTracing(self):
        '''
        trackSensor.getStatus() = (left2, left1, center, right1, right2)
        '''
        speed = 60
        leftSpeed = speed
        rightSpeed = speed
        while True:
            self.goForward(speed)
            data = self.trackSensor.getStatus()
            if not(data[1]):
                rightSpeed += 20
                self.rightMotor.go_forward(rightSpeed)
            if not(data[0]):
                rightSpeed += 20
                self.rightMotor.go_forward(rightSpeed)
            if not(data[3]):
                leftSpeed += 20
                self.leftMotor.go_forward(leftSpeed)
            if not(data[4]):
                leftSpeed += 20
                self.leftMotor.go_forward(leftSpeed)
            if not(data[0] and data[1] and data[2] and data[3] and data[4]):
                self.stop()
                break


if __name__ == "__main__":
    from setup import db
    myCar = RaspberryCar(db)
    try:
        while True:
            myCar.goForward(30)
            if myCar.ultraSonicSensor.getDistance() < 22:
                myCar.stop()
                break
        myCar.leftPointTurn(30, 1)
        sleep(1)
        while True:
            myCar.goForward(30)
            if myCar.ultraSonicSensor.getDistance() < 20:
                myCar.stop()
                break
        myCar.leftSwingTurn(60, 1.4)
        sleep(1)
        myCar.go_forward(50, 1)
        myCar.clear()

    except KeyboardInterrupt as e:
        myCar.clear()
