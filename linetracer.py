import raspberrycar
from time import sleep


class LineTracer(raspberrycar.RaspberryCar):
    def __init__(self, db):
        super(LineTracer, self).__init__(db)

    def lineTracing(self, distance, defaultSpeed):
        self.differentialForward(defaultSpeed, defaultSpeed)
        while True:
            dat = self.trackSensor.getReversedStatus()
            base_l, base_r = 25, 25
            l1, l2, r1, r2, m = dat[0], dat[1], dat[4], dat[3], dat[2]
            weight = 0.7 if m else 1
            left_change = 0 if l1 else 13 * weight + 0 if l2 else 19 * weight
            right_change = 0 if r1 else 13 * weight + 0 if r2 else 19 * weight
            base_l, base_r = base_l + left_change - right_change, base_r + right_change - left_change
            sleep(0.001)
            self.leftMotor.PWM.ChangeDutyCycle(base_l)
            self.rightMotor.PWM.ChangeDutyCycle(base_r)
            if l1 and l2 and r1 and r2 and m:
                break


if __name__ == '__main__':
    from setup import db
    myCar = LineTracer(db)
    try:
        myCar.lineTracing(30, 40)
    except KeyboardInterrupt:
        myCar.clear()