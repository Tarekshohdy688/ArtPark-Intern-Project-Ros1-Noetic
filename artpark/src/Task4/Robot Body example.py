#!/usr/bin/env python3

import rospy
from gazebo_msgs.msg import ModelStates
from geometry_msgs.msg import Twist
import math

SAFE_DISTANCE = 2.0

pub_robot1 = None
pub_robot2 = None

def distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

def model_states_callback(msg):
    global pub_robot1, pub_robot2

    try:
        idx_robot1 = msg.name.index("robot1")
        idx_robot2 = msg.name.index("robot2")
        
        pos_robot1 = msg.pose[idx_robot1].position
        pos_robot2 = msg.pose[idx_robot2].position
        
        dist = distance(pos_robot1.x, pos_robot1.y, pos_robot2.x, pos_robot2.y)
        
        cmd_robot1 = Twist()
        cmd_robot2 = Twist()

        if dist < SAFE_DISTANCE:
            cmd_robot1.linear.x = 0.0
            cmd_robot2.linear.x = 0.0
        else:
            cmd_robot1.linear.x = 0.1
            cmd_robot2.linear.x = 0.1

        pub_robot1.publish(cmd_robot1)
        pub_robot2.publish(cmd_robot2)

    except ValueError:
        rospy.logwarn("Not Found")

def centralized_controller():
    global pub_robot1, pub_robot2

    rospy.init_node("Robot Body example")

    pub_robot1 = rospy.Publisher("/robot1/cmd_vel", Twist, queue_size=10)
    pub_robot2 = rospy.Publisher("/robot2/cmd_vel", Twist, queue_size=10)

    rospy.Subscriber("/gazebo/model_states", ModelStates, model_states_callback)

    rospy.spin()

if __name__ == "__main__":
    centralized_controller()
