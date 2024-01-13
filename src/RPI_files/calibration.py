###########################################################################
# Subject: CZ3004 MDP Image Recognition 20/21
# Team: 22
# Contributor: Sam Jian Shen, Lin Yue
# Version: 1.0
###########################################################################
###########################################################################
# Calibration Image to find the y-offset values
# How to use:
# 1) Place a object at approx 25cm apart and middle from picamera
# 2) Ensure enough lighting on the target
# 3) It is recommended to use circle symbol for this operation
###########################################################################
# Import various libraries
from picamera import PiCamera          
from picamera.array import PiRGBArray   
import cv2 as cv 
import re
import os

# Set Properties
res_horizontal = 640
res_vertical = 480
p = 45 # padding value

# Path Setting
path = 'img_capture/'
num = 0
ext = 'jpg'
key = 0

# Measurement References
def view(image,o):
    a = o
    #a = 104 # offset
    b = 10   # bounding box 
    t = 3    # fine tune (shift down)
    #image = captured_.copy()
    #image  = cv.rectangle(image , (0,0+a), (215,272+a), (255,0,0), 1)
    #image  = cv.rectangle(image , (425,0+a), (640,272+a), (0,0,255), 1)
    #image  = cv.rectangle(image , (215,0+a), (425,272+a), (0,255,0), 1)
    image  = cv.rectangle(image , (5+b,0+a-b+t), (215-b,210+a-3*b+t), (255,255,255), 1)
    image  = cv.rectangle(image, (425+b,0+a-b+t), (635-b,210+a-3*b+t), (255,255,255), 1)
    image  = cv.rectangle(image , (215+b,0+a-b+t), (425-b,210+a-3*b+t), (255,255,255), 1)

    width = (635-b) - (425+b)
    height = (210+a-3*b+t) - (a-b+t)
    print('New Offset Minimum Y Value: ', 0+a-b+t)

    # Display Capture Image to User
    cv.imshow('Calibrated_Image',image)
    cv.waitKey(key) 
    cv.destroyAllWindows() 

# Invoke RPI Camera Module V2 functions and output as array in BGR format
camera = PiCamera()

while True:
    # Produces a 3D RGB Array from RGB Capture
    output = PiRGBArray(camera)

    # Set Resolution of the Camera
    camera.resolution = (res_horizontal,res_vertical)

    # Capture Image in BGR format
    camera.capture(output,'bgr')

    #### Removed This In Main RPI ####
    output.array = cv.rotate(output.array, cv.ROTATE_180)
    image = output.array

    # Target Image to Process
    image_crop = output.array[0:480, 215:425].copy() # crop middle 1/3 image img[y:y+h, x:x+w]

    # Grayscale
    image_gray = cv.cvtColor(image_crop, cv.COLOR_BGR2GRAY) 
    
    # Apply Canny
    image_canny = cv.Canny(image_gray, 30, 200) 

    # Finding Contours 
    contours, heir = cv.findContours(image_canny, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    # Find the highest yield contours (proximity connected dots)
    c = max(contours, key = cv.contourArea)

    # Extract the extreme points which form rectangle
    x,y,w,h = cv.boundingRect(c)

    # Show the rectangle x,y values
    print('Bounding Box Coordinate: ',x+215,y,x+w+215,y+h)

    # Plot the rectangle back to origin image
    output.array = cv.rectangle(output.array, (x+215,y), (x+w+215,y+h), (255,0,0), 1)
    output.array = cv.rectangle(output.array, (x+215-p,y-p), (x+w+215+p,y+h+p), (255,0,255), 1)

    offset = y-p 
    
    view(output.array,offset)

    # Prompt User Ready For Next Capture or Exit Program
    code = str(input("Satisfy with the result? Key In Any except '0' to exit\n"))
    if(code == '0'):
        exit()

    