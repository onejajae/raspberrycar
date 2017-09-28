import RPi.GPIO as GPIO
import time

GPIO.setup(38,GPIO.IN)
GPIO.setup(40,GPIO.IN)

if __name__ == "__main__":
    while True:
        try:
            print '38: %d , 40: %d'%(GPIO.input(38), GPIO.input(40))
        except KeyboardInterrupt:
            quit()
