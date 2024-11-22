###For use with RPI 3 and L289N Motor Driver Boards###

import RPi.GPIO as GPIO
from time import sleep
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Motor Class to be initalized to each individual motor/output pins
class Motor():
    """Args: int value corresponding to pin number on board"""
    def __init__(self, Ena, In1, In2):
        self.Ena = Ena
        self.In1 = In1
        self.In2 = In2
        GPIO.setup(self.Ena, GPIO.OUT)
        GPIO.setup(self.In1, GPIO.OUT)
        GPIO.setup(self.In2, GPIO.OUT)
        
        self.pwmA= GPIO.PWM(self.Ena, 100)
        self.pwmA.start(0)

    def forward(self, speed=50, t=0):
        """Args: speed: int of total motor speed, t: length of time (ms)"""
        self.pwmA.ChangeDutyCycle(speed)
        GPIO.output(self.In1, GPIO.LOW)
        GPIO.output(self.In2, GPIO.HIGH)
        sleep(t)

    def reverse(self, speed):
        self.pwmA.ChangeDutyCycle(speed)
        GPIO.output(self.In1, GPIO.HIGH)
        GPIO.output(self.In2, GPIO.LOW)
        sleep(t)

    def stop(self, time=0):
        self.pwmA.ChangeDutyCycle(0)
        sleep(time)


################################
"""
######TEST MOTORS######

Ena = 2
In1 = 3
In2 = 4
GPIO.setup(Ena, GPIO.OUT)
GPIO.setup(In1, GPIO.OUT)
GPIO.setup(In2, GPIO.OUT)
pwmA= GPIO.PWM(Ena, 100)
pwmA.start(0)

pwmA.ChangeDutyCycle(60)
GPIO.output(In1, GPIO.LOW)
GPIO.output(In2, GPIO.HIGH)
sleep(2)
pwmA.ChangeDutyCycle(0)

"""

def main():    
    motor1.forward(60, 2)
    

if __name__ == '__main__':
    #####Calling motor class object with pin inputs
    motor1 = Motor(2,3,4)
    main()