###########################################################################
# Subject: CZ3004 MDP Image Recognition 20/21
# Team: 22
# Contributor: Sam Jian Shen, Lin Yue
# Version: 1.0
###########################################################################
###########################################################################
# Post Process Functions
###########################################################################
# Import necessary libaries
import cv2 as cv                     # Plotting and Image display, read and write
from datetime import datetime        # Get current date time for result image
#import random as rand                # Generate random color for plotting (Discarded)
import glob                          # Read directories
from PIL import Image                # Tiling Image operation

Path_ABS = ''
path_to_output = Path_ABS + 'CZ3004_MDP_RPI_ImageRecognition/images/output/'
path_to_outputT = Path_ABS + 'CZ3004_MDP_RPI_ImageRecognition/images/output_target/'
path_to_tile = Path_ABS + 'CZ3004_MDP_RPI_ImageRecognition/images/result/'
separator = ','
correct_coordinate = []

# Plotting for 3 partition mode
def plot(list_result, image_raw, coordinates, image_name, data_output):
    print('Plotting over RAW Image')
    i = 0
    toggle_save_img = False
    now = datetime.now()
    dt_string = now.strftime("%d%m%Y_%H%M%S_%f")
    image_output = image_raw.copy()
    for coordinate in coordinates:
        print('Plotting Index: ', i)
        print(list_result[i])
        # b = rand.randint(100, 255)
        # g = rand.randint(100, 255)
        # r = rand.randint(100, 255)
        x, y = coordinate
        xmin, ymin, width, height, label, object_name, index = list_result[i]
        if(object_name != 'none'):
            correct_coordinate = coordinate
            cv.rectangle(image_output, (x + xmin, y + ymin),
                         (x + xmin + width, y + ymin + height), (0, 255, 0), 2)
            labelSize, baseLine = cv.getTextSize(
                label, cv.FONT_HERSHEY_PLAIN, 1, 2)  # Get font size

            # Make sure not to draw label too close to top of window
            label_ymin = max(y + ymin, labelSize[1] + 10)

            # Draw green box to put label text in
            cv.rectangle(image_output, (x + xmin, label_ymin-labelSize[1]-10), (
                x + xmin+labelSize[0] - 45, label_ymin+baseLine - 10), (0, 255, 0), cv.FILLED)
            cv.putText(image_output, object_name, (x + xmin, label_ymin-7),
                       cv.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), 2)  # Draw label text
            toggle_save_img = True

        i += 1

    # Write the image output filename according to image string
    if(toggle_save_img == True):
        print('Image Plotted Sucessfully!')
        if(correct_coordinate[0] == 15):
            output_name = [data_output[0][0], int(
                image_name[0]), int(image_name[1])]
            output_string = ', '.join([str(elem)
                                       for elem in output_name])
        elif(correct_coordinate[0] == 225):
            output_name = [data_output[1][0], int(
                image_name[2]), int(image_name[3])]
            output_string = ', '.join([str(elem)
                                       for elem in output_name])
        else:
            output_name = [data_output[2][0], int(
                image_name[4]), int(image_name[5])]
            output_string = ', '.join([str(elem)
                                       for elem in output_name])
        cv.imwrite(path_to_output + output_string + '.jpg', image_output)
    else:
        print('Image Does Not Detect Any!')

# Plotting for 9 partition mode
def plot9(list_result, image_raw, coordinates, image_name):
    print('Plotting over RAW Image')
    toggle_save_img = False
    now = datetime.now()
    dt_string = now.strftime("%d%m%Y_%H%M%S_%f")
    image_output = image_raw.copy()
    result, indexes = list_result
    for obj in result:
        xmin, ymin, width, height, label, object_name, index_pos, index = obj
        x, y = coordinates[index]
        if(object_name != 'none'):
            cv.rectangle(image_output, (x + xmin, y + ymin),
                         (x + xmin + width, y + ymin + height), (0, 255, 0), 2)
            labelSize, baseLine = cv.getTextSize(
                label, cv.FONT_HERSHEY_PLAIN, 1, 2)  # Get font size

            # Make sure not to draw label too close to top of window
            label_ymin = max(y + ymin, labelSize[1] + 10)

            # Draw green box to put label text in
            cv.rectangle(image_output, (x + xmin, label_ymin-labelSize[1]-10), (
                x + xmin+labelSize[0] - 45, label_ymin+baseLine - 10), (0, 255, 0), cv.FILLED)
            cv.putText(image_output, object_name, (x + xmin, label_ymin-7),
                       cv.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), 2)  # Draw label text
            toggle_save_img = True
    if(toggle_save_img == True):
        print('Image Plotted Sucessfully!')
        name_string = ', '.join([str(elem) for elem in image_name])
        cv.imwrite(path_to_output + name_string + '.jpg', image_output)
    else:
        print('Image Does Not Detect Any!')

