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
current_state = State()
Glocal = PoseStamped()
local = PoseStamped()
battery = BatteryState()

def drone_RTL():
    rospy.init_node('ReturnToLand', anonymous = True)
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

    def battery_callback(bat_dat):
        global battery

        battery.voltage = bat_dat.voltage
        battery.percentage = bat_dat.percentage
        battery.current = bat_dat.current


    ############### Publishers ###############
    local_position_pub = rospy.Publisher('/mavros/setpoint_position/local', PoseStamped, queue_size = 100)


    ########### Subscribers ##################
    local_atual = rospy.Subscriber('/mavros/local_position/pose', PoseStamped, local_callback)

    state_status_subscribe = rospy.Subscriber('/mavros/state', State, state_callback)

    battery_subscriber = rospy.Subscriber('/mavros/battery', BatteryState, battery_callback)

    ############## Services ##################

    arm = rospy.ServiceProxy('/mavros/cmd/arming', mavros_msgs.srv.CommandBool)

    set_mode = rospy.ServiceProxy('/mavros/set_mode', mavros_msgs.srv.SetMode)

    h=2

    def chegou (goal, actual):
        if (abs(actual.pose.position.z - goal.pose.position.z) < 0.05) and (abs(actual.pose.position.y - goal.pose.position.y) < 0.05) and (abs(actual.pose.position.x - goal.pose.position.x) < 0.05):
            return True
        return False


    def set_position(x, y, z):
        global goal_pose
        goal_pose.pose.position.x = x
        goal_pose.pose.position.y = y
        goal_pose.pose.position.z = z
        local_position_pub.publish(goal_pose)



    goal_pose = Glocal

    for i in range(300):
        local_position_pub.publish(goal_pose)
        rate.sleep()

    rospy.loginfo("[ROS] SETUP CONCLUIDO")
    set_position(0,0,0)
    print("Position: ", Glocal.pose.position.x, Glocal.pose.position.y, Glocal.pose.position.z)
    while not rospy.is_shutdown() and not chegou(goal_pose, Glocal):
        if current_state != "OFFBOARD" or not current_state.armed:
            arm(True)
            set_mode(custom_mode = "OFFBOARD")

        print(str(current_state.mode))

        if current_state.armed == True:
            rospy.loginfo("DRONE ARMED")

        if current_state.mode == "OFFBOARD":
            rospy.loginfo('OFFBOARD mode setted')

        rate.sleep()
        #if not compara(Glocal, goal_pose):
        print("Position: ", Glocal.pose.position.x, Glocal.pose.position.y, Glocal.pose.position.z)
        set_position(0,0,0)
        print ("COMING HOME")
        rate.sleep()
    print("\nCHEGUEEEI\n")
    arm(False)
    print("DESARMANDO DRONE")
    return "succeeded"

if __name__ == "__main__":
    drone_RTL()
