import raspberrycar


class MazeRunner(raspberrycar.RaspberryCar):
    def __init__(self, db):
        super(MazeRunner, self).__init__(db)
        self.dat = self.trackSensor.getReversedStatus()

    def lineTracing(self):
        self.dat = self.trackSensor.getReversedStatus()
        left, mid, right = self.dat[1], self.dat[2], self.dat[3]
        base_l, base_r = 25, 25
        weight = 0.7 if mid else 1
        left_change = 0 if left else 13 * weight
        right_change = 0 if right else 13 * weight
        base_l += left_change
        base_r += right_change
        self.leftMotor.PWM.ChangeDutyCycle(base_l)
        self.rightMotor.PWM.ChangeDutyCycle(base_r)

    def rightTurn(self, speed):
        self.dat = self.trackSensor.getReversedStatus()
        while not(self.dat[2]):
            self.leftMotor.go_backward(speed)
            self.rightMotor.go_forward(speed)
            self.dat = self.trackSensor.getReversedStatus()
        else:
            self.stop()

    def leftTurn(self, speed):
        self.dat = self.trackSensor.getReversedStatus()
        while not(self.dat[2]):
            self.rightMotor.go_forward(speed)
            self.leftMotor.go_backward(speed)
            self.dat = self.trackSensor.getReversedStatus()
        else:
            self.stop()

    def uTrun(self, speed):
        self.dat = self.trackSensor.getReversedStatus()
        while not (self.dat[2]):
            self.rightMotor.go_forward(speed)
            self.leftMotor.go_backward(speed)
            self.dat = self.trackSensor.getReversedStatus()
        else:
            self.stop()

    def calibrating(self):
        self.dat = self.trackSensor.getReversedStatus()
        while not(self.dat[0] and self.dat[1] and self.dat[3] and self.dat[4]):
            self.rightMotor.go_forward(30)
            self.leftMotor.go_forward(30)
        else:
            self.stop()

    def mazeEscaping(self):
        while True:
            self.dat = self.trackSensor.getReversedStatus()
            self.lineTracing()
            if self.dat[4]:
                self.stop(0.2)
                self.calibrating()
                self.stop(0.2)
                self.rightTurn(30)
            elif not(self.dat[0] and self.dat[1] and self.dat[2] and self.dat[3] and self.dat[4]):
                self.stop(0.2)
                self.uTrun(30)
            else:
                self.stop(0.2)
                self.calibrating()
                self.stop(0.2)
                self.leftTurn(30)


if __name__ == "__main__":
    import setup
    myCar = MazeRunner(setup.db)
    try:
        myCar.mazeEscaping()
        myCar.clear()
    except KeyboardInterrupt:
        myCar.clear()

