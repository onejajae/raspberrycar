import raspberrycar
import time
from multiprocessing import Process, Queue

find_wall = 14


class LineTracer(raspberrycar.RaspberryCar):
    def __init__(self, db, distance, defaultSpeed):
        super(LineTracer, self).__init__(db)
        self.differentialForward(defaultSpeed, defaultSpeed)

    def lineTracing(self):
        if True:
            dat = self.trackSensor.getReversedStatus()
            base_l, base_r = 25, 25
            l1, l2, r1, r2, m = dat[0], dat[1], dat[4], dat[3], dat[2]
            weight = 0.7 if m else 1
            left_change = 0 if l1 else 13 * weight + 0 if l2 else 19 * weight
            right_change = 0 if r1 else 13 * weight + 0 if r2 else 19 * weight
            base_l, base_r = base_l + left_change - right_change, base_r + right_change - left_change
            time.sleep(0.001)
            self.leftMotor.PWM.ChangeDutyCycle(base_l)
            self.rightMotor.PWM.ChangeDutyCycle(base_r)
            if l1 and l2 and r1 and r2 and m:
                return False
            return True


def fu():
    while True:
        while myCar.ultraSonicSensor.getDistance() > find_wall:
            continue
        if myCar.ultraSonicSensor.getDistance() < find_wall:
            break
    return


if __name__ == '__main__':
    from setup import db

    myCar = LineTracer(db, 30, 40)
    try:
        while True:
            trace_t = Process(target=fu, args=())
            trace_t.start()
            while trace_t.is_alive(): myCar.lineTracing()
        myCar.stop()
        time.sleep(0.5)
        print 'wall'
        st = time.time()
        myCar.rightSwingTurn_(40)
        while True:
            while myCar.ultraSonicSensor.getDistance() < find_wall * 1.3:
                continue
            if myCar.ultraSonicSensor.getDistance() > find_wall * 1.3:
                break
        myCar.stop()
        rt = time.time() - st
        time.sleep(0.5)
        myCar.differentialForward(40, 40)
        time.sleep(3)
        myCar.stop()
        myCar.leftSwingTurn_(40)
        time.sleep(rt * 1.1)
        myCar.stop()

    except KeyboardInterrupt:
        myCar.clear()