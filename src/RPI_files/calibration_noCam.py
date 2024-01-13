###########################################################################
# Subject: CZ3004 MDP Image Recognition 20/21
# Team: 22
# Contributor: Sam Jian Shen, Lin Yue
# Version: 1.0
###########################################################################
###########################################################################
# Calibration Image to find the y-offset values (offline mode)
# How to use:
# 1) Place a object at approx 25cm apart and middle from picamera
# 2) Ensure enough lighting on the target
# 3) It is recommended to use circle symbol for this operation
###########################################################################
# Import various libraries 
import cv2 as cv 
import re
import os

p = 45 # padding value

# Path Setting
path = 'img_capture/'
id = 7
index = 5
num = 0
ext = 'jpg'
key = 0


fullpath = 'CZ3004_MDP_RPI_ImageRecognition/' +  path + str(id) + '/' + str(id) + '(' + str(index) + ').' + ext

print('Reading... path: ', fullpath)

# Measurement References
def view(image,o):
    a = o
    #a = 104 #offset
    b = 10  #bounding box 
    t = 3 #fine tune (shift down)
    #image = captured_.copy()
    #image  = cv.rectangle(image , (0,0+a), (215,272+a), (255,0,0), 1)
    #image  = cv.rectangle(image , (425,0+a), (640,272+a), (0,0,255), 1)
    #image  = cv.rectangle(image , (215,0+a), (425,272+a), (0,255,0), 1)
    image  = cv.rectangle(image , (5+b,0+a-b+t), (215-b,210+a-3*b+t), (255,255,255), 1)
    image  = cv.rectangle(image, (425+b,0+a-b+t), (635-b,210+a-3*b+t), (255,255,255), 1)
    image  = cv.rectangle(image , (215+b,0+a-b+t), (425-b,210+a-3*b+t), (255,255,255), 1)

    width = (635-b) - (425+b)
    height = (210+a-3*b+t) - (a-b+t)
    print('New Offset Minimum Y Value (White Crop): ', 0+a-b+t)
    print('Top Left of Left (White Crop): ', 5+b)
    print('Top Right of Left (White Crop): ', 215-b)
    print('Top Left of Mid (White Crop): ', 215+b)
    print('Top Right of Mid (White Crop): ', 425-b)
    print('Top Left of Right (White Crop): ', 425+b)
    print('Top Right of Right (White Crop): ', 635-b)
    print('New Width = ', width, ' New Height =', height)


    # Display Capture Image to User
    cv.imshow('Calibrated_Image_Full',image)
    cv.imshow('Calibrated_Image_Left',image[0+a-b+t:210+a-3*b+t, 5+b:215-b]) #img[y:y+h, x:x+w]
    cv.imshow('Calibrated_Image_Mid',image[0+a-b+t:210+a-3*b+t, 215+b:425-b])
    cv.imshow('Calibrated_Image_Right',image[0+a-b+t:210+a-3*b+t, 425+b:635-b])
    cv.waitKey(key) 
    cv.destroyAllWindows() 

while True:

    # Target
    image = cv.imread(fullpath)
    image = image[70:480,0:640]
    image_ref = image.copy()
    # print(image) # test img exist

    # Target Image to Process
    image_crop = image[0:480, 215:425].copy() # crop middle 1/3 image img[y:y+h, x:x+w]

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
    print('Bounding Box Coordinate(Blue): ',x+215,y,x+w+215,y+h)

    # Plot the rectangle back to origin image
    image_ref = cv.rectangle(image_ref, (x+215,y), (x+w+215,y+h), (255,0,0), 1)
    image_ref = cv.rectangle(image_ref, (x+215-p,y-p), (x+w+215+p,y+h+p), (255,0,255), 1)

    # Display Capture Image to User
    #cv.imshow('Captured',output.array)
    #cv.waitKey(key) 
    #cv.destroyAllWindows()
    # 
    offset = y-p 
    
    view(image_ref,offset)

    # Prompt User Ready For Next Capture or Exit Program
    code = str(input("Satisfy with the result? Key In Any except '0' to exit\n"))
    if(code == '0'):
        exit(0)

    
