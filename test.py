import RPi.GPIO as GPIO
from time import sleep
from time import time

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
    'right_motor_pwm': 37,
    'trig': 18,
    'echo': 16,
    'track_left2': 0,
    'track_left1': 0,
    'track_center': 0,
    'track_right1': 0,
    'track_right2': 0
}


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
        GPIO.setup(self.pinPWM, GPIO.OUT)
        self.PWM = GPIO.PWM(self.pinPWM, 100)
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
            GPIO.output(self.pinA, GPIO.HIGH)
            GPIO.output(self.pinB, GPIO.LOW)
        else:
            GPIO.output(self.pinA, GPIO.LOW)
            GPIO.output(self.pinB, GPIO.HIGH)
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


class UltraSonicSensor:
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


class TrackSensor:
    def __init__(self, db):
        self.left2 = db['track_left2']
        self.left1 = db['track_left1']
        self.center = db['track_center']
        self.right1 = db['track_right1']
        self.right2 = db['track_right2']

    def setup(self):
        GPIO.setup(self.left2, GPIO.IN)
        GPIO.setup(self.left1, GPIO.IN)
        GPIO.setup(self.center, GPIO.IN)
        GPIO.setup(self.right1, GPIO.IN)
        GPIO.setup(self.right2, GPIO.IN)

    def getStatus(self):
        left2 = GPIO.input(self.left2)
        left1 = GPIO.input(self.left1)
        center = GPIO.input(self.center)
        right1 = GPIO.input(self.right1)
        right2 = GPIO.input(self.right2)
        return left2, left1, center, right1, right2


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
