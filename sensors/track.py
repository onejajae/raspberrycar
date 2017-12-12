import RPi.GPIO as GPIO


class TrackSensor(object):
    def __init__(self, db):
        """
        setting 5-way's pin number to variable
        :param db: setup.py's pin numbers
        """
        self.left2 = db['track_left2']
        self.left1 = db['track_left1']
        self.center = db['track_center']
        self.right1 = db['track_right1']
        self.right2 = db['track_right2']
        self.setup()

    def setup(self):
        # Just setup 5-way sensor using setup.py's db.
        GPIO.setup(self.left2, GPIO.IN)
        GPIO.setup(self.left1, GPIO.IN)
        GPIO.setup(self.center, GPIO.IN)
        GPIO.setup(self.right1, GPIO.IN)
        GPIO.setup(self.right2, GPIO.IN)

    def getStatus(self):
        """
        This function give us sensing result value.

        :return:
        """
        left2 = GPIO.input(self.left2)
        left1 = GPIO.input(self.left1)
        center = GPIO.input(self.center)
        right1 = GPIO.input(self.right1)
        right2 = GPIO.input(self.right2)
        return left2, left1, center, right1, right2

    def getReversedStatus(self):
        """
        This function works as same as getStatus().
        Difference is result value.
        this function's all result value is reversed.
        :return:
        """
        reverse = lambda x: 1-x
        left2 = reverse(GPIO.input(self.left2))
        left1 = reverse(GPIO.input(self.left1))
        center = reverse(GPIO.input(self.center))
        right1 = reverse(GPIO.input(self.right1))
        right2 = reverse(GPIO.input(self.right2))
        return left2, left1, center, right1, right2
