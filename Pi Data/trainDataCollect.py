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
from MotorModule import Motor
#from CamModule import 
# import cv2
# import ... 


def main():
    pass
    
if __name__ == '__main__':
    while True:
        main()