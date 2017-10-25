from RPi.GPIO import GPIO
from time import sleep

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)


reverse = lambda x: ~x

forward0 = True
forward1 = False

backward0 = reverse(forward0)
backward1 = reverse(forward1)

left_motor_a = 12
left_motor_b = 11
left_motor_pwm = 35

right_motor_a = 15
right_motor_b = 13
right_motor_pwm = 37

def left_motor(x):
    if x:
        GPIO.output(left_motor_a, GPIO.HIGH)
        GPIO.output(left_motor_b, GPIO.LOW)
    else:
        GPIO.output(left_motor_a, GPIO.LOW)
        GPIO.output(left_motor_b, GPIO.HIGH)

def right_motor(x):
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
    left_motor(forward0)
    GPIO.output(left_motor_pwm, GPIO.HIGH)
    right_motor(forward1)
    GPIO.output(right_motor_pwm, GPIO.HIGH)
    pwm_left.ChangeDutyCycle(speed)
    pwm_right.ChangeDutyCycle(speed)
    sleep(running_time)

def go_backward(speed, running_time):
    left_motor(backward0)
    GPIO.output(left_motor_pwm, GPIO.HIGH)
    right_motor(backward1)
    GPIO.output(right_motor_pwm, GPIO.HIGH)
    pwm_left.ChangeDutyCycle(speed)
    pwm_right.ChangeDutyCycle(speed)
    sleep(running_time)

def stop():
    GPIO.output(left_motor_pwm, GPIO.LOW)
    GPIO.output(right_motor_pwm, GPIO.LOW)
    pwm_left.ChangeDutyCycle(0)
    pwm_right.ChangeDutyCycle(0)


try:
    pwm_left.start(0)
    pwm_right.start(0)
    go_forward(40, 3)
    sleep(1)
    go_backward(40, 3)
    sleep(1)
    stop()
except KeyboardInterrupt:
    GPIO.output(left_motor_pwm, GPIO.LOW)
    pwm_left.ChangeDutyCycle(0)
    GPIO.output(right_motor_pwm, GPIO.LOW)
    pwm_right.ChangeDutyCycle(0)
    GPIO.cleanup()