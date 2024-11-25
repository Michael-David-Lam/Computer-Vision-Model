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

global imgList, turnAngleList
folderCount =0
count = 0
imgList = []
turnAngleList = []

#Current Directory path
PATH = os.path.join(os.getcwd(), 'Data')

#Create new folder 
while os.path.exists(os.path.join(PATH, f'Images{str(folderCount)}')):
    folderCount +=1
newPath = PATH + '/Images'+str(folderCount)
os.makedirs(newPath)

#Save images in new directory
#def #saveData(imgC, imgL, imgR, steeringAngle, throttle, reverse, speed):
def saveData(img, steeringAngle):
    """Args: 3 images (left, center, right), turning angle (-1 to 1), throttle (0 to 1), reverse (0 to 1), speed(0-30.19) """
    global imgList, turnAngleList  
    currTime = datetime.now()
    timeStamp = str(datetime.timestamp(currTime)).replace('.', '')
    fileName = os.path.join(newPath, f'Images_{timeStamp}_center.jpg')
    cv2.imwrite(fileName, img)
    imgList.append(fileName)
    turnAngleList.append(steeringAngle)

#Save log file of imgs(left, center, right), turning angle (-1 to 1), throttle (0 to 1), reverse (0 to 1), speed(0-30.19) 
def saveLog():
    global imgList, turnAngleList  
    rawData = {'Image': imgList,
               'Steering Angle': turnAngleList
                }
    dataFrame = pd.DataFrame(rawData)
    dataFrame.to_csv(os.path.join(PATH, f'log_{str(folderCount)}.csv'), index=False, header=False)
    print('Log saved.')
    print('Total Images: ', len(imgList))


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