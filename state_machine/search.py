#!/usr/bin/env python

import rospy
import mavros_msgs
from geometry_msgs.msg import PoseStamped, TwistStamped
import time

################# Objetos ############
goal_pose = PoseStamped()
drone_pose = PoseStamped()
final_pose = PoseStamped()


def chegou(goal, actual):
    if (abs(goal.pose.position.x - actual.pose.position.x) < 0.01) and (abs(goal.pose.position.y - actual.pose.position.y) < 0.01) and (abs(goal.pose.position.z - actual.pose.position.z) < 0.01):
        return True
    else:
        return False

def drone_search((x_init, y_init), (x_dim, y_dim), width, velocity):

    def state_callback(state_data):
        global drone_state
        drone_state = state_data


    rate = rospy.Rate(20) # 20hz
    ############## Funcao de Callback ########
    def local_callback(local):
        global drone_pose

        drone_pose.pose.position.x = local.pose.position.x
        drone_pose.pose.position.y = local.pose.position.y
        drone_pose.pose.position.z = local.pose.position.z
    def set_position(x, y, z):
        global goal_pose
        goal_pose.pose.position.x = x
        goal_pose.pose.position.y = y
        goal_pose.pose.position.z = z
        local_position_pub.publish(goal_pose)
    ############### Publishers ###############
    local_position_pub = rospy.Publisher('/mavros/setpoint_position/local', PoseStamped, queue_size = 100)

    ########### Subscribers ##################
    local_atual = rospy.Subscriber('/mavros/local_position/pose', PoseStamped, local_callback)
    #rospy.init_node("search")
    for i in range(100):
        set_position(drone_pose.pose.position.x,drone_pose.pose.position.y,drone_pose.pose.position.z)
        rate.sleep()
    x_dim = 10
    y_dim = 10
    width = 1
    velocity = 1 #Velocidade em m/s
    part = velocity/20.0 # se o rospy.Rate() for 20 Hz
    height = 2
    # if y_dim % width != 0:
    #     rospy.logerr("O lado do retangulo deve ser um multiplo da largura")
    #     return 'erro'

    side_time = x_dim/velocity
    width_time = width/velocity

    final_pose.pose.position.x = x_dim
    final_pose.pose.position.y = y_dim
    final_pose.pose.position.z = height



    init_time = time.time()
    set_position(x_init, y_init, height)
    t=0
    round=0
    #while not chegou(final_pose, drone_pose):
    while round < 6:
        #Loops para as curvas (t, 0); (0, t), (-t, 0), (0, t)
        while t != x_dim and drone_pose.pose.position.x <= x_init + x_dim:
            print("First loop")
            print("Position: (" + str(drone_pose.pose.position.x)+  ", "+ str(drone_pose.pose.position.y)+ ", "+ str(drone_pose.pose.position.z), ")")
            set_position(x_init + t, y_init + round*width, height)
            t = t + part
            rate.sleep()
        for i in range(20):
            set_position(x_init + x_dim, y_init + round*width, height)
            rate.sleep()
        t=0

        while t != width and drone_pose.pose.position.y <= y_init + (round+1)*width:
            print("Second Loop")
            print("Position: (" + str(drone_pose.pose.position.x)+  ", "+ str(drone_pose.pose.position.y)+ ", "+ str(drone_pose.pose.position.z), ")")
            set_position(x_init + x_dim, y_init + round*width + t, height)
            t = t + part
            rate.sleep()
        for i in range(20):
            set_position(x_init + x_dim, y_init + (round+1)*width, height)
            rate.sleep()
        t=0

        round += 1

        while t != x_dim and drone_pose.pose.position.x >= x_init:
            print("Third Loop")
            print("Position: (" + str(drone_pose.pose.position.x)+  ", "+ str(drone_pose.pose.position.y)+ ", "+ str(drone_pose.pose.position.z), ")")
            set_position(x_init + x_dim - t, y_init + round*width, height)
            t = t + part
            rate.sleep()
        for i in range(20):
            set_position(x_init, y_init + round*width, height)
            rate.sleep()
        t=0

        while t != width and drone_pose.pose.position.y <= y_init + (round+1)*width:
            print("Fourth Loop")
            print("Position: (" + str(drone_pose.pose.position.x)+  ", "+ str(drone_pose.pose.position.y)+ ", "+ str(drone_pose.pose.position.z), ")")
            set_position(x_init, y_init + t + round*width, height)
            t = t + part
            rate.sleep()
        for i in range(20):
            set_position(x_init, y_init + (round+1)*width, height)
            rate.sleep()
        t=0
        round += 1

        print("Position: (" + str(drone_pose.pose.position.x)+  ", "+ str(drone_pose.pose.position.y)+ ", "+ str(drone_pose.pose.position.z), ")")

        rate.sleep()

    rospy.loginfo("")
    return 'done'

if __name__ == "__main__":
    drone_search((0, 0), (10, 10), 1, 1)
