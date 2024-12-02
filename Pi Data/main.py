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
    """Main function, using manual motor movement, for collecting the data (images and .csv) for lane detection training."""
    
    
    record = 0
    print('Press "e" to begin data capture, q to stop')
    while True:

        #Detect Key presses for motor control
        if kb.getKey('w'):
            motor.move(0.40, 0, 0.1)
            currSpeed, angle = motor.getMetrics()
            print("forward, " + str(currSpeed) +", "+ str(angle))
        if kb.getKey('s'):
            motor.move(-0.40, 0, 0.1)
            currSpeed, angle = motor.getMetrics()
            print("reverse" + str(currSpeed) +", "+ str(angle))
        if kb.getKey('a'):
            motor.move(0.3, -0.5, 0.1)
            currSpeed, angle = motor.getMetrics()
            print("turn left" + str(currSpeed) +", "+ str(angle))
        if kb.getKey('d'):
            motor.move(0.3, 0.5, 0.1)
            currSpeed, angle = motor.getMetrics()
            print("turn right" + str(currSpeed) +", "+ str(angle))
        if kb.getKey('q'):
            break
        else:
            motor.stop()

        #Get current speed and turn data
        throttle, steeringAngle = motor.getMetrics()
        #Detect key press to start capture
        if kb.getKey('e'):
            #print recording started
            if record == 0: 
                print('Starting Capture... press "e" to log data / stop')
            record +=1        
            sleep(0.3)

        #Capture frames if 'e' was pressed, or save if pressed twice
        if record == 1: 
            print('Capturing...')
            imgC = cM.getImgC(True, [680,440])
            imgR = cM.getImgR(True, [680,440])
            imgL = cM.getImgL(True, [680,440])
            collectData.saveData(imgC, imgR, imgL, steeringAngle, throttle, 0, (throttle*30.19))
        elif record == 2:
            print('Saving...')
            collectData.saveLog()
            print('Save Successful.')
            record = 0
            

if __name__ == '__main__':
    
    main()
    cv2.destroyAllWindows()
