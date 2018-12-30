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
drone_pose = PoseStamped()
final_position = PoseStamped()

final_position.pose.position.x = 0
final_position.pose.position.y = 0
final_position.pose.position.y = 0

def chegou(goal, actual):
    if (abs(goal.pose.position.x - actual.pose.position.x) < 0.1) and (abs(goal.pose.position.y - actual.pose.position.y) < 0.1) and (abs(goal.pose.position.z - actual.pose.position.z) < 0.10):
        return True
    else:
        return False

def drone_RTL():
    rate = rospy.Rate(20)
    velocity = 0.3
    part = velocity/20.0
    ############## Funcoes de Callback ########
    def local_callback(local):
        global drone_pose

        drone_pose.pose.position.x = local.pose.position.x
        drone_pose.pose.position.y = local.pose.position.y
        drone_pose.pose.position.z = local.pose.position.z

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
    height = drone_pose.pose.position.z
    rospy.loginfo('Position: (' + str(drone_pose.pose.position.x) + ', ' + str(drone_pose.pose.position.y) + ', ' + str(drone_pose.pose.position.z) + ')')

    while not chegou(drone_pose, goal_pose):
        rospy.loginfo('Executing State RTL')

        rospy.loginfo ("[ INFO ] STARING HOME")
        set_position(0,0,height)
        rate.sleep()

    t=0
    set_position(0,0,0)
    rate.sleep()
    while not chegou(drone_pose, final_position):
        rospy.loginfo('Executing State RTL')

        rospy.loginfo('Height: ' + str(abs(drone_pose.pose.position.z)))
        #print drone_pose
        if not chegou(drone_pose, goal_pose):
            rospy.logwarn ('LANDING AT ' + str(velocity) + 'm/s')
            if t < height:
                t += part
            set_position(0,0,height - t)
            rate.sleep()

        else:
            if t <= height:
                t += part
                set_position(0,0,height - t)
            else:
                set_position(0,0,0)
            rate.sleep()

    print("\nCHEGUEEEI\n")
    rospy.logwarn("DESARMANDO DRONE")
    arm(False)
    return "succeeded"

if __name__ == "__main__":
    drone_RTL()
