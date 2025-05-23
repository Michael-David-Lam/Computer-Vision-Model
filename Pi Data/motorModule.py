###For use with RPI 3 and L289N Motor Driver Boards###

import RPi.GPIO as GPIO
from time import sleep
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Motor Class to be initalized to each individual motor/output pins
class Motor():
    """Args: int value corresponding to pin number on board. Formatting: (EnA, In1, In2, EnB, In3, In4)
    """
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

        self.currentSpeed = 0
        self.turnAngle = 0

    def move(self, speed=0.5, turn = 0, t=0):
        """Args: speed: float of motor speed (0 - 1: forward, -1 - 0: reverse), turn: float of turning amount (0 - 1: left, -1 - 0: right) , t: length of time (ms)"""
        
        self.currentSpeed = speed
        self.turnAngle = turn

        #Normalize speed and turn values 
        speed = speed * 100
        turn = turn * 100

        #Set speed values for turn
        rightSpeed = speed - turn
        leftSpeed = speed + turn

        #Limit left and right speed values
        if rightSpeed > 100:
            rightSpeed = 100
        elif rightSpeed < -100:
            rightSpeed -100
        if leftSpeed > 100:
            leftSpeed = 100
        elif leftSpeed < -100:
            leftSpeed -100

        self.pwmA.ChangeDutyCycle(abs(leftSpeed))
        self.pwmB.ChangeDutyCycle(abs(rightSpeed))

        #Set pin values based on speed and turn args 
        if leftSpeed > 0: #if turning left
            #reverse left motors
            GPIO.output(self.In1A, GPIO.HIGH)
            GPIO.output(self.In2A, GPIO.LOW)
            
            
        else:
             #if not turning left, forward left motors
            GPIO.output(self.In1A, GPIO.LOW)
            GPIO.output(self.In2A, GPIO.HIGH)
           
        
        if rightSpeed > 0: #if turning right
            #reverse right motors
            GPIO.output(self.In1B, GPIO.HIGH)
            GPIO.output(self.In2B, GPIO.LOW)
            
        else:
            #if not turning right, forward right motors
            GPIO.output(self.In1B, GPIO.LOW)
            GPIO.output(self.In2B, GPIO.HIGH)

        sleep(t)

    def stop(self, time=0):
        """Stop Motors for t, time (ms)"""
        self.pwmA.ChangeDutyCycle(0)
        self.pwmB.ChangeDutyCycle(0)
        sleep(time)

    def getMetrics(self):
        return self.currentSpeed, self.turnAngle 
        #save to file; json or txt?

################################
# For testing functionality

def main():    
    motor1.move(0.40, 0, 0.3)
    motor1.stop()
    
if __name__ == '__main__':
    #####Calling motor class object with pin inputs
    motor1 = Motor(2,3,4,22,17,27)
    main()