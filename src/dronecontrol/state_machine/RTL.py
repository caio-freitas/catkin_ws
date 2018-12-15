#!/usr/bin/env python

import rospy
import mavros_msgs
from mavros_msgs import srv
from geometry_msgs.msg import PoseStamped, TwistStamped
from mavros_msgs.msg import State
from sensor_msgs.msg import BatteryState
import time

################# Objetos ############
goal_pose = PoseStamped()
Glocal = PoseStamped()

def chegou(goal, actual):
    if (abs(goal.pose.position.x - actual.pose.position.x) < 0.05) and (abs(goal.pose.position.y - actual.pose.position.y) < 0.05) and (abs(goal.pose.position.z - actual.pose.position.z) < 0.05):
        return True
    else:
        return False

def drone_RTL():
    rate = rospy.Rate(20)

    ############## Funcoes de Callback ########
    def local_callback(local):
        global Glocal

        Glocal.pose.position.x = local.pose.position.x
        Glocal.pose.position.y = local.pose.position.y
        Glocal.pose.position.z = local.pose.position.z

    ############### Publishers ###############
    local_position_pub = rospy.Publisher('/mavros/setpoint_position/local', PoseStamped, queue_size = 100)

    ########### Subscribers ##################
    local_atual = rospy.Subscriber('/mavros/local_position/pose', PoseStamped, local_callback)

    ############## Services ##################

    arm = rospy.ServiceProxy('/mavros/cmd/arming', mavros_msgs.srv.CommandBool)

    def set_position(x, y, z):
        global goal_pose
        goal_pose.pose.position.x = x
        goal_pose.pose.position.y = y
        goal_pose.pose.position.z = z
        local_position_pub.publish(goal_pose)


    rospy.loginfo("[ROS] SETUP CONCLUIDO")
    rate.sleep()
    height = Glocal.pose.position.z
    print("Position: ", Glocal.pose.position.x, Glocal.pose.position.y, Glocal.pose.position.z)
    rate.sleep()
    set_position(0,0,height)
    while not chegou(Glocal, goal_pose):
        set_position(0,0,height)
        print ("[ INFO ] STARING HOME")
        rate.sleep()
    set_position(0,0,0)
    while not chegou(Glocal, goal_pose):
        print(abs(Glocal.pose.position.z - goal_pose.pose.position.z))
        if not chegou(Glocal, goal_pose):
            set_position(0,0,0)
            print ("[ INFO ] LANDING")
            rate.sleep()
        if chegou(Glocal, goal_pose):
            arm(False)
            break

    print("\nCHEGUEEEI\n")
    arm(False)
    print("DESARMANDO DRONE")
    return "succeeded"

if __name__ == "__main__":
    drone_RTL()
