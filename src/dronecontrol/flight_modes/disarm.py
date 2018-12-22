#!/usr/bin/env python

import rospy
import mavros_msgs
from mavros_msgs import srv

rospy.init_node("EmergencyDisarm")
rate = rospy.Rate(20)
arm = rospy.ServiceProxy('/mavros/cmd/arming', mavros_msgs.srv.CommandBool)

arm(False)
