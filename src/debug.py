###########################################################################
# Subject: CZ3004 MDP Image Recognition 20/21
# Team: 22
# Contributor: Sam Jian Shen, Lin Yue
# Version: 1.0
###########################################################################
###########################################################################
# Various isolate functions debug
###########################################################################
from preprocess import *
from model import *
from postprocess import *
from debug import *
import pickle

def load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        
        img = cv.imread(os.path.join(folder,filename))
        if img is not None:
            images.append(img)
            print('Added: ', filename)
    return images

def test_contour():
    images = []
    images.append(cv.imread('CZ3004_MDP_RPI_ImageRecognition/images/test/1_(1).jpg'))
    images.append(cv.imread('CZ3004_MDP_RPI_ImageRecognition/images/test/2_(50).jpg'))
    images.append(cv.imread('CZ3004_MDP_RPI_ImageRecognition/images/test/3_(75).jpg'))
    for image in images:
        contour(image)

def test_plot():
    list_result  = []
    coordinates = []
    image_raw = cv.imread('CZ3004_MDP_RPI_ImageRecognition/images/output/1(2).jpg')
    list_result.append([5,5,50,50,'hello','Go',0])
    list_result.append([50,50,50,50,'hello1','seven',1])
    list_result.append([200,200,50,50,'hello2','none',2])
    coordinates.append([5,5])
    coordinates.append([5,5])
    coordinates.append([100,100])
    image_output = plot(list_result, image_raw, coordinates)

def test_detection():
    
    images = []
    path = 'CZ3004_MDP_RPI_ImageRecognition/images/test/'
    '''
    images.append(cv.imread('CZ3004_MDP_RPI_ImageRecognition/images/test/1_(1).jpg'))
    images.append(cv.imread('CZ3004_MDP_RPI_ImageRecognition/images/test/2_(50).jpg'))
    images.append(cv.imread('CZ3004_MDP_RPI_ImageRecognition/images/test/3_(75).jpg'))
    '''
    images = load_images_from_folder(path)

    #print(images[0])
    #exit(0)
    detect_fn = load_model()
    list_result = detection(detect_fn, images) 
    for result in list_result:
        print(result)
    

def test_loadall_imgdata(path):
    with open(path, "rb") as f:
        while True:
            try:
                yield pickle.load(f)
            except EOFError:
                break