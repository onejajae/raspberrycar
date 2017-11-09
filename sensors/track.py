import RPi.GPIO as GPIO


class TrackSensor:
    def __init__(self, db):
        self.left2 = db['track_left2']
        self.left1 = db['track_left1']
        self.center = db['track_center']
        self.right1 = db['track_right1']
        self.right2 = db['track_right2']
        self.setup()

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
