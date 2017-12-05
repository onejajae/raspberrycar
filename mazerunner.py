import raspberrycar
import time


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
        base_l += left_change - right_change
        base_r += right_change - left_change
        time.sleep(0.001)
        # print base_l, base_r
        self.leftMotor.PWM.ChangeDutyCycle(base_l)
        self.rightMotor.PWM.ChangeDutyCycle(base_r)

    def rightTurn(self, speed):
        self.dat = self.trackSensor.getReversedStatus()
        self.rightPointTurn(speed, 0.3)
        while not(self.dat[2]):
            self.rightMotor.go_backward(speed)
            self.leftMotor.go_forward(speed)
            self.dat = self.trackSensor.getReversedStatus()
        else:
            self.stop()

    def leftTurn(self, speed):
        self.dat = self.trackSensor.getReversedStatus()
        self.leftPointTurn(speed, 0.3)
        while not(self.dat[2]):
            self.rightMotor.go_forward(speed)
            self.leftMotor.go_backward(speed)
            self.dat = self.trackSensor.getReversedStatus()
        else:
            self.stop()

    def uTrun(self, speed):
        self.dat = self.trackSensor.getReversedStatus()
        self.leftPointTurn(speed, 0.3)
        while not (self.dat[2]):
            self.rightMotor.go_forward(speed)
            self.leftMotor.go_backward(speed)
            self.dat = self.trackSensor.getReversedStatus()
        else:
            self.stop()

    def calibrating(self):
        self.go_forward(30, 0.3)
        self.stop()



    def mazeEscaping(self):
        self.differentialForward(20, 20)
        while True:
            self.dat = self.trackSensor.getReversedStatus()
            self.lineTracing()
            if self.dat[4] or self.dat[0]:
                print self.dat[0], self.dat[4]
                self.stop(0.3)
                self.dat = self.trackSensor.getReversedStatus()
                print self.dat[0], self.dat[4]
                if self.dat[4]:
                    print 'right'
                    self.calibrating()
                    self.rightTurn(30)
                    raw_input("re")
                else:
                    self.calibrating()
                    self.stop(0.3)
                    self.dat = self.trackSensor.getReversedStatus()
                    if not (self.dat[0] or self.dat[1] or self.dat[2] or self.dat[3] or self.dat[4]):
                        print 'left'
                        self.leftTurn(30)
                        raw_input("re")
                    else:
                        continue
            elif not (self.dat[0] or self.dat[1] or self.dat[2] or self.dat[3] or self.dat[4]):
                self.stop()
                print 'uturn'
                self.uTrun(30)
                raw_input("re")


"""
            if self.dat[4]:
                print 'right'
                self.stop(0.2)
                self.calibrating()
                self.stop(0.2)
                self.rightTurn(25)
            elif not(self.dat[0] and self.dat[2] and self.dat[4]):
                print 'uturn'
                self.stop(0.2)
                self.uTrun(25)
            elif self.dat[0] and self.dat[1]:
                print 'left'
                self.stop(0.2)
                self.calibrating()
                self.stop(0.2)
                self.leftTurn(25)
            else:
                print'go'
                self.differentialForward(40, 40)
                self.lineTracing()
"""


if __name__ == "__main__":
    import setup
    myCar = MazeRunner(setup.db)
    try:
        myCar.mazeEscaping()
        myCar.clear()
    except KeyboardInterrupt:
        myCar.clear()

