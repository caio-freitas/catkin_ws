#!/usr/bin/env python
'''
    Thread de seguranca que permite mudar o modo de voo do drone para MANUAL
    assim que um toggle no controle remoto e' ativado
'''
import rospy
import mavros_msgs
from mavros_msgs.msg import State
from mavros_msgs.msg import RCIn
import time

drone_state = State()
rc = RCIn()

def rc_callback(data):
    global rc
    rc = data

def safety_thread():
    rate = rospy.Rate(20)
    set_mode = rospy.ServiceProxy('/mavros/set_mode', mavros_msgs.srv.SetMode)
    rc_sub = rospy.Subscriber('/mavros/rc/in', mavros_msgs.msg.RCIn, rc_callback)
    while rc.rssi==0:
        rate.sleep()
    rospy.loginfo("RC SAFETY THREAD INICIALIZED!!")
    while not rospy.is_shutdown():
        #print (rc.channels[16])
        if(rc.channels[16] == 1998):
            for i in range(3):
                rospy.logwarn("SETTING MANUAL FLIGHT MODE")
                set_mode(custom_mode = "MANUAL")
                rate.sleep()
