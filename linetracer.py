import raspberrycar
from time import sleep


class LineTracer(raspberrycar.RaspberryCar):
    def __init__(self, db):
        super(LineTracer, self).__init__(db)
        self.status = True

    def lineTracking(self, defaultSpeed):
        '''
        Our core code for line-tracing.
        We use reversed 5-way sensor's value.
        each sensor's reversed value is added in each wheel's speed.
        and each wheel's speed input ChangeDutyCycle.

        :param defaultSpeed:
        :return:
        '''
        dat = self.trackSensor.getReversedStatus()
        base_l, base_r = 45, 45
        l1, l2, r1, r2, m = dat[0], dat[1], dat[4], dat[3], dat[2]
        weight = 0.7 if m else 1
        left_change = 0 if l1 else 13 * weight + 0 if l2 else 19 * weight
        right_change = 0 if r1 else 13 * weight + 0 if r2 else 19 * weight
        base_l, base_r = base_l + left_change - right_change, base_r + right_change - left_change
        sleep(0.001)
        self.leftMotor.PWM.ChangeDutyCycle(base_l)
        self.rightMotor.PWM.ChangeDutyCycle(base_r)
        if l1 and l2 and r1 and r2 and m:
            self.status = False
            return

    def avoidObstacle(self):
        '''
        This function make our machine avoiding obstacle.
        :return:
        '''
        print 'wall'
        self.stop()
        avoidTime = 0.4
        self.stop()
        sleep(0.5)
        self.rightPointTurn(30, avoidTime)
        self.stop()
        sleep(0.5)
        self.go_forward(30, 2)
        self.stop()
        sleep(0.5)
        self.leftPointTurn(30, avoidTime * 2)
        self.stop()
        sleep(0.5)
        self.goForward(0)

    def lineTracing(self, defaultSpeed, distance):
        '''
        this code is main code.
        if our machine detect obstacle, we use avoidObstacle()
        else, we use f().

        :param defaultSpeed:  The basic speed of our car
        :param distance:  machine's detect range
        :return: no return parameter
        '''
        self.differentialForward(defaultSpeed, defaultSpeed)
        while self.status:
            if self.ultraSonicSensor.getDistance() < distance:
                self.avoidObstacle()
                self.stop()
            else:
                self.lineTracking(defaultSpeed)


if __name__ == '__main__':
    from setup import db
    myCar = LineTracer(db)
    try:
        myCar.lineTracing(60, 20)
        myCar.clear()
    except KeyboardInterrupt:
        myCar.clear()
