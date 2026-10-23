#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

def scan_callback(msg):
    min_distance = min(msg.ranges)
    threshold = 2.0

    cmd = Twist()
    if min_distance < threshold:
        cmd.linear.x = 0.0
        cmd.angular.z = 0.2
    else:
        cmd.linear.x = 0.1
        cmd.angular.z = 0.0

    pub.publish(cmd)

rospy.init_node('LiDAR example')
sub = rospy.Subscriber('/scan', LaserScan, scan_callback)
pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

rospy.spin()
