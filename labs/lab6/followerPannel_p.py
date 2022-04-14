#!/usr/bin/env python
import rospy, cv2, cv_bridge, numpy
from sensor_msgs.msg import CompressedImage
from geometry_msgs.msg import Twist
import numpy as np

class Follower:
  def __init__(self):
    self.bridge = cv_bridge.CvBridge()
    cv2.namedWindow("window", 1)
    self.image_sub = rospy.Subscriber('/raspicam_node/image/compressed', CompressedImage, self.image_callback)
    self.cmd_vel_pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
    self.maskPub = rospy.Publisher('/mask', CompressedImage, queue_size=1)
    self.twist = Twist()

  def image_callback(self, msg):
    # image = self.bridge.imgmsg_to_cv2(msg,desired_encoding='bgr8')
    np_arr = np.fromstring(msg.data, np.uint8)
    image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV) # defines color
    lower_yellow = numpy.array([170, 50, 50]) # defines yellowness that we want to follow
    upper_yellow = numpy.array([175, 255, 255]) # defines upper bound for yellowness
    mask = cv2.inRange(hsv, lower_yellow, upper_yellow) # if not yellow, mask it
    h, w, d = image.shape
    search_top = 0# 3*h//4
    search_bot = 0# 3*h//4 + 20
    # mask[0:search_top, 0:w] = 0
    # mask[search_bot:h, 0:w] = 0
    M = cv2.moments(mask)
    if M['m00'] > 0:
      cx = int(M['m10']/M['m00'])
      cy = int(M['m01']/M['m00'])
      cv2.circle(image, (cx, cy), 20, (0,0,255), -1)
      # err = cx - w/2 # error of where the dot is vs where it should be. We want the dot to be at the center of the window
      err = w/2 - cx
      print(err)
      self.twist.linear.x = .8
      self.twist.angular.z = float(err) / 300
      self.cmd_vel_pub.publish(self.twist)
    #cv2.imshow('mask', mask)
    #cv2.waitKey(3)
    cv2.imshow("window", image)
    cv2.waitKey(3)

rospy.init_node('follower')
follower = Follower()
rospy.spin()
