###########################################################################
# Subject: CZ3004 MDP Image Recognition 20/21
# Team: 22
# Contributor: Sam Jian Shen, Lin Yue
# Version: 1.0
###########################################################################
###########################################################################
# Capture camera while camera function is executed 
# Goal:
# Minimize Execution Time during capture.
# Note: This file is without communciation modules such that IR can run 
# independently to test on runtime detection
###########################################################################
print('Initialize Capture Operation')
import time
import os
start = time.time()
from picamera import PiCamera
from picamera.array import PiRGBArray
pathDir = '/home/pi/shared'

# Clear Shared File
#for file in os.listdir(pathDir):
#	os.remove(pathDir + '/' + file)
#	print('Removing: ' + file)

# Set Camera Properties and Parameter
res_horizontal = 640
res_vertical = 480
limit = 20
i = 0
#channel = 3
exposure_mode = 'auto' # 'auto'(default) , 'off' , read Picamera to check other properties
iso = 100 # 100 - 200 day light 400-800 night time
# pathDir = "//Z"
# filename = ""
# Invoke Function
camera = PiCamera()
output = PiRGBArray(camera)
#output = np.empty((res_vertical,res_horizontal,channel), dtype=np.uint8)
camera.resolution = (res_horizontal,res_vertical)
# PiCamera Settings
camera.shutter_speed = camera.exposure_speed
camera.exposure_mode = exposure_mode 
camera.iso = iso 
end = time.time()
print('Initialize Time Taken : ' + str(round(end-start,2)) + 's')
print('Capture Operation Ready')
try:
	index = 10
	while True:
		# Listening for Incoming Signal 'A'
		#!! if signal 'A' == true
		start = time.time()
		#camera.capture(output,'rgb') 
		camera.capture('/home/pi/shared/' + str(index) + '.jpg') #debug purpose
		index  = index + 1
		if(limit + 10  < i):
			print('Capture Operation Stopped')
			camera.close()
			exit(0)
		i = i + 1
		end = time.time()
		print('Image Capture Successfully, Time Taken: ' + str(round(end-start,2)) + 's')
	
except KeyboardInterrupt: # Press Control + C to terminate program	
	print('Capture Operation Stopped')
	camera.close()
	exit(0) # proper closed of program
