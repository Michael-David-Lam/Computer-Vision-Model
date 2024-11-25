"""
Script for collecting training data

For each pass of the loop, collect:
    -> current frame: image file of each camera connected
    -> current speed at that frame
    -> current turning angle at that frame

    send images to directory + JSON or txt file of speed and turn angle 
    
    JSON or txt file should have format:
    {
        "filname of image": "filename"
        "speed": decimal 
        "angle": decimal
    }
"""
import pandas as pd
import cv2
import os
from datetime import datetime  

global imgListC, imgListR, imgListL, turnAngleList, throttleList, rThrottleList, speedListMPH
folderCount =0
count = 0
#Create image lists for each camera
imgListC = []
imgListR = []
imgListL = []
turnAngleList = []
throttleList = []
rThrottleList = []
speedListMPH = []

#Current Directory path
PATH = os.path.join(os.getcwd(), 'Data')

#Create new folder 
while os.path.exists(os.path.join(PATH, f'Images{str(folderCount)}')):
    folderCount +=1
newPath = PATH + '/Images'+str(folderCount)
os.makedirs(newPath)

#Save images in new directory
def saveData(imgC, imgR, imgL, steeringAngle, throttle, reverse, speed): 
    """Args: 3 images (left, center, right), turning angle (-1 to 1), throttle (0 to 1), reverse (0 to 1), speed(0-30.19) """
    global imgList, turnAngleList  
    currTime = datetime.now()
    timeStamp = str(datetime.timestamp(currTime)).replace('.', '')
    
    fileNameC = os.path.join(newPath, f'Images_{timeStamp}_center.jpg')
    fileNameR = os.path.join(newPath, f'Images_{timeStamp}_right.jpg')
    fileNameL = os.path.join(newPath, f'Images_{timeStamp}_left.jpg')

    cv2.imwrite(fileNameC, imgC)
    cv2.imwrite(fileNameR, imgR)
    cv2.imwrite(fileNameL, imgL)

    imgListC.append(fileNameC) 
    imgListR.append(fileNameR)
    imgListL.append(fileNameL)

    turnAngleList.append(steeringAngle)
    throttleList.append(throttle)
    rThrottleList.append(reverse)
    speedListMPH.append(speed)

#Save log file of imgs(left, center, right), turning angle (-1 to 1), throttle (0 to 1), reverse (0 to 1), speed(0-30.19) 
def saveLog():
    global imgListC, imgListR, imgListL, turnAngleList, throttleList, rThrottleList, speedListMPH 
    rawData = {'ImageC': imgListC,
               'ImageR': imgListR,
               'ImageL': imgListL,
               
               'Steering Angle': turnAngleList
                }
    dataFrame = pd.DataFrame(rawData)
    dataFrame.to_csv(os.path.join(PATH, f'log_{str(folderCount)}.csv'), index=False, header=False)
    print('Log saved.')
    print('Total Images: ', len(imgListC)*3)


def main():
    cap = cv2.VideoCapture(0)
    for x in range(5):
        _, img = cap.read()
        saveData(img, 0.5)
        cv2.waitKey(1)
        cv2.imshow("image", img)
    saveLog()

if __name__ == '__main__':
    main()