#!/usr/bin/env python

import rospy
import mavros_msgs
from mavros_msgs import srv
from geometry_msgs.msg import PoseStamped, Quaternion
from mavros_msgs.msg import State
import time
import math

drone_pose = PoseStamped()
goal_pose = PoseStamped()
drone_state = State()
goal_rotation = Quaternion()


def set_position(x, y, z):
    global goal_pose
    global goal_rotation
    goal_pose.pose.position.x = x
    goal_pose.pose.position.y = y
    goal_pose.pose.position.z = z
    goal_pose.pose.orientation = goal_rotation
    local_position_pub.publish(goal_pose)


def state_callback(state_data):
    global drone_state
    drone_state = state_data


def local_callback(local):
    global drone_pose
    drone_pose = local

def set_goal_rotation(theta, (x,y,z)):
    global goal_rotation
    theta = math.pi*theta/360
    if x*x + y*y + z*z != 1:
        norm = math.sqrt((x*x) + (y*yo) + (z*z))
        x /= norm
        y /= norm
        z /= norm

    goal_rotation.x = math.sin(theta)*x
    goal_rotation.y = math.sin(theta)*y
    goal_rotation.z = math.sin(theta)*z
    goal_rotation.w = math.cos(theta)

def get_orientation():
    global drone_pose
    theta = 360*math.acos(drone_pose.pose.orientation.w)/(math.pi)
    t = (drone_pose.pose.orientation.x/math.sin(theta), drone_pose.pose.orientation.y/math.sin(theta), drone_pose.pose.orientation.z/math.sin(theta))
    return theta, t

rospy.init_node('Vel_Control_Node', anonymous = True)

rate = rospy.Rate(20)

local_position_pub = rospy.Publisher('/mavros/setpoint_position/local', PoseStamped, queue_size = 100)

########### Subscribers ##################
local_atual = rospy.Subscriber('/mavros/local_position/pose', PoseStamped, local_callback)

state_status_subscribe = rospy.Subscriber('/mavros/state', State, state_callback)

############## Services ##################

arm = rospy.ServiceProxy('/mavros/cmd/arming', mavros_msgs.srv.CommandBool)

set_mode = rospy.ServiceProxy('/mavros/set_mode', mavros_msgs.srv.SetMode)
set_goal_rotation(0, (0,0,1))
set_position(0,0,0)
for i in range(300):
    local_position_pub.publish(goal_pose)
    arm(True)
    rate.sleep()

rospy.loginfo("[ROS] SETUP CONCLUIDO")

ds = 0
while not rospy.is_shutdown():
    angle, tang = get_orientation()
    rospy.loginfo("DRONE ORIENTATION: {} DEGREES AROUND THE AXIS {}".format(angle, str(tang)))
    if drone_state != "OFFBOARD" or not drone_state.armed:
        arm (True)
        set_mode(custom_mode = "OFFBOARD")

    print(str(drone_state.mode))

    if drone_state.armed == True:
        rospy.loginfo("DRONE ARMED")

    else:
        rospy.logwarn("DRONE DISARMED")

    if drone_state.mode == "OFFBOARD":
        rospy.loginfo('OFFBOARD mode setted')

    else:
        rospy.loginfo(drone_state)

    set_position(0, 0, 2)
    set_goal_rotation(ds, (0,0,1))
    ds += 1
    # rospy.loginfo('ds = ' + str(ds))
    rate.sleep()
