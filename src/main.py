###########################################################################
# Subject: CZ3004 MDP Image Recognition 20/21
# Team: 22
# Contributor: Sam Jian Shen, Lin Yue
# Version: 1.0
###########################################################################
###########################################################################
# This is the main file that consist of all the functions of IR
###########################################################################
# Import other python files
from postprocess import *
from model import *
from preprocess import *

# Libraries used
import os           # Read and Write Files
import cv2 as cv    # Show Image for Tile
import time         # Time delay and Time Tracking
import socket       # TCP/IP Connection

# Import samba
from smb import *   # Get all Samba Libraries
import urllib       # URL Libraries for Samba
from smb.SMBHandler import SMBHandler # Samba Handler
opener = urllib.request.build_opener(SMBHandler)

# Import other custom python functions
images = []
images_contour = []
count = 0
limit = 0
index = 0
i = 0
final_image_list = []
test_mode = 'organise'
path_test = 'CZ3004_MDP_RPI_ImageRecognition/images/test/' + test_mode
path_contour = 'CZ3004_MDP_RPI_ImageRecognition/images/test/contour/'
path_imgData = 'CZ3004_MDP_RPI_ImageRecognition/shared_data/imgdata_output.p'

# Data Read and Write Directories
path_imgInputs = 'CZ3004_MDP_RPI_ImageRecognition/images/input/'
path_imgOutputs = 'CZ3004_MDP_RPI_ImageRecognition/images/output/'
path_imgOutputsT = 'CZ3004_MDP_RPI_ImageRecognition/images/output_target/'
path_imgResult = 'CZ3004_MDP_RPI_ImageRecognition/images/result/'

# User settings
num_partition = 3  # 3 or 9
set_clear_data = False
allow_connection = False
path_imgSource = 'Z://' # Read Images with RPI
#path_imgSource = 'CZ3004_MDP_RPI_ImageRecognition/images/input/' #Read Images Locally
model_on = True


# Clear all Read and Write Directories
if(set_clear_data == True):
    print('Checking Data...')
    for item in os.listdir(path_imgSource):
        os.remove(path_imgSource + item)
        print('Removing Source Image: ' + item)
    for item in os.listdir(path_imgInputs):
        os.remove(path_imgInputs + item)
        print('Removing Input Image: ' + item)
    for item in os.listdir(path_imgOutputs):
        os.remove(path_imgOutputs + item)
        print('Removing Output Image: ' + item)
    for item in os.listdir(path_imgOutputsT):
        os.remove(path_imgOutputsT + item)
        print('Removing Target Output Image: ' + item)
    # for item in os.listdir(path_imgResult):
    #    os.remove(path_imgResult + item)
    #    print('Removing Result Image: ' + item)

# Established Connection to RPI using TCP/IP
class Connection:
    def __init__(self):
        if(allow_connection == True):
            self.socket = 0
            self.host = '192.168.22.1'
            self.port = 9990
        else:
            print('[Warning] Connection Disabled')

    def connect_to_rpi(self):
        if(allow_connection == True):
            while(self.socket == 0):
                try:
                    print("Attempting  to Connect...")
                    self.socket = socket.create_connection(
                        (self.host, self.port))
                except:
                    print("Connection refused. Trying again in 2 seconds")
                    time.sleep(2)
            print("Connected successfully")
        else:
            print('[Warning] Connection Disabled')

    def send_to_rpi(self, message):
        if(allow_connection == True):
            try:
                self.socket.sendall(message)
            except Exception as e:
                print(e)
        else:
            print('[Warning] Connection Disabled')

    def close_connection(self):
        if(allow_connection == True):
            self.socket.close()
        else:
            print('[Warning] Connection Disabled')

    def get_socket_instance(self):
        if(allow_connection == True):
            return self.socket
        else:
            print('[Warning] Connection Disabled')

# Load Output Files for Tiling
def load_images_filename_from_folder(folder):
    images = []
    flist = []
    for filename in os.listdir(folder):
        img = cv.imread(os.path.join(folder, filename))
        if img is not None:
            images.append(img)
            filename = filename.replace('.jpg', '')
            filename = filename.replace(' ', '')
            flist.append(filename)
            print("Added")
            print(filename)
    return images, flist


