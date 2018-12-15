#!/usr/bin/env python

import roslib
import rospy
import smach
import smach_ros
import takeoff
import RTL
from RTL import drone_RTL
from takeoff import drone_takeoff
from Circulo import fazCirculo

# define state Takeoff
class Takeoff(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['succeeded','aborted'])
        self.counter = 0

    def execute(self, userdata):
        rospy.loginfo('Executing state Takeoff')
        return takeoff.drone_takeoff(2, 15)


 # define state RTL
class ReturnToLand(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['succeeded'])

    def execute(self, userdata):
        RTL.drone_RTL()
        rospy.loginfo('Executing state RTL')
        return 'succeeded'
 # define state RTL
class Circle(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['done'])

    def execute(self, userdata):
        rospy.loginfo('Executing state Circle')
        fazCirculo(2)
        return 'done'


rospy.init_node('drone_state_machine', anonymous = True)
rate = rospy.Rate(20) # 10hz

def main():

    # Create a SMACH state machine
    sm = smach.StateMachine(outcomes=['Mission executed successfully!'])

    # Open the container
    with sm:
        # Add states to the container
        smach.StateMachine.add('TAKEOFF', Takeoff(),
                                transitions={'succeeded':'CIRCLE', 'aborted':'RTL'})
        smach.StateMachine.add('CIRCLE', Circle(),
                                transitions={'done':'RTL'})
        smach.StateMachine.add('RTL', ReturnToLand(),
                                transitions={'succeeded':'Mission executed successfully!'})

     # Execute SMACH plan
    outcome = sm.execute()
    print outcome



if __name__ == '__main__':
    main()
