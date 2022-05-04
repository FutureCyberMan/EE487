#!/usr/bin/python3
#
# Copyright (c) 2019, NVIDIA CORPORATION. All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
#

import jetson.inference
import jetson.utils
from Quanser.product_QCar import QCar
from Quanser.q_control import *
from Quanser.q_dp import *
from Quanser.q_interpretation import *
from Quanser.q_misc import *
from Quanser.q_ui import *
from Quanser.q_essential import *
from sensor_msgs.msg import Image
from geometry_msgs.msg import Vector3Stamped
import rospy

class Follower:
	def __init__(self):
		self.cmd_vel_pub = rospy.Publisher('/qcar/user_command', Vector3dStamped, queue_size=10)
		self.Vector3dStamped = Vector3dStamped()
	def callBack(self, error):
		self.Vector3dStamped.vector.x = .15
		self.Veector3dStamped.vector.y = error/300
		self.cmd_vel_pub.publish(self.Vector3dStamped)
		

#Setting Filter
steering_filter = Filter().low_pass_first_order_variable(25, 0.033)
next(steering_filter)
dt = 0.033

myCar = QCar()
gpad = gamepadViaTarget(1)


net = jetson.inference.detectNet("ped-100", threshold=0.5)
camera = jetson.utils.videoSource("csi://1", argv=['--input-flip=rotate-180'])      # '/dev/video0' for V4L2

display = jetson.utils.videoOutput("display://0") # 'my_video.mp4' for file
x = Follower()

while display.IsStreaming():
	img = camera.Capture()
	detections = net.Detect(img)
	if len(detections) == 1 and detections[0].Confidence > .5:
		location = detections[0].Center[1]
	error = 1280/2 - location
	x.callBack(error)
	display.Render(img)
	display.SetStatus("Object Detection | Network {:.0f} FPS".format(net.GetNetworkFPS()))
