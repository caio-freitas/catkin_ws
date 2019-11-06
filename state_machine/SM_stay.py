#!/usr/bin/env python

import rospy
import smach
import smach_ros
import takeoff
import RTL
from RTL import drone_RTL
from takeoff import drone_takeoff
from validation import drone_validate
from stay import drone_stay

# define state Takeoff
class Takeoff(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['done','aborted'])
        self.counter = 0

    def execute(self, userdata):
        rospy.loginfo('Executing state Takeoff')
        # height = input('Digite a altura do droe: ')
        # time = input('Digite o tempo de voo: ')
        height=2
        time=15
        return takeoff.drone_takeoff(height, time)


class Validation(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['validated', 'overheat', 'low_battery'])

    def execute(self, userdata):
        print userdata
        return drone_validate()


 # define state RTL
class ReturnToLand(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['succeeded'])

    def execute(self, userdata):
        RTL.drone_RTL()
        rospy.loginfo('Executing state RTL')
        return 'succeeded'

class Stay(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['done'])

    def execute(self, userdata):
        dur = 10 #in seconds
        rospy.loginfo('Executing state STAY for {} seconds'.format(dur))
        return drone_stay(dur)

rospy.init_node('drone_state_machine', anonymous = True)
rate = rospy.Rate(20) # 10hz

def main():

    # Create a SMACH state machine
    sm = smach.StateMachine(outcomes=['Mission executed successfully!'])

    # Open the container
    with sm:
        # Add states to the container
        smach.StateMachine.add('TAKEOFF', Takeoff(),
                                transitions={'done':'STAY', 'aborted':'Mission executed successfully!'})

        # smach.StateMachine.add('VALIDATION', Validation(),
        #                 transitions={'validated':'RTL', 'overheat':'RTL', 'low_battery':'RTL'})

        smach.StateMachine.add('STAY', Stay(),
                                transitions={'done':'RTL'})

        smach.StateMachine.add('RTL', ReturnToLand(),
                                transitions={'succeeded':'Mission executed successfully!'})

     # Execute SMACH plan
    outcome = sm.execute()
    print outcome



if __name__ == '__main__':
    main()
