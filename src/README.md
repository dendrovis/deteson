# CZ3004 MDP IR Team
A object detection algorithm using 15 classify target signs, image(s) was captured with PI-Camera attached to RasberryPI 3 B+

## Our objectives
1.	Ability to detect 15 classify object from images taken from the arena with camera mounted on the robot.
2.	The object detected must be plotted and label correctly onto corresponding images.
3.	All object detect images must be tile and display at the PC/Notebook or N7(Android)
4.	Keep the solutions simple!

## Prerequisite
1. Owned at least one Raspberry Pi 3 B+ with PiCamera enabled and all its python 3 and opencv dependency. https://pimylifeup.com/raspberry-pi-opencv/, https://www.raspberrypi.org/documentation/linux/software/python.md

2. Owned at least a PC/Laptop with GPUs capability rating of 3.5 and above.

3. Tensorflow Installation :
https://tensorflow-object-detection-api-tutorial.readthedocs.io/en/latest/install.html#tensorflow-installation

4. Tensorflow Object Detection API Installation : 
https://tensorflow-object-detection-api-tutorial.readthedocs.io/en/latest/install.html#tensorflow-object-detection-api-installation

5. Update Gfile to support Tensorflow 2:
https://stackoverflow.com/questions/55591437/attributeerror-module-tensorflow-has-no-attribute-gfile

6. Setup Samba for Server and Client:
https://ubuntu.com/tutorials/install-and-configure-samba#1-overview (Shared Drive in client(s) side is Z://)

7. Putty for SSH :
https://www.putty.org/

## How to use?
1. Downloaded CZ3004_MDP_RPI_ImageRecognition.zip file from github or other available source.
2. Extract CZ3004_MDP_RPI_ImageRecognition.zip file into IDE workspace
3. SSH to RPI with the correct credentials
4. Execute Z:// Files by running python3 capture_live.py in the home directory of RPI.
3. After image(s) start appearing in Z:// directory execute main.py

## About Us
Team 22

## Contributor
1. Lin Yue 
2. Sam Jian Shen

## Version
1.0