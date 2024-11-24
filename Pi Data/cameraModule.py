import cv2 
"""
from picamera2 import Picamera2, Preview

# Initialize Picamera2
camera = Picamera2()

# Configure camera for preview and capture
camera_config = camera.create_preview_configuration(main={"size": (640, 480), "format": "BGR888"})
camera.configure(camera_config)
"""


#Init webcam capture
capR = cv2.VideoCapture(0)
capL = cv2.VideoCapture(1)

def getImgR(display=False, size=[480,240]):
    """Returns image file at specified size, display true to dislay image file, from the right camera"""
    _, img = capR.read()
    img = cv2.resize(img, (size[0], size[1])) #Resize the image 
    if display:
        #cv2.imshow("image", img) #cv2.imshow() hangs on Pi 
        cv2.waitKey(1)
    return img


def getImgL(display=False, size=[480,240]):
    """Returns image file at specified size, display true to dislay image file, from the right camera"""
    _, img = capL.read()
    img = cv2.resize(img, (size[0], size[1])) #Resize the image 
    if display:
        #cv2.imshow("image", img) #cv2.imshow() hangs on Pi  
        cv2.waitKey(1)
    return img
    

def getImgCenter(display=False, size=(480, 240)):
    """Returns image file at specified size, display True to display the image."""
    img = camera.capture_array()  #Capture an image as a NumPy array
    img = cv2.resize(img, size)  #Resize the image  
    if display:
        #cv2.imshow("image", img) #cv2.imshow() hangs on Pi 
        cv2.waitKey(1)  #Allow OpenCV to process window events
    return img

#def getImgRight
#def getImgLeft

if __name__ == '__main__':
    img = getImgR()