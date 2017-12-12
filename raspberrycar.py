import RPi.GPIO as GPIO
from time import sleep
from motor import LeftMotor, RightMotor
from sensors.track import TrackSensor
from sensors.ultrasonic import UltraSonicSensor


class RaspberryCar(object):
    def __init__(self, db):
        """
        bring all settings from motor, ultra, track.py
        :param db: setup.py's pin numbers.
        """
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
        """
        make machine go forward.
        but this function can give different speed for each motor.
        :param leftSpeed: speed of left motor
        :param rightSpeed: speed of right motor
        :return:
        """
        self.leftMotor.go_forward(leftSpeed)
        self.rightMotor.go_forward(rightSpeed)

    def goForward(self, speed):
        """
        make machine go forward.
        but this function can give same speed for each motor.
        :param speed: speed of both motor
        :return:
        """
        self.leftMotor.go_forward(speed)
        self.rightMotor.go_forward(speed)

    def goBackward(self, speed):
        '''
        make machine go backward.
        but this function can give same speed for each motor.
        :param speed: speed of both motor
        :return:
        '''
        self.leftMotor.go_backward(speed)
        self.rightMotor.go_backward(speed)

    def go_forward(self, speed, time):
        """
        make machine go forward.
        but this function can give same speed for each motor.
        and this can control how much time can machine run
        :param speed: speed of both motor
        :param time: time limit of machine's run
        :return:
        """
        self.leftMotor.go_forward(speed)
        self.rightMotor.go_forward(speed)
        sleep(time)
        self.stop()

    def go_backward(self, speed, time):
        """
        make machine go forward.
        but this function can give same speed for each motor.
        and this can control how much time can machine run
        :param speed: speed of both motor
        :param time: time limit of machine's run
        :return:
        """
        self.leftMotor.go_backward(speed)
        self.rightMotor.go_backward(speed)
        sleep(time)
        self.stop()

    def stop(self, sec=0):
        """
        make the machine stop
        :return:
        """
        self.leftMotor.stop()
        self.rightMotor.stop()
        if sec:
            sleep(sec)
        else:
            pass

    def leftSwingTurn(self, speed, time):
        """
        use only right wheel to turn left
        :param speed: speed of right motor
        :param time: time limit of machine's run
        :return:
        """
        self.rightMotor.go_forward(speed)
        sleep(time)
        self.stop()

    def rightSwingTurn(self, speed, time):
        """
        use only left motor to turn right
        :param speed: speed of left motor
        :param time: time limit of machine's run
        :return:
        """
        self.leftMotor.go_forward(speed)
        sleep(time)
        self.stop()

    def leftPointTurn(self, speed, time):
        """
        use both wheel to turn left.
        right wheel goes forward, left wheel goes backward
        :param speed: speed of both motor
        :param time: time limit of machine's run
        :return:
        """
        self.rightMotor.go_forward(speed)
        self.leftMotor.go_backward(speed)
        sleep(time)
        self.stop()

    def rightPointTurn(self, speed, time):
        """
        use both wheel to turn right.
        right wheel goes backward, left wheel goes forward
        :param speed: speed of both motor
        :param time: time limit of machine's run
        :return:
        """
        self.leftMotor.go_forward(speed)
        self.rightMotor.go_backward(speed)
        sleep(time)
        self.stop()

    def clear(self):
        """
        use stop() and GPIO.cleanup() to reset all settings of machine.
        :return:
        """
        self.stop()
        GPIO.cleanup()


if __name__ == "__main__":
    from setup import db
    myCar = RaspberryCar(db)
    try:
        while True:
            print myCar.ultraSonicSensor.getDistance()
            sleep(0.5)
    except KeyboardInterrupt as e:
        myCar.clear()
