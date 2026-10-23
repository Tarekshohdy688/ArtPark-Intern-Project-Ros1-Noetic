#!/usr/bin/env python3

import rospy
from std_msgs.msg import String

def publishing():
    rospy.init_node('talker', anonymous=True)
    pub = rospy.Publisher('/robot_status', String, queue_size=10)
    rate = rospy.Rate(10)

    while not rospy.is_shutdown():
        message = "Robot is running. %s" % rospy.get_time()
        rospy.loginfo(message)
        pub.publish(message)
        rate.sleep()

if __name__ == '__main__':
    try:
        publishing()
    except rospy.ROSInterruptException:
        pass
