###########################################################################
# Subject: CZ3004 MDP Image Recognition 20/21
# Team: 22
# Contributor: Sam Jian Shen, Lin Yue
# Version: 1.0
###########################################################################
###########################################################################
# Object Detection Functions 
###########################################################################
# Import all required libraries
import os                                   # Interact with operating system
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'    # Suppress TensorFlow logging (1)
import time                                 # For tracking time purpose
from datetime import datetime               # Use current date time for filenames
import pathlib                              # Allow object-Oriented filesystem path
import tensorflow as tf                     # Tensorflow machine learning operation
import cv2 as cv                            # Use for image manipulation feature
import numpy as np                          # Manipulate matrix and datatype
from object_detection.utils import label_map_util                   # Object Detection Label Functions
from object_detection.utils import visualization_utils as viz_utils # Object Detection Visual Functions
# Used for machine learning in object detection
tf.get_logger().setLevel('ERROR')           # Suppress TensorFlow logging (2)

# Configuration
# Model Used
model = 'rgb_room'
Path_ABS = ''
PATH_TO_MODEL_DIR = Path_ABS + \
    'CZ3004_MDP_RPI_ImageRecognition/exported-models/my_mobilenet_model/rgb_room/'
# Provide path to label map
PATH_TO_LABELS = Path_ABS + 'CZ3004_MDP_RPI_ImageRecognition/exported-models/my_mobilenet_model/' + \
    model + '/saved_model/label_map.pbtxt'
# Provide the minimum confidence threshold
MIN_CONF_THRESH = float(0.90) # 90% and above
# Path to Result
PATH_TO_TEST_RESULT = Path_ABS + \
    'CZ3004_MDP_RPI_ImageRecognition/images/test/result/'
PATH_TO_RESULT = Path_ABS + \
    'CZ3004_MDP_RPI_ImageRecognition/images/process/[3] detection/'

# Read the trained model and convert into a function to be used for detections
def load_model():
    print('Tensorflow Version: ', tf.__version__)  # check tensorflow version
    # Enable GPU dynamic memory allocation
    gpus = tf.config.experimental.list_physical_devices('GPU')
    for gpu in gpus:
        tf.config.experimental.set_memory_growth(gpu, True)
    PATH_TO_SAVED_MODEL = PATH_TO_MODEL_DIR + "/saved_model"
    start_time = time.time()
    # Load saved model and build detection function
    detect_fn = tf.saved_model.load(PATH_TO_SAVED_MODEL)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print('Done! Took {} seconds\n'.format(elapsed_time))
    return detect_fn

