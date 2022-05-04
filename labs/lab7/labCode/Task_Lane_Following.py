from Quanser.product_QCar import QCar
from Quanser.q_control import *
from Quanser.q_dp import *
from Quanser.q_interpretation import *
from Quanser.q_misc import *
from Quanser.q_ui import *
from Quanser.q_essential import *
import jetson.inference
import jetson.utils
import time
import struct
import numpy as np 
import cv2
import math

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
## Timing Parameters and methods 
sampleRate = 60
sampleTime = 1/sampleRate
print('Sample Time: ', sampleTime)

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
# Additional parameters
counter = 0
imageWidth = 1640
imageHeight = 820
cameraID = '3'

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
#Setting Filter
steering_filter = Filter().low_pass_first_order_variable(25, 0.033)
next(steering_filter)
dt = 0.033

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
## Initialize the CSI cameras
myCam = Camera2D(camera_id=cameraID, frame_width=imageWidth, frame_height=imageHeight, frame_rate=sampleRate)

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
## QCar and Gamepad Initialization
myCar = QCar()
gpad = gamepadViaTarget(1)

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 

net = jetson.inference.detectNet("multiped-500", threshold=0.8)
#camera = jetson.utils.videoSource("csi://0", argv=['--input-flip=rotate-180'])
# display = jetson.utils.videoOutput("display://0") # 'my_video.mp4' for file

## Main Loop
go = True
try:
	while True:
		start = time.time()
		# Capture RGB Image from CSI
		myCam.read()

		# Crop out a piece of the RGB to improve performance
		cropped_rgb = myCam.image_data[524:674, 0:820]

		# Convert to HSV and then threshold it for yellow
		hsv_buf = cv2.cvtColor(cropped_rgb, cv2.COLOR_BGR2HSV)
		binary = binary_thresholding(hsv_buf, lower_bounds=np.array([10, 50, 100]), upper_bounds=np.array([45, 255, 255]))

		# Display the RGB (Original) as well as the Binary in 1/4th resolution for speed
		# cv2.imshow('My RGB image', cv2.resize(myCam.image_data, (410, 205) ) )
		cv2.imshow('My RGB image', myCam.image_data )
		# cv2.imshow('My Binary image', cv2.resize(binary, (410, 75) ))

		# Find slope and intercept of linear fit from the binary image
		slope, intercept = find_slope_intercept_from_binary(binary)

		# steering from slope and intercept
		raw_steering = 1.5*(slope - 0.3419) + (1/150)*(intercept+5)
		steering = steering_filter.send((saturate(raw_steering, 0.5, -0.5), dt))

		# Write steering to qcar
		new = gpad.read()

		mtr_cmd = control_from_gamepad(gpad.LB, gpad.RT, gpad.LLA, gpad.A)
		# mtr_cmd = [0, 0] where 0 == velocity and 1 is equal to y.

		detections = net.Detect(jetson.utils.cudaFromNumpy(myCam.image_data))
		if len(detections) == 0:
			go = True
		for detection in detections:
			print(net.GetClassDesc(detection.ClassID))
			if (net.GetClassDesc(detection.ClassID)) == "person" and detection.Area > 65000 and detection.Area < 90000:
				go = False
				mtr_cmd[0] = 0
		# display.Render(jetson.utils.cudaFromNumpy(myCam.image_data))
		# display.SetStatus("Object Detection | Network {:.0f} FPS".format(net.GetNetworkFPS()))
		if gpad.X == 1:
			if math.isnan(steering):
				mtr_cmd[1] = 0
			else:
				mtr_cmd[1] = steering
			if go:
				mtr_cmd[0] = .075	
				# mtr_cmd[0] = mtr_cmd[0]*np.cos(steering)
		# mtr_cmd[1] = steering
		myCar.write_mtrs(mtr_cmd)
		cv2.waitKey(1)
		end = time.time()
		dt = end - start

except KeyboardInterrupt:
	print("User interrupted!")

finally:
	# Terminate camera and QCar
	myCam.terminate()
	myCar.terminate()
# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
