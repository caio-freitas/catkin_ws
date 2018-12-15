#!/usr/bin/env python

import rospy
import mavros_msgs
from mavros_msgs import srv
from geometry_msgs.msg import PoseStamped, TwistStamped
from mavros_msgs.msg import State
import time

################# Objetos ############
goal_pose = PoseStamped()
current_state = State()
Glocal = PoseStamped()
local = PoseStamped()

def chegou(goal, actual):
    if (abs(goal.pose.position.x - actual.pose.position.x) < 0.05) and (abs(goal.pose.position.y - actual.pose.position.y) < 0.05) and (abs(goal.pose.position.z - actual.pose.position.z) < 0.05):
        return True
    else:
        return False

def drone_takeoff(height, duration):
    rate = rospy.Rate(20) # 10hz
    ############## Funcoes de Callback ########
    def state_callback(state_data):
        global current_state
        current_state = state_data


    def local_callback(local):
        global Glocal

        Glocal.pose.position.x = local.pose.position.x
        Glocal.pose.position.y = local.pose.position.y
        Glocal.pose.position.z = local.pose.position.z


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



    rospy.loginfo("[ROS] SETUP CONCLUIDO")

    init_time = time.time()
    while not rospy.is_shutdown() and time.time() - init_time < duration:
        #print(Glocal)
        if current_state != "OFFBOARD" or not current_state.armed:
            arm(True)
            set_mode(custom_mode = "OFFBOARD")

        if current_state.armed == True:
            rospy.loginfo("DRONE ARMED")

        if current_state.mode == "OFFBOARD":
            rospy.loginfo('OFFBOARD mode setted')
        print(abs(Glocal.pose.position.z - goal_pose.pose.position.z))
        if not chegou(Glocal, goal_pose):
            set_position(0, 0, height)
            print("DECOLANDO")

        rate.sleep()

    print("\nROS FOI DESATIVADO\n")
    return "succeeded"

if __name__ == "__main__":
    drone_takeoff()
