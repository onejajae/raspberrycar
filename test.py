import RPi.GPIO as GPIO
from time import sleep

db = {
    'left_forward': False,
    'right_forward': False,
    'left_backward': True,
    'right_backward': True,
    'left_motor_a': 12,
    'left_motor_b': 11,
    'left_motor_pwm': 35,
    'right_motor_a': 31,
    'right_motor_b': 33,
    'right_motor_pwm': 37
}


class RaspberryCar(object):
    def __init__(self, db):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        self.leftMotor = LeftMotor(db)
        self.rightMotor = RightMotor(db)

    def go_forward(self, speed, time):
        self.leftMotor.go_forward(speed)
        self.rightMotor.go_forward(speed)
        sleep(time)

    def go_backward(self, speed, time):
        self.leftMotor.go_backward(speed)
        self.rightMotor.go_backward(speed)
        sleep(time)

    def stop(self):
        self.leftMotor.stop()
        self.rightMotor.stop()


class Motor(object):
    def __init__(self, pinA, pinB, pinPWM, forward, backward):
        self.pinA = pinA
        self.pinB = pinB
        self.pinPWM = pinPWM
        self.forward = forward
        self.backward = backward
        self.PWM = GPIO.PWM(self.pinPWM, 100)
        self.setup()

    def setup(self):
        GPIO.setup(self.pinA, GPIO.OUT)
        GPIO.setup(self.pinB, GPIO.OUT)
        GPIO.setup(self.PWM, GPIO.OUT)
        self.PWM.start(0)

    def go_forward(self, speed):
        if self.forward:
            GPIO.output(self.pinA, GPIO.HIGH)
            GPIO.output(self.pinB, GPIO.LOW)
        else:
            GPIO.output(self.pinA, GPIO.LOW)
            GPIO.output(self.pinB, GPIO.HIGH)
        GPIO.output(self.pinPWM, GPIO.HIGH)
        self.PWM.ChangeDutyCycle(speed)

    def go_backward(self, speed):
        if self.backward:
            GPIO.output(self.pinA, GPIO.LOW)
            GPIO.output(self.pinB, GPIO.HIGH)
        else:
            GPIO.output(self.pinA, GPIO.HIGH)
            GPIO.output(self.pinB, GPIO.LOW)
        GPIO.output(self.pinPWM, GPIO.HIGH)
        self.PWM.ChangeDutyCycle(speed)

    def stop(self):
        GPIO.output(self.pinPWM, GPIO.LOW)
        self.PWM.ChangeDutyCycle(0)


class LeftMotor(Motor):
    def __init__(self, db):
        self.pinA = db['left_motor_a']
        self.pinB = db['left_motor_b']
        self.pinPWM = db['left_motor_pwm']
        self.forward = db['left_forward']
        self.backward = db['left_backward']
        self.setup()


class RightMotor(Motor):
    def __init__(self, db):
        self.pinA = db['right_motor_a']
        self.pinB = db['right_motor_b']
        self.pinPWM = db['right_motor_pwm']
        self.forward = db['right_forward']
        self.backward = db['right_backward']
        self.setup()


if __name__ == "__main__":
    myCar = RaspberryCar(db)
    try:
        myCar.go_forward(45, 2)
        sleep(1)
        myCar.go_forward(45, 2)
        sleep(1)
        myCar.stop()
    except KeyboardInterrupt as e:
        myCar.stop()
        GPIO.cleanup()
