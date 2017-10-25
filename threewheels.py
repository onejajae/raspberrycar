import RPi.GPIO as GPIO
from time import sleep
from setup import *

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)


reverse = lambda x: ~x


def left_motor(x):
    '''
    to setup left motor
    :param x: x should be boolean
    :return: Nothing to return
    '''
    if x:
        GPIO.output(left_motor_a, GPIO.HIGH)
        GPIO.output(left_motor_b, GPIO.LOW)
    else:
        GPIO.output(left_motor_a, GPIO.LOW)
        GPIO.output(left_motor_b, GPIO.HIGH)

def right_motor(x):
    '''
    to setup right motor
    :param x: x should be booblen
    :return: Nothing to return
    '''
    if x:
        GPIO.output(right_motor_a, GPIO.HIGH)
        GPIO.output(right_motor_b, GPIO.LOW)
    else:
        GPIO.output(right_motor_a, GPIO.LOW)
        GPIO.output(right_motor_b, GPIO.HIGH)

GPIO.setup(left_motor_a, GPIO.OUT)
GPIO.setup(left_motor_b, GPIO.OUT)
GPIO.setup(left_motor_pwm, GPIO.OUT)

GPIO.setup(right_motor_a, GPIO.OUT)
GPIO.setup(right_motor_b, GPIO.OUT)
GPIO.setup(right_motor_pwm, GPIO.OUT)

pwm_left = GPIO.PWM(left_motor_pwm, 100)
pwm_right = GPIO.PWM(right_motor_pwm, 100)

def go_forward(speed, running_time):
    '''
    to make the car move forward
    :param speed: car speed to move
    :param running_time: time to move
    :return: Nothing to return
    '''
    left_motor(left_forward)
    GPIO.output(left_motor_pwm, GPIO.HIGH)
    right_motor(right_forward)
    GPIO.output(right_motor_pwm, GPIO.HIGH)
    pwm_left.ChangeDutyCycle(speed)
    pwm_right.ChangeDutyCycle(speed)
    sleep(running_time)

def go_backward(speed, running_time):
    '''
    to make the car move backward
    :param speed: car speed to move
    :param running_time: time to move
    :return: Nothing to return
    '''
    left_motor(left_backward)
    GPIO.output(left_motor_pwm, GPIO.HIGH)
    right_motor(right_backward)
    GPIO.output(right_motor_pwm, GPIO.HIGH)
    pwm_left.ChangeDutyCycle(speed)
    pwm_right.ChangeDutyCycle(speed)
    sleep(running_time)

def stop():
    '''
    to stop the car
    :return: Nothing to return 
    '''
    GPIO.output(left_motor_pwm, GPIO.LOW)
    GPIO.output(right_motor_pwm, GPIO.LOW)
    pwm_left.ChangeDutyCycle(0)
    pwm_right.ChangeDutyCycle(0)


try:
    pwm_left.start(0)
    pwm_right.start(0)
    go_forward(45, 3)
    sleep(1)
    go_backward(45, 3)
    sleep(1)
    stop()
except KeyboardInterrupt:
    GPIO.output(left_motor_pwm, GPIO.LOW)
    pwm_left.ChangeDutyCycle(0)
    GPIO.output(right_motor_pwm, GPIO.LOW)
    pwm_right.ChangeDutyCycle(0)
    GPIO.cleanup()
