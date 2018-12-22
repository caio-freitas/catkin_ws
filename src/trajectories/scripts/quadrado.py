#!/usr/bin/env python

import smach

import math

import rospy

import mavros_msgs

from sensor_msgs.msg import BatteryState

from mavros_msgs import srv # importando services da omavros

from geometry_msgs.msg import PoseStamped

from mavros_msgs.msg import State # importando classe State da Mavros

# ================= Criacao dos objetos ============================ #

goal_pose = PoseStamped()
current_state = State()
battery = BatteryState()


def set_position(x, y, z):
    global goal_pose
    goal_pose.pose.position.z = z
    goal_pose.pose.position.y = y
    goal_pose.pose.position.x = x
    local_position_pub.publish(goal_pose)

def set_position(x, y, z):
    global goal_pose
    goal_pose.pose.position.z = z
    goal_pose.pose.position.y = y
    goal_pose.pose.position.x = x
    local_position_pub.publish(goal_pose)

def state_callback(state_data):
    global current_state
    current_state = state_data

def callback_battery_status(bateria):
    global voltage
    global current
    global percentage

    voltage = bateria.voltage
    current = bateria.current
    percentage = bateria.percentage

def callback_position(posicao):

    global pos_atual_x
    global pos_atual_y
    global pos_atual_z
    pos_atual_x = posicao.pose.position.x
    pos_atual_y = posicao.pose.position.y
    pos_atual_z = posicao.pose.position.z


def print_battery_status():

    global voltage, current, percentage

    print ("[ INFO ] V = " + str(voltage) +  " , i = "  + str(current) +  " , Remaning = " + str(percentage))

def print_current_position():

    global pos_atual_x
    global pos_atual_y
    global pos_atual_z

    print("[ INFO ] Posicao X = " + str(pos_atual_x) + " | Posicao Y = " + str(pos_atual_y) + " | Posicao Z = " + str(pos_atual_z))


    # =============== Inicializacao do No e Setup dos topicos =============== #
local_position_pub = rospy.Publisher(
'/mavros/setpoint_position/local', PoseStamped, queue_size=10)

local_position_sub = rospy.Subscriber('/mavros/local_position/pose', PoseStamped, callback_position)

state_status_subscribe = rospy.Subscriber(
'/mavros/state', State, state_callback)
pos_origem_x=0
pos_origem_y=0
pos_origem_z=0
error=0.05

def faz_o_quadradinho(comprimento):
    rospy.init_node("quadrado")
    rate = rospy.Rate(20)  # publish at 20 Hz

    print(" [ INFO ] Doing the Square Mission!")

    while(pos_atual_x != (pos_origem_x + comprimento)):
        # if verification()=='low_battery':
        #     return "low_battery"
        print("[ DEBUG ] Estamos no primeiro Loop")
        set_position(pos_origem_x + comprimento, pos_origem_y, pos_origem_z)
        print_current_position()
        rate.sleep()

        if (abs(pos_atual_x - ( pos_origem_x + comprimento )) < error):

            break

    while(pos_atual_y != (pos_origem_y + comprimento)):
        # if verification()=='low_battery':
        #     return "low_battery"
        print("[ DEBUG ] Estamos no segundo Loop")
        set_position(pos_origem_x + comprimento, pos_origem_y + comprimento, pos_origem_z)
        print_current_position()
        rate.sleep()

        if (abs(pos_atual_y -(pos_origem_y + comprimento)) < error):

            break

    while(pos_atual_x != pos_origem_x):
        # if verification()=='low_battery':
        #     return "low_battery"
        print("[ DEBUG ] Estamos no terceiro Loop")
        set_position(pos_origem_x - comprimento, pos_origem_y + comprimento, pos_origem_z)
        print_current_position()
        rate.sleep()

        if(abs(pos_atual_x - abs(pos_atual_x - comprimento)) < error):

            break

    while(pos_atual_y != pos_origem_y):
        # if verification()=='low_battery':
        #     return "low_battery"
        print("[ DEBUG ] Estamos no quarto Loop")
        set_position(pos_origem_x, pos_origem_y, pos_origem_z)
        print_current_position()
        rate.sleep()

        if(abs(pos_atual_y - abs(pos_atual_y - comprimento)) < error):
            break

if __name__ == "__main__":
    faz_o_quadradinho(2)
