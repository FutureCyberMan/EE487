#!/usr/bin/env python
#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from math import pow, atan2, sqrt
import math

class KeyBoardSubscriber:
    def __init__(self):
	self.start = False
	# rospy.init_node('listener', anonymous=True)
	self.listenKey = rospy.Subscriber("chatter", String, self.callback)

    def callback(self, data):
	data = str(data)
	print(data)
	if data == "data: \"P\"":
		print(str(self.start))
		self.start = True
class TurtleBot:
    def __init__(self):
        rospy.init_node('turtlebot_controller', anonymous=True)

        self.pose_subscriber = rospy.Subscriber('/turtle1/pose',
                                                Pose, self.update_pose)

        self.pose = Pose()
        self.rate = rospy.Rate(10)

	self.vel_msg = Twist()

    def update_pose(self, data):
        """Callback function which is called when a new message of type Pose is
        received by the subscriber."""
        self.pose = data
        self.pose.x = round(self.pose.x, 4)
        self.pose.y = round(self.pose.y, 4)


    def rotate(self, angle):
    	# Setting the current time for distance calculus
	print("X location: {}, Y location: {}".format(self.pose.x, self.pose.y))
	self.vel_msg.angular.z = .25
    	t0 = rospy.Time.now().to_sec()
    	current_angle = 0
	relative_angle = angle*2*math.pi/360

    	while(current_angle < relative_angle):
        	self.velocity_publisher.publish(self.vel_msg)
        	t1 = rospy.Time.now().to_sec()
        	current_angle = self.vel_msg.angular.z*(t1-t0)

	self.vel_msg.angular.z = 0
    	self.velocity_publisher.publish(self.vel_msg)
    def move(self, distance):
	print("X location: {}, Y location: {}".format(self.pose.x, self.pose.y))
	self.vel_msg.linear.x = 1.0
	t0 = rospy.Time.now().to_sec()
	current_location = 0
	while current_location < distance:
		self.velocity_publisher.publish(self.vel_msg)
		t1 = rospy.Time.now().to_sec()
		current_location = self.vel_msg.linear.x*(t1-t0)
	self.vel_msg.linear.x = 0
	self.velocity_publisher.publish(self.vel_msg)


if __name__ == '__main__':
	try:
		x = TurtleBot()
		key = KeyBoardSubscriber()
		while not key.start:
			pass
		x.rotate(90)
		x.move(3.0)
		x.rotate(225)
		x.move(3.5)
		x.rotate(135)
		x.move(3.0)
	except rospy.ROSInterruptException:
		pass