def main():
    
    # Debug Purpose
    # items = test_loadall_imgdata(path_imgData)
    # for item in items:
    #    print(item)
    # test_contour()
    # test_detection()
    # test_plot()
    
    # Initialize
    global count, limit, i, key
    print('Initialising Image Recognition Process...')

    # Invoke TCP/IP Connection
    connection_rpi = Connection()
    connection_rpi.connect_to_rpi()
    print('Loading Model...')
    if(model_on == True):
        time.sleep(45)
        detect_fn = load_model()
    else:
        print('[Warning] Model Not Activated')
    try:
        print('Start')
        while True:
            # print('Waiting...')
            # If exist more than 1 file in image source 
            while(len(os.listdir(path_imgSource)) > 0):
                print('Item(s) Found: ' + str(len(os.listdir(path_imgSource))))
                start_time = time.time()
                print('[0] Reading RAW Image...')
                image_raw_and_name = read_input()

                # If images is not read correctly or out of grid skip to next iteration
                if(image_raw_and_name[1] == None or model_on != True or image_raw_and_name[0] == []):
                    continue
                if(int(image_name[0]) > 14 or int(image_name[2]) > 14 or int(image_name[4]) > 14):
                    print("out of grid")
                    continue
                elif(int(image_name[1]) > 19 or int(image_name[3]) > 19 or int(image_name[5]) > 19):
                    print("out of grid")
                    continue
                elif(int(image_name[0]) < 0 or int(image_name[1]) < 0 or int(image_name[2]) < 0 or int(image_name[3]) < 0 or int(image_name[4]) < 0 or int(image_name[5]) < 0):
                    print("out of grid")
                    continue
                image_raw = image_raw_and_name[0]
                image_name = image_raw_and_name[1]
                print(image_name)

                # Arena Coordinates Adjustment
                image_name[1] = str(19 - int(image_name[1]))
                image_name[3] = str(19 - int(image_name[3]))
                image_name[5] = str(19 - int(image_name[5]))
                print(image_name)

                # Run 9 Partition Detection
                if(num_partition == 9):
                    print('[1] Partitioning Image...\n')
                    image_partitions = partition9(image_raw)
                    coordinates, image_partition = image_partitions
                    print('[2] Processing Object Detection...')
                    list_result = detection9(detect_fn, image_partitions[1])
                    data_output = output9(list_result)
                    print(data_output)
                    print('[3] Plotting Object...')
                    image_output = plot9(
                        list_result, image_raw, coordinates, image_name, data_output)
                    end_time = time.time()
                    elapsed_time = end_time - start_time
                    print(':))) Took {} seconds\n'.format(elapsed_time))

                # Run 3 Partition Detection
                else:
                    print('[1] Partitioning Image...\n')
                    image_partitions = partition(image_raw)
                    coordinates, image_partition = image_partitions
                    print('[2] Processing Object Detection...')
                    list_result = detection(detect_fn, image_partitions[1])
                    data_output = output(list_result)
                    print(data_output)
                    print('[3] Plotting Object...')
                    image_output = plot(
                        list_result, image_raw, coordinates, image_name, data_output)
                    end_time = time.time()
                    elapsed_time = end_time - start_time
                    print(':))) Took {} seconds\n'.format(elapsed_time))

                # Generate Image String if detected object
                if(data_output[0][0] > 0):
                    image_string = [data_output[0][0],
                                    int(image_name[0]), int(image_name[1])]
                    image_string = ', '.join([str(elem)
                                              for elem in image_string])
                    print(image_string)
                    connection_rpi.send_to_rpi(image_string.encode('UTF-8'))
                    final_image_list.append(image_string)
                elif(data_output[1][0] > 0):
                    image_string = [data_output[1][0], int(
                        image_name[2]), int(image_name[3])]
                    image_string = ', '.join([str(elem)
                                              for elem in image_string])
                    print(image_string)
                    connection_rpi.send_to_rpi(image_string.encode('UTF-8'))
                    final_image_list.append(image_string)
                elif(data_output[2][0] > 0):
                    image_string = [data_output[2][0], int(
                        image_name[4]), int(image_name[5])]
                    image_string = ', '.join([str(elem)
                                              for elem in image_string])
                    print(image_string)
                    connection_rpi.send_to_rpi(image_string.encode('UTF-8'))
                    final_image_list.append(image_string)

    # press ctrl-c to break while loop
    except KeyboardInterrupt:
        pass

    # Show all detected image string
    print('REF')
    print(final_image_list)

    # Get final image string from RPI and Tile them
    try:
        result_list = []      # final final image string
        result_img = []       # Store all image(s) in array form
        print('Populate Image List')
        images, filenames = load_images_filename_from_folder(
            path_imgOutputs)  # all the files
        print(filenames)
        print('Populate Image String')
        final_image_string = connection_rpi.get_socket_instance().recv(1024)
        print(final_image_string)
        final_image_string = final_image_string.replace(' ', '')
        final_image_string = final_image_string.split(',')
        while(len(final_image_string) != 0):
            result_list.append(str(final_image_string[0]) + ',' + str(
                final_image_string[1]) + ',' + str(final_image_string[2]))
            final_image_string.pop(0)
            final_image_string.pop(0)
            final_image_string.pop(0)
        print(result_list)
        for result in result_list:
            result_img.append(images[filenames.index(result)])
        index_img = 0
        for result in result_img:
            cv.imwrite(path_imgOutputsT + str(index_img) + '.jpg', result)
            index_img += 1

        # Save the image
        print('[4] Tile Images...')
        image_tile_Dir = tile()
        tile_img = cv.imread(image_tile_Dir)
        cv.namedWindow('Resultant Image', cv.WND_PROP_FULLSCREEN)
        cv.setWindowProperty(
            'Resultant Image', cv.WND_PROP_FULLSCREEN, cv.WINDOW_FULLSCREEN)
        cv.imshow('Resultant Image', tile_img)
        cv.waitKey(0)
        cv.destroyAllWindows()
        print('Image Recognition Program Terminated')

    except Exception as e:
        print('Error Tiling')
        print(e)

if __name__ == "__main__":
    main()
