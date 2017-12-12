import RPi.GPIO as GPIO


class Motor(object):
    def __init__(self, pinA, pinB, pinPWM, forward, backward):
        """
        Inherit this class to setup motor.

        :param pinA: determine the wheel's way with pinB
        :param pinB: determine the wheel's way with pinA
        :param pinPWM: determine motor's speed
        :param forward: determine the rotate direction.
        :param backward:
        """
        self.pinA = pinA
        self.pinB = pinB
        self.pinPWM = pinPWM
        self.forward = forward
        self.backward = backward
        self.PWM = GPIO.PWM(self.pinPWM, 100)
        self.setup()

    def setup(self):
        """
        main setting definition
        all pins and pwm are setting in here.
        :return:
        """
        GPIO.setup(self.pinA, GPIO.OUT)
        GPIO.setup(self.pinB, GPIO.OUT)
        GPIO.setup(self.pinPWM, GPIO.OUT)
        self.PWM = GPIO.PWM(self.pinPWM, 100)
        self.PWM.start(0)

    # both go_forward and go_backward determine the rotate direction.
    # param speed means the speed of wheel.
    # each Motor's class use this to go.

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
        """
        make the wheel's speed 0 to stop the machine.
        :return:
        """
        self.PWM.ChangeDutyCycle(0)
        GPIO.output(self.pinPWM, GPIO.LOW)


class LeftMotor(Motor):
    def __init__(self, db):
        """
        This class setup Left motor
        :param db: setup.py's pins.
        """
        self.pinA = db['left_motor_a']
        self.pinB = db['left_motor_b']
        self.pinPWM = db['left_motor_pwm']
        self.forward = db['left_forward']
        self.backward = db['left_backward']
        self.setup()


class RightMotor(Motor):
    def __init__(self, db):
        """
        This class setup Right motor
        :param db: setup.py's pins.
        """
        self.pinA = db['right_motor_a']
        self.pinB = db['right_motor_b']
        self.pinPWM = db['right_motor_pwm']
        self.forward = db['right_forward']
        self.backward = db['right_backward']
        self.setup()
