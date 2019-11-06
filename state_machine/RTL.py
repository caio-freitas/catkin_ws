#!/usr/bin/env python

import rospy
import mavros_msgs
from mavros_msgs import srv
from geometry_msgs.msg import PoseStamped, TwistStamped
from mavros_msgs.msg import State
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


"""
Function that brings the drone down to the (0,0,0) position

"""

def drone_RTL():
    init_time = time.time()
    rate = rospy.Rate(100)
    velocity = 0.3
    ds = velocity/100.0
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

    for i in range(100):
        set_position(0,0,0)
        rate.sleep()

    rospy.loginfo("[ROS] SETUP CONCLUIDO")
    transition_time = time.time() - init_time
    rospy.logwarn('Time in setup: ' + str(transition_time))
    rate.sleep()
    height = drone_pose.pose.position.z
    rospy.loginfo('Position: (' + str(drone_pose.pose.position.x) + ', ' + str(drone_pose.pose.position.y) + ', ' + str(drone_pose.pose.position.z) + ')')

    set_position(0,0,height)
    rate.sleep()
    rospy.loginfo('Position: (' + str(drone_pose.pose.position.x) + ', ' + str(drone_pose.pose.position.y) + ', ' + str(drone_pose.pose.position.z) + ')')
    rospy.loginfo('Goal Position: (' + str(goal_pose.pose.position.x) + ', ' + str(goal_pose.pose.position.y) + ', ' + str(goal_pose.pose.position.z) + ')')


    while not chegou(drone_pose, goal_pose):
        rospy.loginfo('Executing State RTL')
        rospy.loginfo ("STARING HOME")
        set_position(0,0,height)
        rate.sleep()

    t=0
    set_position(0,0,height-ds)
    rate.sleep()

    while not drone_pose.pose.position.z < 0.3:
        rospy.loginfo('Executing State RTL')

        rospy.loginfo('Height: ' + str(abs(drone_pose.pose.position.z)))
        #print drone_pose
        if not chegou(drone_pose, goal_pose):
            rospy.logwarn ('LANDING AT ' + str(velocity) + 'm/s')
            if t <= height:
                t += ds
            set_position(0,0,height - t)
            rate.sleep()

        else:
            if t <= height:
                t += ds
                set_position(0,0,height - t)
            else:
                set_position(0,0,0)
            rate.sleep()

    print("\nCHEGUEEEI\n")
    cmd = 0
    while not cmd == 1:
        cmd = input("Posso desarmar o drone? (1 para sim, 0 para nao)\n")
        set_position(0,0,0)
        rate.sleep()
    rospy.logwarn("DESARMANDO DRONE")
    arm(False)
    return "succeeded"

if __name__ == "__main__":
    rospy.init_node("RTL")
    drone_RTL()
