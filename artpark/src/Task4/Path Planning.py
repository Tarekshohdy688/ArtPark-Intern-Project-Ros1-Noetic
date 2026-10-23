import rospy
from gazebo_msgs.msg import ModelStates
from geometry_msgs.msg import Twist
import math

SAFE_DISTANCE = 2.0
TARGET_X, TARGET_Y = 10.0, 10.0
def distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

def calculate_velocity(current_x, current_y, target_x, target_y, other_robot_x, other_robot_y):
    cmd = Twist()
    dx = target_x - current_x
    dy = target_y - current_y
    angle_to_target = math.atan2(dy, dx)
    
    dist_to_robot = distance(current_x, current_y, other_robot_x, other_robot_y)
    
    if dist_to_robot < SAFE_DISTANCE:
        cmd.angular.z = 0.2
    else:
        cmd.linear.x = 0.1
        cmd.angular.z = angle_to_target

    return cmd

def model_states_callback(msg):
    try:
        idx_robot1 = msg.name.index("robot1")
        idx_robot2 = msg.name.index("robot2")
        
        pos_robot1 = msg.pose[idx_robot1].position
        pos_robot2 = msg.pose[idx_robot2].position
        
        cmd_robot1 = calculate_velocity(pos_robot1.x, pos_robot1.y, TARGET_X, TARGET_Y, pos_robot2.x, pos_robot2.y)
        cmd_robot2 = calculate_velocity(pos_robot2.x, pos_robot2.y, TARGET_X, TARGET_Y, pos_robot1.x, pos_robot1.y)
        
        pub_robot1.publish(cmd_robot1)
        pub_robot2.publish(cmd_robot2)

    except ValueError:
        rospy.logwarn("Not Found")

def dynamic_path_planning():
    global pub_robot1, pub_robot2

    rospy.init_node("Path Planning")

    pub_robot1 = rospy.Publisher("/robot1/cmd_vel", Twist, queue_size=10)
    pub_robot2 = rospy.Publisher("/robot2/cmd_vel", Twist, queue_size=10)

    rospy.Subscriber("/gazebo/model_states", ModelStates, model_states_callback)

    rospy.spin()

if __name__ == "__main__":
    dynamic_path_planning()