# Execute detection algorithm with 3 partition
def detection(detect_fn, images_contour):
    index = 0
    list_result = []
    for image in images_contour:
        image_target = []
        image_rgb = cv.cvtColor(image, cv.COLOR_BGR2RGB)      # For RGB Detect
        # image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # For Gray Detect
        imH, imW, _ = image.shape
        image_expanded = np.expand_dims(image_rgb, axis=0)

        # The input needs to be a tensor, convert it using `tf.convert_to_tensor`.
        input_tensor = tf.convert_to_tensor(image)

        # The model expects a batch of images, so add an axis with `tf.newaxis`.
        input_tensor = input_tensor[tf.newaxis, ...]
        detections = detect_fn(input_tensor)

        # All outputs are batches tensors.
        # Convert to numpy arrays, and take index [0] to remove the batch dimension.
        # We're only interested in the first num_detections.
        num_detections = int(detections.pop('num_detections'))
        detections = {key: value[0, :num_detections].numpy()
                      for key, value in detections.items()}
        detections['num_detections'] = num_detections
        scores = detections['detection_scores']
        boxes = detections['detection_boxes']

        # detection_classes should be ints.
        detections['detection_classes'] = detections['detection_classes'].astype(
            np.int64)
        classes = detections['detection_classes']

        count_detect = 0
        maxscore = 0

        # Load Label Map data for plotting
        category_index = label_map_util.create_category_index_from_labelmap(
            PATH_TO_LABELS, use_display_name=True)

        # Find the best score
        for i in range(len(scores)):
            if ((scores[i] > MIN_CONF_THRESH) and (scores[i] <= 1.0) and (maxscore < scores[i])):
                index_maxscore = i
                count_detect += 1
                maxscore = scores[i]  # update new high score
                print('New Max Score = ' + str(maxscore))
        
        # If exist object get the necessary parameter for further process
        if(count_detect > 0):
            ymin = int(max(1, (boxes[index_maxscore][0] * imH)))
            xmin = int(max(1, (boxes[index_maxscore][1] * imW)))
            ymax = int(min(imH, (boxes[index_maxscore][2] * imH)))
            xmax = int(min(imW, (boxes[index_maxscore][3] * imW)))
            object_name = category_index[int(classes[index_maxscore])]['name']
            label = '%s: %d%%' % (object_name, int(
                scores[index_maxscore]*100))  # Example: 'person: 72%'
            labelSize, baseLine = cv.getTextSize(
                label, cv.FONT_HERSHEY_PLAIN, 1, 2)  # Get font size
            # Make sure not to draw label too close to top of window
            label_ymin = max(ymin, labelSize[1] + 10)
            # Debug Purpose
            # cv.rectangle(image, (xmin, label_ymin-labelSize[1]-10), (xmin+labelSize[0], label_ymin+baseLine-10), (0, 255, 0), cv.FILLED) # Draw green box to put label text in
            # cv.rectangle(image, (xmin, label_ymin-labelSize[1]-10), (xmin+labelSize[0] - 45, label_ymin+baseLine - 10), (0, 255, 0), cv.FILLED) # Draw green box to put label text in
            # cv2.putText(image, label, (xmin, label_ymin-7), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2) # Draw label text
            # cv.putText(image, object_name, (xmin, label_ymin-7), cv.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), 2) # Draw label text
            width = xmax - xmin
            height = ymax - ymin
            print('x = ', str(xmin), '\nw = ', str(width),
                  '\ny = ', str(ymin), '\nh = ', str(height))
            print(label)
            list_result.append(
                [xmin, ymin, width, height, label, object_name, index])

        print('Number of Object Detected: ', str(count_detect))
        # If Object Detect more than one
        if(count_detect > 1):
            print('[Warning] More Than 1 Object Detected')
        # If Object Detect None
        elif(count_detect < 1):
            print('[Warning] No Object Detected')
            list_result.append([0, 0, 0, 0, 'none', 'none', index])

        now = datetime.now()
        dt_string = now.strftime("%d%m%Y_%H%M%S_%f")
        # cv.imwrite(PATH_TO_TEST_RESULT +  str(index) + '.jpg', image) # Test Output
        cv.imwrite(PATH_TO_RESULT + dt_string + '_' +
                   str(index) + '.jpg', image)  # Official Output
        index += 1
    print('Object Detection Completed')
    return list_result

