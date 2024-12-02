import cv2 

#Init webcam capture
capR = cv2.VideoCapture("/dev/video0")
capL = cv2.VideoCapture("/dev/video2")
capC = cv2.VideoCapture("/dev/video4")

def getImgR(display=False, size=[480,240]):
    """Returns image file at specified size, display true to dislay image file, from the right camera"""
    _, img = capR.read()
    img = cv2.resize(img, (size[0], size[1])) #Resize the image 
    if display:
        cv2.imshow("image", img) #cv2.imshow() hangs on Pi 
        cv2.waitKey(1)
    return img


def getImgL(display=False, size=[480,240]):
    """Returns image file at specified size, display true to dislay image file, from the right camera"""
    _, img = capL.read()
    img = cv2.resize(img, (size[0], size[1])) #Resize the image 
    if display:
        cv2.imshow("image", img) #cv2.imshow() hangs on Pi  
        cv2.waitKey(1)
    return img
    

def getImgC(display=False, size=[480,240]):
    """Returns image file at specified size, display true to dislay image file, from the center camera"""
    _, img = capC.read()
    img = cv2.resize(img, (size[0], size[1])) #Resize the image 
    if display:
        cv2.imshow("image", img) #cv2.imshow() hangs on Pi  
        cv2.waitKey(1)
    return img


if __name__ == '__main__':
    img = getImgR(True)
    print(img)
    cv2.destroyAllWindows()
