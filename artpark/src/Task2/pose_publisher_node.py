#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import PoseStamped
import math

class RobotPosePublisher:
    def __init__(self):
        rospy.init_node('pose_publisher', anonymous=True)
        self.pose_pub = rospy.Publisher('/robot_pose', PoseStamped, queue_size=10)
        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0
        self.rate = rospy.Rate(10)

    def publish_pose(self):
        while not rospy.is_shutdown():
            pose__pub_msg = PoseStamped()
            pose__pub_msg.header.stamp = rospy.Time.now()
            pose__pub_msg.header.frame_id = "map"

            pose__pub_msg.pose.position.x = self.x
            pose__pub_msg.pose.position.y = self.y
            pose__pub_msg.pose.position.z = 0.0

            qx, qy, qz, qw = self.euler_to_quaternion(0, 0, self.theta)
            pose__pub_msg.pose.orientation.x = qx
            pose__pub_msg.pose.orientation.y = qy
            pose__pub_msg.pose.orientation.z = qz
            pose__pub_msg.pose.orientation.w = qw

            self.pose_pub.publish(pose__pub_msg)
            self.simulate_movement()
            self.rate.sleep()

    def simulate_movement(self):
        self.x += 0.1 * math.cos(self.theta)
        self.y += 0.1 * math.sin(self.theta)
        self.theta += 0.1

    def euler_to_quaternion(self,roll, pitch, yaw):
        qx = math.sin(roll / 2) * math.cos(pitch / 2) * math.cos(yaw / 2) - math.cos(roll / 2) * math.sin(pitch / 2) * math.sin(yaw / 2)
        qy = math.cos(roll / 2) * math.sin(pitch / 2) * math.cos(yaw / 2) + math.sin(roll / 2) * math.cos(pitch / 2) * math.sin(yaw / 2)
        qz = math.cos(roll / 2) * math.cos(pitch / 2) * math.sin(yaw / 2) - math.sin(roll / 2) * math.sin(pitch / 2) * math.cos(yaw / 2)
        qw = math.cos(roll / 2) * math.cos(pitch / 2) * math.cos(yaw / 2) + math.sin(roll / 2) * math.sin(pitch / 2) * math.sin(yaw / 2)
        return qx, qy, qz, qw

if __name__ == '__main__':
    try:
        robot_pose_publisher = RobotPosePublisher()
        robot_pose_publisher.publish_pose()
    except rospy.ROSInterruptException:
        pass
