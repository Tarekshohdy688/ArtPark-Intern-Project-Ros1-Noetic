#!/usr/bin/env python3

import rospy
from std_msgs.msg import String

def callback(data):
    rospy.loginfo("I heard %s",data.data)

def subscribing():
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber('/robot_status', String, callback)

    rospy.spin()

if __name__ == '__main__':
    try:
        subscribing()
    except rospy.ROSInterruptException:
        pass