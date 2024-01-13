###########################################################################
# Subject: CZ3004 MDP Image Recognition 20/21
# Team: 22
# Contributor: Sam Jian Shen, Lin Yue
# Version: 1.0
###########################################################################
###########################################################################
# Extract Crop Images for Dataset and ability to prompt user to choose.
###########################################################################
# Import various libraries 
import cv2 as cv 
import re
import os

# Path Setting
path_src = 'img_capture/'
path_dst_w = 'img_crop/white/'
path_dst_c = 'img_crop/card/'
id = 1 # manually change ID
#index = 1
num = 0
ext = 'jpg' #image format
key = 0

# Image Setting
x_left  = 15  # top left of left crop
x_mid   = 225 # top left of mid crop
x_right = 435 # top left of right crop
y       = 138 # calibrated y value
w       = 190 # width and height (same value)
p       = 16  # padding (padding need to keep adjust for different distance)

# Checking Cropping with respect to origin image
def view(image, image_crop, image_contour):
    image  = cv.rectangle(image , (x_left,y), (x_left+w,y+w), (255,255,255), 1)
    image  = cv.rectangle(image, (x_mid,y), (x_mid+w,y+w), (255,255,255), 1)
    image  = cv.rectangle(image , (x_right,y), (x_right+w,y+w), (255,255,255), 1)
    cv.imshow('Ref Image',image)
    cv.imshow('Crop Image',image_crop)
    cv.imshow('Contour Image',image_contour)
    cv.waitKey(key)
    cv.destroyAllWindows() 

# Crop with Contour
def contour(image):
    # Grayscale
    global p

    while True:
        image_gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY) 

        # Apply Canny
        image_canny = cv.Canny(image_gray, 30, 200) 

        # Finding Contours 
        contours, heir = cv.findContours(image_canny, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

        # Find the highest yield contours (proximity connected dots)
        c = max(contours, key = cv.contourArea)

        # Extract the extreme points which form rectangle
        xc,yc,wc,hc = cv.boundingRect(c)

        # Contour Image with Padding

        # Check Out Of Boundary Case
        if(yc-p < 0):
            y1 = 0
        else:
            y1 = yc - p
        if(yc+wc+p > 480):
            y1_w = 480
        else:
            y1_w = yc + wc+ p 
        if(xc-p < 0):
            x1 = 0
        else:
            x1 = xc - p
        if(xc+wc+p > 640):
            x1_w = 640
        else:
            x1_w = xc + wc+ p 
        
        #image_contour = image_process[yc-p:yc+wc+p, xc-p:xc+wc+p]
        image_contour = image_process[y1:y1_w, x1:x1_w]
        print('Press ', str(key) , ' to exit')
        cv.imshow('Contour Image',image_contour)
        cv.waitKey(key)
        cv.destroyAllWindows() 
        try:
            ans = int(input("Ok!? Key in 0 to continue or key in any integer value to set the padding (default = " + str(p) +" )\n"))
        except:
            print('Please key again')
        if(ans == 0):
            break
        else:
            p = ans
    
    return image_contour

# Choosing the right crop images for model's dataset
while True:
    # Get Index
    while True:
        try:
            index = int(input("Index: \n"))
            break
        except:
            print('Please Try Again')

    fullpath_src = 'CZ3004_MDP_RPI_ImageRecognition/' +  path_src + str(id) + '/' + str(id) + '(' + str(index) + ').' + ext

    # Target
    image = cv.imread('11(2).jpg') 
    cv.imshow('Preview',image)
    cv.waitKey(key)
    cv.destroyAllWindows() 
    #print(image)
    # Image Crop Target
    while True:
        pos = str(input("Choose target position\n[1] left\n[2] mid\n[3] right\n"))
        if(pos == '1' or pos == '2' or pos == '3'):
            break
        else:
            print('Please try again')

    image_process = image.copy()
    if(pos == '1'):
        image_crop = image_process[y:y+w, x_left:x_left+w].copy() #img[y:y+h, x:x+w]
    if(pos == '2'):
        image_crop = image_process[y:y+w, x_mid:x_mid+w].copy()
    if(pos == '3'):
        image_crop = image_process[y:y+w, x_right:x_right+w].copy()

    image_contour = contour(image).copy()
    #view(image, image_crop, image_contour)
    #name = str(input("Please key in your processed image name to be saved!\n"))
    name_w = str(id) + '_w(' + str(index) + ')'
    name_c = str(id) + '_c(' + str(index) + ')'
    fullpath_dst = 'CZ3004_MDP_RPI_ImageRecognition/' +  path_dst_c + name_c + '.' + ext
    fullpath_dst_w = 'CZ3004_MDP_RPI_ImageRecognition/' +  path_dst_w + name_w + '.' + ext
    print('Image (Single Classifier) Saved Successfully to: ', fullpath_dst)
    print('Image (White Crop) Saved Successfully to: ', fullpath_dst_w)
    cv.imwrite(fullpath_dst, image_contour)
    cv.imwrite(fullpath_dst_w, image_crop)

    end = str(input("Key any to continue, Key 0 to end \n"))
    if(end == '0'):
        break

print('Program Terminated Successfully')

