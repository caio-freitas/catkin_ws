#!/usr/bin/env python

import rospy
import mavros_msgs
from geometry_msgs.msg import PoseStamped, TwistStamped
import time

################# Objetos ############
drone_pose = PoseStamped()
goal_pose = PoseStamped()
init_pose = PoseStamped()

def drone_stay(duration):
    #rospy.init_node("Stay")
    rate = rospy.Rate(20) # 10hz

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

    rate.sleep()
    init_time = time.time()

    init_pose.pose.position.x = drone_pose.pose.position.x
    init_pose.pose.position.y = drone_pose.pose.position.y
    init_pose.pose.position.z = drone_pose.pose.position.z
    while not rospy.is_shutdown() and time.time() - init_time < duration:
        local_position_pub.publish(init_pose)
        info = 'Position: (' + str(drone_pose.pose.position.x) + ', ' + str(drone_pose.pose.position.y) + ', ' + str(drone_pose.pose.position.z) +   ')'
        rospy.loginfo(info)
        rospy.loginfo('STAYING IN POSITION')
        rate.sleep()

    return "done"

if __name__ == "__main__":
    drone_stay(10)
