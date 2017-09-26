#!/usr/bin/env python
# Import necessary modules
import RPi.GPIO as GPIO
import video_dir
import car_dir
import motor
import time          
 
busnum = 1          # Edit busnum to 0, if you uses Raspberry Pi 1 or 0
 
def setup():
   global offset_x,  offset_y, offset, forward0, forward1, backward0, backward1 
   offset_x = -79
   offset_y = -140
   offset = -51
   forward0 = False
   forward1 = True

   #Read calibration value from config file
   try:
      for line in open('config'):
         if line[0:8] == 'offset_x':
            offset_x = int(line[11:-1])
            print 'offset_x =', offset_x
         if line[0:8] == 'offset_y':
            offset_y = int(line[11:-1])
            print 'offset_y =', offset_y
         if line[0:8] == 'offset =':
            offset = int(line[9:-1])
            print 'offset =', offset
         if line[0:8] == "forward0":
            forward0 = line[11:-1]
            print 'turning0 =', forward0
         if line[0:8] == "forward1":
            forward1 = line[11:-1]
            print 'turning1 =', forward1
   except:
      print 'no config file, set config to original' 
   video_dir.setup(busnum=busnum)
   car_dir.setup(busnum=busnum)
   motor.setup(busnum=busnum)
   video_dir.calibrate(offset_x, offset_y)
   car_dir.calibrate(offset)
   
   #Set the motor's true / false value to the opposite.
   backward0 = REVERSE(forward0)
   backward1 = REVERSE(forward1)

#Functions to control the direction of motor in reverse
def REVERSE(x):
   if x == 'True':
      return 'False'
   elif x == 'False':
      return 'True'
 
def go_Forward(speed, running_time):
   global forward0, forward1
   motor.setSpeed(speed)
   motor.motor0(forward0)
   motor.motor1(forward1)
   time.sleep(running_time)
   motor.stop()
   
def go_Backward(speed, running_time):
   global backward0, backward1
   motor.setSpeed(speed)
   motor.motor0(backward0)
   motor.motor1(backward1)
   time.sleep(running_time)
   motor.stop()
 
if __name__ == "__main__":
   try:
      setup()
      go_Forward(40, 2)
      time.sleep(1)
      go_Forward(60, 2)
      time.sleep(1)      
      
   except KeyboardInterrupt:
      go_Forward(0, 1)
      quit()
