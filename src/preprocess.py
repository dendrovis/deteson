###########################################################################
# Subject: CZ3004 MDP Image Recognition 20/21
# Team: 22
# Contributor: Sam Jian Shen, Lin Yue
# Version: 1.0
###########################################################################
###########################################################################
# Pre Process Functions
###########################################################################
# Import necessary libaries
import cv2 as cv                            # Use for image manipulation feature
import numpy as np                          # Image enhancement purpose
import math as m                            # Complex to simple calculation
from datetime import datetime               # Keep track of current time for contour filenames
import glob                                 # Read, Write directories
import os                                   # Read, Write directories
import shutil                               # Copy Images to another directories
import time                                 # Keep track of time, delay time and file creation time


# Settings for all X,Y coordinates
p = 20  # padding value

# 3 partition
left_box_left_x = 15
left_box_right_x = 205
middle_box_left_x = 225
middle_box_right_x = 415
right_box_left_x = 435
right_box_right_x = 625

# 9 partition
# middle crop
left_box_left_x_middle = 15
middle_box_left_x_middle = 225
right_box_left_x_middle = 435
# left crop
left_box_left_x_left = 0
middle_box_left_x_left = 210
right_box_left_x_left = 420
# right crop
left_box_left_x_right = 30
middle_box_left_x_right = 240
right_box_left_x_right = 450
upper_y = 230  # 130
lower_y = 420  # 320

# Re-read same file chance before discard or skip
limit = 3

# Initial declaration
skip_file_list = []
path_to_sourceImg = "Z://" # Read from RPI
#path_to_sourceImg = 'CZ3004_MDP_RPI_ImageRecognition/images/input/' # Read Locally
path_to_contour = 'CZ3004_MDP_RPI_ImageRecognition/images/process/[2] contour/'
path_to_raw = 'CZ3004_MDP_RPI_ImageRecognition/images/process/[0] input/'
path_to_partition = 'CZ3004_MDP_RPI_ImageRecognition/images/process/[1] partition/'

# Read input images discard or skip if not readable or catched error during OS operation
def read_input():
    global skip_file_list 
    limit_i = 0
    img_loaded = False
    while True:
        if (img_loaded == True):
            break
        print('Loading Image')
        time.sleep(1)
        file_list = []
        file_create_time = []
        earliest_file_index = 0
        skip_count = 0
        for filename in os.listdir(path_to_sourceImg):
            if(skip_file_list.count(filename) >= 1): # exist 1 in the skip list
                print('Skipping File: ' + filename)
                skip_count += 1
                if(len(os.listdir(path_to_sourceImg)) == skip_count):
                    print('Remain All Skip Files, Waiting for anymore...')
                    image = []
                    return [image, None]
                continue
            file_earliest_time = os.stat(path_to_sourceImg + filename).st_ctime_ns #get file creation time in ns
            file_list.append(filename) #filenames list
            file_create_time.append(file_earliest_time) #file creation time list in ns
            print(file_earliest_time)
        earliest_file_index = file_create_time.index(min(file_create_time)) #get earliest index of the file
        fname = file_list[earliest_file_index]
        print('Processing: ' + fname)
        img_name = fname.replace('.jpg', '')
        print('Removing Extension: ' + str(img_name))
        try:
            shutil.copyfile(path_to_sourceImg + fname,
                            path_to_raw + fname)
        except Exception as e:
            print(e)
            image = []
            skip_file_list.append(fname)
            return [image, None]
        image = cv.imread(path_to_raw + fname)
        if(img_name == "dummy"):
            try:
                os.remove(path_to_sourceImg + fname)
            except Exception as e:
                image = []
                skip_file_list.append(fname)
                print(e)
            return [image, None]

        name_array = img_name.split(',')

        if image is None:
            print('Error Image Return None ' + str(limit_i))
            if(limit_i >= limit):
                try:
                    os.remove(path_to_sourceImg + fname)
                except Exception as e:
                    image = []
                    skip_file_list.append(fname)
                    print(e)
                print("Read failed! Image removed!!")
                skip_file_list.append(fname)
                return [image, None]
            limit_i += 1
        else:
            print('Removing: ' + fname)
            try:
                os.remove(path_to_sourceImg + fname)
            except Exception as e:
                skip_file_list.append(fname)
                print(e)
            break
    return [image, name_array]

# Partition Image into 3
def partition(image):  
    image_left = image[upper_y:lower_y, left_box_left_x:left_box_right_x]
    image_mid = image[upper_y:lower_y, middle_box_left_x:middle_box_right_x]
    image_right = image[upper_y:lower_y, right_box_left_x:right_box_right_x]
    image_partition = [image_left, image_mid, image_right]
    coordinates = [[left_box_left_x, upper_y],
                   [middle_box_left_x, upper_y],
                   [right_box_left_x, upper_y]]
    return [coordinates, image_partition]

