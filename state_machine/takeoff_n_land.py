#!/usr/bin/env python
#import roslib
import rospy
import smach
import smach_ros
from MAV import MAV
import threading
import time
from align_reference import adjust_position
from std_msgs.msg import Bool

mav = MAV()

# define state Takeoff
class Takeoff(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['done','aborted'])
        self.counter = 0

    def execute(self, userdata):
        global mav
        rospy.loginfo('Executing state Takeoff')
        mav.set_position(0,0,0)
        for i in range(300):
            mav.local_position_pub.publish(mav.goal_pose)
            mav.rate.sleep()
        rospy.loginfo("SETUP COMPLETE")
        result = mav.takeoff(3)
        return result


 # define state RTL
class ReturnToLand(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['succeeded'])

    def execute(self, userdata):
        global mav
        rospy.loginfo('Executing state RTL')
        mav.RTL()
        mav.arm(False)
        return 'succeeded'


#rospy.init_node('drone_state_machine', anonymous = True)
#rate = rospy.Rate(60) # 10hz

def run():
    # Create a SMACH state machine
    #rospy.init_node("State Machine")
    mav = MAV()
    sm = smach.StateMachine(outcomes=['Mission executed successfully!'])
    # Open the container
    with sm:
        # Add states to the container
        smach.StateMachine.add('TAKEOFF', Takeoff(),
                                transitions={'done':'RTL', 'aborted':'Mission executed successfully!'})
        smach.StateMachine.add('RTL', ReturnToLand(),
                                transitions={'succeeded':'Mission executed successfully!'})

     # Execute SMACH plan
    outcome = sm.execute()
    print outcome

if __name__ == '__main__':
    run()
