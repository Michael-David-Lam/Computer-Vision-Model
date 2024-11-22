import RPi.GPIO as GPIO
from time import sleep
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


class Motor():
    def __init__(self, Ena, In1, In2):
        self.Ena = Ena
        self.In1 = In1
        self.In2 = In2
        GPIO.setup(self.Ena, GPIO.OUT)
        GPIO.setup(self.In1, GPIO.OUT)
        GPIO.setup(self.In2, GPIO.OUT)
        
        self.pwmA= GPIO.PWM(self.Ena, 100)
        self.pwmA.start(0)

    def moveForward(self, speed):
        pass
    def moveBackward(self, speed):
        pass
    def turnLeft(self, speed):
        pass
    def turnRight(self, speed):
        pass





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