# Output for 3 partition mode, bind all the labels
def output(list_result):
    output = []
    print(list_result)
    for obj in list_result:
        xmin, ymin, width, height, label, object_name, index = obj
        id = -1  # indicate some error happen
        if(object_name == 'none'):
            id = 0
        elif(object_name == 'up arrow'):
            id = 1
        elif(object_name == 'down arrow'):
            id = 2
        elif(object_name == 'right arrow'):
            id = 3
        elif(object_name == 'left arrow'):
            id = 4
        elif(object_name == 'Go'):
            id = 5
        elif(object_name == 'six'):
            id = 6
        elif(object_name == 'seven'):
            id = 7
        elif(object_name == 'eight'):
            id = 8
        elif(object_name == 'nine'):
            id = 9
        elif(object_name == 'zero'):
            id = 10
        elif(object_name == 'Alphabet V'):
            id = 11
        elif(object_name == 'Alphabet W'):
            id = 12
        elif(object_name == 'Alphabet X'):
            id = 13
        elif(object_name == 'Alphabet Y'):
            id = 14
        elif(object_name == 'Alphabet Z'):
            id = 15
        output.append([id, index])  # index is position (left,mid,right)
    return output

# Output for 9 partition mode, bind all the labels
def output9(list_result):
    output = []
    result, indexing = list_result
    print(list_result)
    print(result)
    for obj in result:
        xmin, ymin, width, height, label, object_name, index_pos, index = obj
        id = -1  # indicate some error happen
        if(object_name == 'none'):
            id = 0
        elif(object_name == 'up arrow'):
            id = 1
        elif(object_name == 'down arrow'):
            id = 2
        elif(object_name == 'right arrow'):
            id = 3
        elif(object_name == 'left arrow'):
            id = 4
        elif(object_name == 'Go'):
            id = 5
        elif(object_name == 'six'):
            id = 6
        elif(object_name == 'seven'):
            id = 7
        elif(object_name == 'eight'):
            id = 8
        elif(object_name == 'nine'):
            id = 9
        elif(object_name == 'zero'):
            id = 10
        elif(object_name == 'Alphabet V'):
            id = 11
        elif(object_name == 'Alphabet W'):
            id = 12
        elif(object_name == 'Alphabet X'):
            id = 13
        elif(object_name == 'Alphabet Y'):
            id = 14
        elif(object_name == 'Alphabet Z'):
            id = 15
        output.append([id, index_pos])  # index is position (left,mid,right)
    return output

# for every image in the img/output, combine them into one, return output with 1 jpg image
def tile():
   
    path = glob.glob(path_to_outputT + "/*.*")
    cv_img = []
    for img in path:
        image = Image.open(img)
        cv_img.append(image)
    no_of_images = len(cv_img)
    # plt.figure()
    # f, axarr = plt.subplots(2, no_of_images+1)
    if(len(cv_img) == 1):
        image_tile = cv_img[0]
    else:
        upper_image_tile = cv_img[0]
        lower_image_tile = cv_img[len(cv_img)//2]
        for i in range(1, len(cv_img)//2, 1):
            upper_image_tile = get_concat_h(upper_image_tile, cv_img[i])
        for i in range((len(cv_img)//2)+1, len(cv_img), 1):
            lower_image_tile = get_concat_h(lower_image_tile, cv_img[i])
        image_tile = get_concat_v_blank(
            upper_image_tile, lower_image_tile, (0, 0, 0))
    now = datetime.now()
    dt_string = now.strftime("%d%m%Y_%H%M%S_%f")
    image_tile.save(path_to_tile + dt_string + '.jpg')
    return path_to_tile + dt_string + '.jpg'

# tile operation
def get_concat_h(im1, im2):
    dst = Image.new('RGB', (im1.width + im2.width, im1.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (im1.width, 0))
    return dst

# tile operation
def get_concat_v_blank(im1, im2, color=(0, 0, 0)):
    dst = Image.new('RGB', (max(im1.width, im2.width),
                            im1.height + im2.height), color)
    dst.paste(im1, (0, 0))
    dst.paste(im2, (0, im1.height))
    return dst
