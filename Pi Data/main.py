from MotorModule import Motor
import KBModule as kb
import cameraModule as cM
import trainDataCollect as collectData
import cv2 
from time import sleep

##################################
###Define Motor Config###
# Pin Order for motor class connected to L298N board: EnA In1 In2 (left), EnB, In3, In4(right)
motor = Motor(2,3,4, 22,17,27)
##################################

kb.init() #init pygame to read key presses

 
def main():
    """
    if kb.getKey('w'):
        motor.move(0.40, 0, 0.1)
        currSpeed, angle = motor.getMetrics()
        print("forward, " + str(currSpeed) +", "+ str(angle))
    if kb.getKey('s'):
        motor.move(-0.40, 0, 0.1)
        currSpeed, angle = motor.getMetrics()
        print("reverse" + str(currSpeed) +", "+ str(angle))
    if kb.getKey('a'):
        motor.move(0.30, -0.5, 0.1)
        currSpeed, angle = motor.getMetrics()
        print("turn left" + str(currSpeed) +", "+ str(angle))
    if kb.getKey('d'):
        motor.move(0.30, 0.5, 0.1)
        currSpeed, angle = motor.getMetrics()
        print("turn right" + str(currSpeed) +", "+ str(angle))
    else:
        motor.stop()
    """
    record = 0
    while True:
        throttle, steeringAngle = motor.getMetrics()
        if kb.getKey('e'):
            #print recording started
            if record == 0: 
                print('Starting Capture... press "e" to log data / stop')
            record +=1
        
            sleep(0.3)
        print("record", str(record))
        #capture frames
        if record == 1: 
            print('Capturing...')
            img = cM.getImgR(False)
            collectData.saveData(img, steeringAngle)
        elif record == 2:
            print('saving...')
            collectData.saveLog()
            record = 0
            print('Done.')

if __name__ == '__main__':
    
    main()