# Partition Image into 9
def partition9(image): 
    image_left_1 = image[upper_y:lower_y,
                         left_box_left_x_middle:left_box_left_x_middle + 190]
    image_mid_1 = image[upper_y:lower_y,
                        middle_box_left_x_middle:middle_box_left_x_middle + 190]
    image_right_1 = image[upper_y:lower_y,
                          right_box_left_x_middle:right_box_left_x_middle + 190]

    image_left_0 = image[upper_y:lower_y,
                         left_box_left_x_left:left_box_left_x_left + 190]
    image_mid_0 = image[upper_y:lower_y,
                        middle_box_left_x_left:middle_box_left_x_left + 190]
    image_right_0 = image[upper_y:lower_y,
                          right_box_left_x_left:right_box_left_x_left + 190]

    image_left_2 = image[upper_y:lower_y,
                         left_box_left_x_right:left_box_left_x_right + 190]
    image_mid_2 = image[upper_y:lower_y,
                        middle_box_left_x_right:middle_box_left_x_right + 190]
    image_right_2 = image[upper_y:lower_y,
                          right_box_left_x_right:right_box_left_x_right + 190]
    '''
    # Debug purpose
    now = datetime.now()
    dt_string = now.strftime("%d%m%Y_%H%M%S_%f")
    
    cv.imwrite(path_to_partition + dt_string +
               '_left_partition_left_crop.jpg', image_left_0)
    cv.imwrite(path_to_partition + dt_string +
               '_left_partition_mid_crop.jpg', image_left_1)
    cv.imwrite(path_to_partition + dt_string +
               '_left_partition_right_crop.jpg', image_left_2)

    cv.imwrite(path_to_partition + dt_string +
               '_mid_partition_left_crop.jpg', image_mid_0)
    cv.imwrite(path_to_partition + dt_string +
               '_mid_partition_mid_crop.jpg', image_mid_1)
    cv.imwrite(path_to_partition + dt_string +
               '_mid_partition_right_crop.jpg', image_mid_2)

    cv.imwrite(path_to_partition + dt_string +
               '_right_partition_left_crop.jpg', image_right_0)
    cv.imwrite(path_to_partition + dt_string +
               '_right_partition_mid_crop.jpg', image_right_1)
    cv.imwrite(path_to_partition + dt_string +
               '_right_partition_right_crop.jpg', image_right_2)
    '''
    image_partition = [image_left_1, image_left_0, image_left_2, image_mid_1,
                       image_mid_0, image_mid_2, image_right_1, image_right_0, image_right_2]
    coordinates = [[left_box_left_x_middle,   upper_y],
                   [left_box_left_x_left,    upper_y],
                   [left_box_left_x_right,   upper_y],
                   [middle_box_left_x_middle, upper_y],
                   [middle_box_left_x_left,  upper_y],
                   [middle_box_left_x_right, upper_y],
                   [right_box_left_x_middle, upper_y],
                   [right_box_left_x_left,   upper_y],
                   [right_box_left_x_right,  upper_y]]
    return [coordinates, image_partition]

# Enhance Image Contrast
def image_enhancement(img, alpha, beta):
    return cv.addWeighted(img, alpha, np.zeros(img.shape, img.dtype), 0, beta)


# Enhancement and Contour Image
def contour(image):
    print('Contouring Image(s)...')

    # Convert to Grayscale
    image_gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

    # Enhancement Image Adjustment
    image_enhance = image_enhancement(image, 5, 0)

    # Apply Canny
    image_canny = cv.Canny(image_gray, 30, 200)

    # Finding Contours
    contours, heir = cv.findContours(
        image_canny, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    # Find the highest yield contours (proximity connected dots) # if none should throw except
    try:
        c = max(contours, key=cv.contourArea)

        # Extract the extreme points which form rectangle
        xc, yc, wc, hc = cv.boundingRect(c)

        image_rgb = cv.cvtColor(image_canny, cv.COLOR_GRAY2RGB).copy()
        cv.rectangle(image_rgb, (xc, yc), (xc+wc, yc+hc), (0, 0, 255))

        # Add Padding
        y = yc - p
        h = hc + 2*p
        p_y = m.floor((h - wc) / 2)
        x = xc - p_y

        # Measure origin dimension
        origin_h = image.shape[0]
        #origin_w = image.shape[1]

        # Condition if reached corner
        if(x+h > origin_h):
            #h =  origin_h - x
            x = x - ((x + h) - origin_h)

        if(y+h > origin_h):
            y = y - ((y + h) - origin_h)
        if(x < 0):
            x = 0
        if(y < 0):
            y = 0

        cv.rectangle(image_rgb, (x, y), (x+h, y+h), (0, 255, 255))
        image_contour = image[y:y+h, x:x+h].copy()  # img[y:y+h, x:x+w]
        now = datetime.now()
        dt_string = now.strftime("%d%m%Y_%H%M%S_%f")
        cv.imwrite(path_to_contour + dt_string + '.jpg', image_rgb)

    except:
        print('No Contour')
        return image

    return image_contour
