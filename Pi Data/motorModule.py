###For use with RPI 3 and L289N Motor Driver Boards###

import RPi.GPIO as GPIO
from time import sleep
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Motor Class to be initalized to each individual motor/output pins
class Motor():
    """Args: int value corresponding to pin number on board"""
    def __init__(self, EnaA, In1A, In2A, EnaB, In1B, In2B):
        self.EnaA = EnaA
        self.In1A = In1A
        self.In2A = In2A

        self.EnaB = EnaB
        self.In1B = In1B
        self.In2B = In2B

        GPIO.setup(self.EnaA, GPIO.OUT)
        GPIO.setup(self.In1A, GPIO.OUT)
        GPIO.setup(self.In2A, GPIO.OUT)
        GPIO.setup(self.EnaB, GPIO.OUT)
        GPIO.setup(self.In1B, GPIO.OUT)
        GPIO.setup(self.In2B, GPIO.OUT)
        
        self.pwmA= GPIO.PWM(self.EnaA, 100)
        self.pwmA.start(0)
        self.pwmB= GPIO.PWM(self.EnaB, 100)
        self.pwmB.start(0)

    def forward(self, speed=50, t=0):
        """Args: speed: int of motor speed, t: length of time (ms)"""
        self.pwmA.ChangeDutyCycle(speed)
        GPIO.output(self.In1A, GPIO.HIGH)
        GPIO.output(self.In2A, GPIO.LOW)
        self.pwmB.ChangeDutyCycle(speed)
        GPIO.output(self.In1B, GPIO.HIGH)
        GPIO.output(self.In2B, GPIO.LOW)
        sleep(t)

    def reverse(self, speed, t=0):
        """Args: speed: int of motor speed, t: length of time (ms)"""
        self.pwmA.ChangeDutyCycle(speed)
        GPIO.output(self.In1A, GPIO.LOW)
        GPIO.output(self.In2A, GPIO.HIGH)
        self.pwmB.ChangeDutyCycle(speed)
        GPIO.output(self.In1B, GPIO.LOW)
        GPIO.output(self.In2B, GPIO.HIGH)
        sleep(t)
        

    def stop(self, time=0):
        self.pwmA.ChangeDutyCycle(0)
        self.pwmB.ChangeDutyCycle(0)
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
    motor1.forward(30, 2)
    motor1.reverse(30, 2)
    motor1.stop()
    

if __name__ == '__main__':
    #####Calling motor class object with pin inputs
    motor1 = Motor(2,3,4,22,17,27)
    main()