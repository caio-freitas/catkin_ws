#!/usr/bin/env python

import rospy
import mavros_msgs
from mavros_msgs import srv
from geometry_msgs.msg import PoseStamped
from mavros_msgs.msg import State
import time


goal_pose = PoseStamped()
drone_pose = PoseStamped()
final_pose = PoseStamped()

def chegou(goal, actual):
    if (abs(goal.pose.position.x - actual.pose.position.x) < 0.1) and (abs(goal.pose.position.y - actual.pose.position.y) < 0.1) and (abs(goal.pose.position.z - actual.pose.position.z) < 0.10):
        return True
    else:
        return False

def local_callback(local):
    global drone_pose

    drone_pose.pose.position.x = local.pose.position.x
    drone_pose.pose.position.y = local.pose.position.y
    drone_pose.pose.position.z = local.pose.position.z

def set_position(x, y, z):
    global goal_pose
    goal_pose.pose.position.x = x
    goal_pose.pose.position.y = y
    goal_pose.pose.position.z = z
    local_position_pub.publish(goal_pose)


def drone_land():
    rate = rospy.Rate(20)
    velocity = 0.3
    part = velocity/20.0

    ############### Publisher ###############
    local_position_pub = rospy.Publisher('/mavros/setpoint_position/local', PoseStamped, queue_size = 100)

    ########### Subscriber ##################
    local_atual = rospy.Subscriber('/mavros/local_position/pose', PoseStamped, local_callback)

    ############## Service ##################
    arm = rospy.ServiceProxy('/mavros/cmd/arming', mavros_msgs.srv.CommandBool)

    final_pose.pose.position.x = drone_pose.pose.position.x
    final_pose.pose.position.y = drone_pose.pose.position.y
    final_pose.pose.position.z = 0

    height = drone_pose.pose.position.z

    while not rospy.is_shutdown() or not chegou(drone_pose, final_pose):
        rospy.loginfo('Executing State LAND')

        rospy.loginfo('Height: ' + str(abs(drone_pose.pose.position.z)))

        if not chegou(drone_pose, goal_pose):
            rospy.logwarn ('LANDING AT ' + str(velocity) + 'm/s')
            if t < height:
                t += part
            set_position(0,0,height - t)
            rate.sleep()

    print("\nCHEGUEEEI\n")
    rospy.logwarn("DESARMANDO DRONE")
    arm(False)
    return "succeeded"

if __name__ == "__main__":
    drone_land()
