#!/usr/bin/env python
#!/usr/bin/env python
import rospy
from std_msgs.msg import String

def talker():
    pub = rospy.Publisher('chatter', String, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    # while not rospy.is_shutdown():
    while True:
        string = raw_input("\n")
	if string == "P":
        	rospy.loginfo(string)
        	pub.publish(string)
        	# rate.sleep()
		break

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
