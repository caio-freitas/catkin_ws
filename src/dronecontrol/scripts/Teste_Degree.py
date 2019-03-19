#!/usr/bin/env python

import rospy
import mavros_msgs
from mavros_msgs import srv
#from mavros_msgs import PositionTarget
from geometry_msgs.msg import PoseStamped, TwistStamped, Quaternion
from mavros_msgs.msg import State
from sensor_msgs.msg import BatteryState
from sensor_msgs.msg import Imu
import time
import math

SECURE = 0.1

print('importou')

goal_pose = PoseStamped()
current_state = State()
local = PoseStamped()
Drone_local = PoseStamped()
Yaw = Imu()
y = Imu()


print('criou variais')

#As duas funcoes podem ser resumidas em uma so??
def set_position(x, y, z):
    global goal_pose
    goal_pose.pose.position.x = x
    goal_pose.pose.position.y = y
    goal_pose.pose.position.z = z

    local_position_pub.publish(goal_pose)

def set_rotation(theta):
    goal_pose.pose.orientation.y = theta
    goal_pose.pose.orientation.w = 1

    local_orientation_pub.publish(goal_pose)

def state(state_data):
    global current_state
    current_state = state_data

def drone_position(local):
    global Drone_local

    Drone_local.pose.position.x = local.pose.position.x
    Drone_local.pose.position.y = local.pose.position.y
    Drone_local.pose.position.z = local.pose.position.z

    #Drone_local.pose.orientation.y = local.pose.orientation.y

#funcao com quater
def drone_Yaw (y):
    global Yaw

    Yaw.orientation.y = y.orientation.y


def secure_accuracy (x,y):
    if (abs(x.pose.position.z - y.pose.position.z) < SECURE) and (abs(x.pose.position.y - y.pose.position.y) < SECURE) and (abs(x.pose.position.x - y.pose.position.x) < SECURE):
        return True
    return False

def rel_Goto (x, y, z):
    x = Drone_local.pose.position.x + x
    y = Drone_local.pose.position.y + y
    z = Drone_local.pose.position.z + z
    set_position(x, y, z)

    rate.sleep()

    while not secure_accuracy(Drone_local, goal_pose):
        set_position (x, y, z)

        rate.sleep()

def abs_Goto (x, y, z):
    set_position (x, y, z)

    rate.sleep()

    while not secure_accuracy(Drone_local, goal_pose):
        set_position (x, y, z)

        rate.sleep()

def abs_rotation (theta):
    set_rotation(theta)
    rate.sleep()

    while not abs(Yaw.orientation.y - goal_pose.pose.orientation.y) < 0.1:
        print('entrou no while')
        set_rotation(theta)
        print (Yaw.orientation.y)
        #print (Drone_local.pose.orientation.y)
        print (goal_pose.pose.orientation.y)

        rate.sleep()

print('criou funcao')

rospy.init_node('Vel_Control_Node', anonymous = True)

rate = rospy.Rate(20)

local_position_pub = rospy.Publisher('/mavros/setpoint_position/local', PoseStamped, queue_size = 100)

local_orientation_pub = rospy.Publisher('/mavros/setpoint_position/local', PoseStamped, queue_size = 100)

state_status_subscribe = rospy.Subscriber('/mavros/state', State, state)

arm = rospy.ServiceProxy('/mavros/cmd/arming', mavros_msgs.srv.CommandBool)

set_mode = rospy.ServiceProxy('/mavros/set_mode', mavros_msgs.srv.SetMode)

local_atual_subscribe = rospy.Subscriber('/mavros/local_position/pose', PoseStamped, drone_position)

yaw_atual_subscribe = rospy.Subscriber('/mavros/imu/data', Imu, drone_Yaw)

print('sub e pubs')

for i in range(300):
    local_position_pub.publish(goal_pose)
    rate.sleep()

rospy.loginfo("[ROS] SETUP CONCLUIDO")

cont = 0


while not rospy.is_shutdown():
    if current_state != "OFFBOARD" or not current_state.armed:
        arm (True)
        set_mode(custom_mode = "OFFBOARD")


    print(str(current_state.mode))

    if current_state.armed == True:
        rospy.loginfo("DRONE ARMED")

    if current_state.mode == "OFFBOARD":
        rospy.loginfo('OFFBOARD mode setted')

    abs_Goto (0, 0, 2)
    print ('inicia a rotacao')
    abs_rotation(math.pi)
    print('termina a rotacao')
    abs_Goto(2, 0, 2)
