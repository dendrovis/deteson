###########################################################################
# Subject: CZ3004 MDP Image Recognition 20/21
# Team: 22
# Contributor: Sam Jian Shen, Lin Yue
# Version: 1.0
###########################################################################
###########################################################################
# Produce capture RAW images and store into a directory to produce dataset 
# for our model.
# References:
# [1] up arrow (white)
# [2] down arrow (blue)
# [3] left arrow (red)
# [4] right arrow (yellow)
# [5] Go (circle)
# [6] six
# [7] seven
# [8] eight
# [9] nine
# [10] zero
# [11] alphabet V
# [12] alphabet W
# [13] alphabet X
# [14] alphabet Y
# [15] alphabet Z
###########################################################################
# Import various libraries
from picamera import PiCamera 
from picamera.array import PiRGBArray
import cv2 as cv 
import re
import os

# Bug Message
print('this program is able to read max (10) only for some reason therefore please ensure all photo for this class is taken 1 single time')

# Measurement References
def view(image):
    a = 104 #offset
    b = 10  #bounding box 
    #image = captured_.copy()
    image  = cv.rectangle(image , (0,0+a), (215,272+a), (255,0,0), 1)
    image  = cv.rectangle(image , (425,0+a), (640,272+a), (0,0,255), 1)
    image  = cv.rectangle(image , (215,0+a), (425,272+a), (0,255,0), 1)
    image  = cv.rectangle(image , (5+b,0+a+b), (215-b,210+a-b), (255,255,255), 1)
    image  = cv.rectangle(image , (425+b,0+a+b), (635-b,210+a-b), (255,255,255), 1)
    image  = cv.rectangle(image , (215+b,0+a+b), (425-b,210+a-b), (255,255,255), 1)

    # Display Capture Image to User
    cv.imshow('Captured',image)
    cv.waitKey(key) 
    cv.destroyAllWindows() 

# Set Properties
res_horizontal = 640
res_vertical = 480

# Subject Settings
id =  15
arr = []

# Find serial number (sn) of the jpg file or else set default as 1
list_item = os.listdir('img_capture/' + str(id))
for item in list_item:
    name,ext = os.path.splitext(item)
    start = name.find("(") + 1
    end = name.find(")")
    substring = name[start:end]
    arr.append(substring)

if(not arr):
    sn = 1
else:
    sn = int(max(arr)) + 1

print(str(sn))

# Path Setting
path = 'dataset/' + str(id) + '/'
num = 0
ext = 'jpg'
key = 0

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
    
    #view(output.array)

    # Saved Image file into respective directory and format
    name = str(id) + '(' + str(sn) + ')'
    cv.imwrite(path + name + '.' + ext,output.array)
    print('Successfully saved in: ' + path + name + '.' + ext)

    # Prompt User Ready For Next Capture or Exit Program
    code = str(input("Ready? Key In Any except '0' to exit\n"))
    if(code == '0'):
        exit()
    sn = sn + 1



'''
# Input a number
while True:
  try:
    code = int(input("Please enter name of file (In Code)\n"))
    if(code == 0):
        exit()
    if(len(str(code)) == 6):
        break
    print('Error: At least 6 digits')
  except ValueError:
    print("Please input integer only...")  
    continue

print("You have entered:", code)

i = 1
for digit in str(code):
    if(i == 1):
        mode_str = mode[int(digit)-1]
    if(i == 2):
        dist_str = str(dist[int(digit)-1])
    if(i == 3):
        light_str = light[int(digit)-1]
    if(i == 4):
        pos_str = pos[int(digit)-1]
    if(i == 5):
        offset_str = offset[int(digit)-1]
    if(i == 6):
        serial = str(int(digit))

    i = i + 1

name = mode_str + '_' + dist_str + '_' + light_str + '_' + pos_str + '_' + offset_str + '(' + serial + ')'

#print(name)
#name = 'test'
'''
    