# Execute detection algorithm with 9 partition
def detection9(detect_fn, images_contour):
    index = 0  # for selecting the right image in the list of image
    index_pos = 0  # image position indicator start from left mid then right
    list_result = []
    index_detected = []  # for index of successful detection

    # for every partition
    for k in range(9):
        print('Running Index: ' + str(index))
        image = images_contour[index]
        image_target = []
        image_rgb = cv.cvtColor(image, cv.COLOR_BGR2RGB)      # For RGB Detect
        # image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # For Gray Detect
        imH, imW, _ = image.shape
        image_expanded = np.expand_dims(image_rgb, axis=0)

        # The input needs to be a tensor, convert it using `tf.convert_to_tensor`.
        input_tensor = tf.convert_to_tensor(image)

        # The model expects a batch of images, so add an axis with `tf.newaxis`.
        input_tensor = input_tensor[tf.newaxis, ...]
        detections = detect_fn(input_tensor)

        # All outputs are batches tensors.
        # Convert to numpy arrays, and take index [0] to remove the batch dimension.
        # We're only interested in the first num_detections.
        num_detections = int(detections.pop('num_detections'))
        detections = {key: value[0, :num_detections].numpy()
                      for key, value in detections.items()}
        detections['num_detections'] = num_detections
        scores = detections['detection_scores']
        boxes = detections['detection_boxes']

        # Detection_classes should be ints.
        detections['detection_classes'] = detections['detection_classes'].astype(
            np.int64)
        classes = detections['detection_classes']

        count_detect = 0
        maxscore = 0
        # Load Label Map data for plotting
        category_index = label_map_util.create_category_index_from_labelmap(
            PATH_TO_LABELS, use_display_name=True)

        # Find the best score
        for i in range(len(scores)):
            if ((scores[i] > MIN_CONF_THRESH) and (scores[i] <= 1.0) and (maxscore < scores[i])):
                index_maxscore = i
                count_detect += 1
                maxscore = scores[i]  # update new high score
                print('New Max Score = ' + str(maxscore))

        # If exist object detected
        if(count_detect > 0):
            # Get bounding box coordinates and draw box
            # Interpreter can return coordinates that are outside of image dimensions, need to force them to be within image using max() and min()
            ymin = int(max(1, (boxes[index_maxscore][0] * imH)))
            xmin = int(max(1, (boxes[index_maxscore][1] * imW)))
            ymax = int(min(imH, (boxes[index_maxscore][2] * imH)))
            xmax = int(min(imW, (boxes[index_maxscore][3] * imW)))
            object_name = category_index[int(classes[index_maxscore])]['name']
            label = '%s: %d%%' % (object_name, int(
                scores[index_maxscore]*100))  # Example: 'person: 72%'
            labelSize, baseLine = cv.getTextSize(
                label, cv.FONT_HERSHEY_PLAIN, 1, 2)  # Get font size
            # Make sure not to draw label too close to top of window
            label_ymin = max(ymin, labelSize[1] + 10)

            # Debug Purpose
            # cv.rectangle(image, (xmin, label_ymin-labelSize[1]-10), (xmin+labelSize[0], label_ymin+baseLine-10), (0, 255, 0), cv.FILLED) # Draw green box to put label text in
            # cv.rectangle(image, (xmin, label_ymin-labelSize[1]-10), (xmin+labelSize[0] - 45, label_ymin+baseLine - 10), (0, 255, 0), cv.FILLED) # Draw green box to put label text in
            # cv2.putText(image, label, (xmin, label_ymin-7), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2) # Draw label text
            # cv.putText(image, object_name, (xmin, label_ymin-7), cv.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), 2) # Draw label text
            width = xmax - xmin
            height = ymax - ymin
            print('x = ', str(xmin), '\nw = ', str(width),
                  '\ny = ', str(ymin), '\nh = ', str(height))
            print(label)

        print('Number of Object Detected: ', str(count_detect))

        # If Object Detect more than one
        if(count_detect > 1):
            print('[Warning] More Than 1 Object Detected')

        # If Object Detect None
        elif(count_detect < 1):
            print('[Warning] No Object Detected')

        # cv.imwrite(PATH_TO_TEST_RESULT +  str(index) + '.jpg', image) # Test Output

        now = datetime.now()
        dt_string = now.strftime("%d%m%Y_%H%M%S_%f")
        cv.imwrite(PATH_TO_RESULT + dt_string + '_ ' + str(index_pos) +
                   '.jpg', image)  # Official Output

        # Control the index which one to process, worst case all 9 partition, best case 3 partition
        if(index == 8):
            if(count_detect < 1):
                list_result.append(
                    [0, 0, 0, 0, 'none', 'none', index_pos, index])
                index_detected.append(-1)
            else:
                list_result.append(
                    [xmin, ymin, width, height, label, object_name, index_pos, index])
                index_detected.append(index)
            break
        elif(count_detect >= 1):
            if(index == 0 or index == 1 or index == 2):
                list_result.append(
                    [xmin, ymin, width, height, label, object_name, index_pos, index])
                index_detected.append(index)
                index_pos += 1
                index = 3  # set index to next position
            elif(index == 3 or index == 4 or index == 5):
                list_result.append(
                    [xmin, ymin, width, height, label, object_name, index_pos, index])
                index_detected.append(index)
                index_pos += 1
                index = 6  # set index to next position
            elif(index == 6 or index == 7 or index == 8):
                list_result.append(
                    [xmin, ymin, width, height, label, object_name, index_pos, index])
                index_detected.append(index)
                break
        elif(index == 2 or index == 5):
            list_result.append([0, 0, 0, 0, 'none', 'none', index_pos, index])
            index_detected.append(-1)
            index_pos += 1
            index += 1
        else:
            index += 1

    print('Object Detection Completed')
    return [list_result, index_detected]
