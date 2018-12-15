#!/usr/bin/env python

import time
import rospy
import smach
import mavros_msgs
from smach_ros import condition_state
#from smach import StateMachine
from mavros_msgs import srv
from geometry_msgs.msg import PoseStamped, TwistStamped
from sensor_msgs.msg import BatteryState
from mavros_msgs.msg import State
from RTL import drone_RTL
from takeoff import drone_takeoff

import smach_ros
import roslib

# Estado responsavel por decolar o drone a uma altura de 2 metros; tem como outcomes: succeeded, preempted, aborted
#class Takeoff(condition_state.ConditionState):
class Takeoff(smach.State):
    def __init__(self):
        smach.State.__init__(self,
        outcomes=['succeeded', 'aborted'])


    def execute(self):
        outcome = takeoff.drone_takeoff()
        if True:
            return 'succeeded'
        else:
            return 'aborted'

# Estado responsavel por trazer o drone de volta a posicao (0,0,0)
class ReturnToLand(smach.State):
    def __init__(self):
        smach.State.__init__(self,
        outcomes=['succeeded'])

    def execute(self):
        rospy.loginfo('Executing state ReturnToLand')
        takeoff.drone_RTl()
        return 'succeeded'




def main():
    rospy.init_node('state_machine')


    state_machine = smach.StateMachine(outcomes=['deuBom'])


    with state_machine:
        #smach.StateMachine.add("TAKEOFF", Takeoff(), transitions={"succeeded":"SQUARE", "preempted":"RTL","aborted":"DISARM"})
        smach.StateMachine.add('TAKEOFF', Takeoff(), transitions={'succeeded':'RTL', 'aborted':'deuBom'})
        smach.StateMachine.add('RTL', ReturnToLand(), transitions={'succeeded':'deuBom'})
        #smach.StateMachine.add("RTL", ReturnToLand(), transitions={"succeeded":"TAKEOFF", "aborted":"TAKEOFF"})
        # smach.StateMachine.add("SQUARE", Square(), transitions={"low_battery":"RTL"})

    output = state_machine.execute()



if __name__ == "__main__":
    main()
