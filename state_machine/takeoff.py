#!/usr/bin/env python

import rospy
import mavros_msgs
from mavros_msgs import srv
from geometry_msgs.msg import PoseStamped, TwistStamped
from mavros_msgs.msg import State
import time

################# Objetos ############
goal_pose = PoseStamped()
drone_state = State()
drone_pose = PoseStamped()


def drone_takeoff(height, duration):
    rate = rospy.Rate(100) # 10hz
    velocity = 0.3
    part = velocity/100.0

    ############## Funcoes de Callback ########
    def state_callback(state_data):
        global drone_state
        drone_state = state_data


    def local_callback(local):
        global drone_pose

        drone_pose.pose.position.x = local.pose.position.x
        drone_pose.pose.position.y = local.pose.position.y
        drone_pose.pose.position.z = local.pose.position.z

    ############### Publishers ###############
    local_position_pub = rospy.Publisher('/mavros/setpoint_position/local', PoseStamped, queue_size = 100)

    ########### Subscribers ##################
    local_atual = rospy.Subscriber('/mavros/local_position/pose', PoseStamped, local_callback)

    state_status_subscribe = rospy.Subscriber('/mavros/state', State, state_callback)

    ############## Services ##################

    arm = rospy.ServiceProxy('/mavros/cmd/arming', mavros_msgs.srv.CommandBool)

    set_mode = rospy.ServiceProxy('/mavros/set_mode', mavros_msgs.srv.SetMode)


    def set_position(x, y, z):
        global goal_pose
        goal_pose.pose.position.x = x
        goal_pose.pose.position.y = y
        goal_pose.pose.position.z = z
        local_position_pub.publish(goal_pose)

    set_position(0,0,0)
    for i in range(300):
        local_position_pub.publish(goal_pose)
        rate.sleep()

    while not drone_state.armed:
        rospy.logwarn("ARMING DRONE")
        arm(True)
        rate.sleep()


    init_time = time.time()

    t=0
    while not rospy.is_shutdown() and drone_pose.pose.position.z <= height:
        rospy.loginfo('Executing State TAKEOFF')

        if drone_state != "OFFBOARD":
            rospy.loginfo("SETTING OFFBOARD FLIGHT MODE")
            set_mode(custom_mode = "OFFBOARD")

        if not drone_state.armed:
            rospy.logwarn("ARMING DRONE")
            arm(True)

        if drone_state.armed == True:
            rospy.loginfo("DRONE ARMED")

        if t < height:
            rospy.logwarn('TAKING OFF AT ' + str(velocity) + ' m/s')
            set_position(0, 0, t)
            t += part
        else:
            set_position(0, 0, height)

        rospy.loginfo('Position: (' + str(drone_pose.pose.position.x) + ', ' + str(drone_pose.pose.position.y) + ', '+ str(drone_pose.pose.position.z) + ')')

        rate.sleep()

    set_position(0, 0, height)

    return "done"

if __name__ == "__main__":
    drone_takeoff()
