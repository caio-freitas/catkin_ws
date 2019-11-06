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
        result = mav.takeoff(1.5)
        return result

class AllignMailbox(smach.State):
    def __init__(self):
        self.aligned = Bool()
        self.aligned.data = False
        smach.State.__init__(self, outcomes=['done','aborted'])
        # self.rectangle_detector = rectangle_detector()
        self.pose_adjust = adjust_position()
        self.subcriber = rospy.Subscriber('/control/align_reference/aligned', Bool, self.align_callback)

    def align_callback(self, boolean):
        self.aligned = boolean
        print(self.aligned)

    def execute(self, userdata):
        rospy.loginfo('\n\nAlinhando com as Mailboxes, motherfucker!\n\n')
        # self.rectangle_detector.run()
        self.pose_adjust.run()
        return 'done'

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

def main():
    # Create a SMACH state machine
    #rospy.init_node("State Machine")
    mav = MAV()
    sm = smach.StateMachine(outcomes=['Mission executed successfully!'])
    # Open the container
    with sm:
        # Add states to the container
        smach.StateMachine.add('TAKEOFF', Takeoff(),
                                transitions={'done':'ALLIGN', 'aborted':'Mission executed successfully!'})
        smach.StateMachine.add('ALLIGN', AllignMailbox(),
                                transitions={'done':'RTL', 'aborted':'RTL'})
        smach.StateMachine.add('RTL', ReturnToLand(),
                                transitions={'succeeded':'Mission executed successfully!'})

     # Execute SMACH plan
    outcome = sm.execute()
    print outcome

if __name__ == '__main__':
    main()
