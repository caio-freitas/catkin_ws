#!/usr/bin/env python

import rospy
import mavros_msgs
from mavros_msgs import srv
from geometry_msgs.msg import PoseStamped, TwistStamped
from mavros_msgs.msg import State
import time
import math

goal_pose = PoseStamped() #Possicao que voce deseja ir
local = PoseStamped() #capta a posicao q vc esta
Glocal = PoseStamped() #variavel que recebe a posicao q esta e usaremos para comparacoes
current_state = State() #recebe o estado da maquina

#set_posicao recebe de parametros a posicao que deseja ir e publicara


#rospy.init_node('Vel_Control_Node', anonymous = True)
#rate = rospy.Rate(10)


def fazCirculo(R):
    rospy.init_node('Vel_Control_Node', anonymous = True)
    rate = rospy.Rate(10)

    def set_position(x, y, z):
        global goal_pose
        goal_pose.pose.position.x = x
        goal_pose.pose.position.y = y
        goal_pose.pose.position.z = z
        local_position_pub.publish(goal_pose)

    #state_callback subscrevera e recebera o status do DRONE
    def state_callback(state_data):
        global current_state
        current_state = state_data

    #local_callback subscrevera e recebera a localizacao atual do DRONE
    def local_callback(local):
        global Glocal
        Glocal.pose.position.x = local.pose.position.x
        Glocal.pose.position.y = local.pose.position.y
        Glocal.pose.position.z = local.pose.position.z

        #Definicao dos publishers e subscribers
    local_position_pub = rospy.Publisher('/mavros/setpoint_position/local', PoseStamped, queue_size = 100)

    local_atual = rospy.Subscriber('/mavros/local_position/pose', PoseStamped, local_callback)
    arm = rospy.ServiceProxy('/mavros/cmd/arming', mavros_msgs.srv.CommandBool)

    def chegou (x,y):
        if (abs(x.pose.position.z - y.pose.position.z) < 0.1) and (abs(x.pose.position.y - y.pose.position.y) < 0.1) and (abs(x.pose.position.x - y.pose.position.x) < 0.1):
            return True
        return False

    if not current_state.armed:
        arm(True)

    part = 0.1
    i=0
    while(i<500):
        print("LOOP ETERNO")
        theta = (3/4)*math.pi + part
        #if not chegou(goal_pose, Glocal):
        set_position(R*math.cos(theta), R + R*math.sin(theta), h)
        part = part + 0.06
        i = i + 1
        rate.sleep()
    return 'done'

h = 2
x = 0

def main():
    fazCirculo(1)


if __name__ == "__main__":
    main()
