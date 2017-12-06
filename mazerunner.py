import raspberrycar
import time


class MazeRunner(raspberrycar.RaspberryCar):
    def __init__(self, db):
        super(MazeRunner, self).__init__(db)
        self.dat = self.trackSensor.getReversedStatus()

    def lineTracing(self):
        self.dat = self.trackSensor.getReversedStatus()
        left, mid, right = self.dat[1], self.dat[2], self.dat[3]
        base_l, base_r = 27, 27
        weight = 0.7 if mid else 1
        left_change = 0 if left else 20 * weight
        right_change = 0 if right else 20 * weight
        base_l += left_change - right_change
        base_r += right_change - left_change
        time.sleep(0.001)
        # print base_l, base_r
        self.leftMotor.PWM.ChangeDutyCycle(base_l)
        self.rightMotor.PWM.ChangeDutyCycle(base_r)

    def rightTurn(self, speed):
        self.dat = self.trackSensor.getReversedStatus()
        while self.dat[1] or self.dat[2] or self.dat[3]:
            print 1
            self.rightMotor.go_backward(speed)
            self.leftMotor.go_forward(speed)
            time.sleep(0.1)
            self.dat = self.trackSensor.getReversedStatus()
        else:
            print 2, self.dat
            self.stop(0.1)
        while not(self.dat[2] or self.dat[3]) or self.dat[4]:
            print 3
            self.rightMotor.go_backward(speed-5)
            self.leftMotor.go_forward(speed-5)
            time.sleep(0.1)
            self.dat = self.trackSensor.getReversedStatus()
        else:
            print 4, self.dat
            self.stop()

    def leftTurn(self, speed):
        self.dat = self.trackSensor.getReversedStatus()
        while self.dat[1] or self.dat[2] or self.dat[3]:
            print 1
            self.rightMotor.go_forward(speed)
            self.leftMotor.go_backward(speed)
            time.sleep(0.1)
            self.dat = self.trackSensor.getReversedStatus()
        else:
            print 2, self.dat
            self.stop(0.1)
        while not(self.dat[1] or self.dat[2]) or self.dat[0]:
            print 3
            self.rightMotor.go_forward(speed)
            self.leftMotor.go_backward(speed)
            time.sleep(0.1)
            self.dat = self.trackSensor.getReversedStatus()
        else:
            print 4, self.dat
            self.stop()

    def uTrun(self, speed):
        self.dat = self.trackSensor.getReversedStatus()
        while not (self.dat[2]):
            print 1
            self.rightMotor.go_forward(speed)
            self.leftMotor.go_backward(speed)
            time.sleep(0.1)
            self.dat = self.trackSensor.getReversedStatus()
        else:
            print 2
            self.stop()

    def calibrating(self):
        self.goForward(0)
        t=0
        while t < 0.7:
            self.lineTracing()
            time.sleep(0.1)
            t += 0.1
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
                    self.goForward(0)
                    self.rightTurn(25)
                    #raw_input("re")
                    self.goForward(0)
                else:
                    self.calibrating()
                    self.stop(0.3)
                    self.dat = self.trackSensor.getReversedStatus()
                    if not (self.dat[0] or self.dat[1] or self.dat[2] or self.dat[3] or self.dat[4]):
                        print 'left'
                        self.goForward(0)
                        self.leftTurn(25)
                        #raw_input("re")
                        self.goForward(0)
                    else:
                        continue
            elif not (self.dat[0] or self.dat[1] or self.dat[2] or self.dat[3] or self.dat[4]):
                self.stop()
                print 'uturn'
                self.goForward(0)
                self.uTrun(24)
                #raw_input("re")
                self.goForward(0)


if __name__ == "__main__":
    import setup
    myCar = MazeRunner(setup.db)
    try:
        myCar.mazeEscaping()
        myCar.clear()
    except KeyboardInterrupt:
        myCar.clear()