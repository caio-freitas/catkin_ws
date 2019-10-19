#!/usr/bin/env python
#import roslib
import rospy
import smach
#import smach_ros
from states import drone_RTL
from states import drone_takeoff
from geometry_msgs.msg import PoseStamped, TwistStamped
from std_msgs.msg import Bool
import mavros_msgs
import threading
import time
from align_reference import adjust_position
from rectangle_detector import rectangle_detector

import os

goal_pose = PoseStamped()
drone_pose = PoseStamped()

ALTURA_DE_LARGAR_A_CAIXA = 0.4

def chegou(goal, actual):
    if (abs(goal.pose.position.x - actual.pose.position.x) < 0.2) and (abs(goal.pose.position.y - actual.pose.position.y) < 0.2) and (abs(goal.pose.position.z - actual.pose.position.z) < 0.2):
        return True
    else:
        return False

def setVelocity(velocity):
   rospy.wait_for_service('param/set')
   try:
      velocitySetService = rospy.ServiceProxy('param/set', mavros_msgs.srv.ParamSet)
      velocitySetService(velocity)
      rospy.logwarn('Just tried to set velocity parameter')
   except rospy.ServiceException, e:
      rospy.logwarn('FAILED to set velocity parameter')


# define state Takeoff
class Takeoff(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['done','aborted'])
        self.counter = 0

    def execute(self, userdata):
        rospy.loginfo('Executing state Takeoff')
        return drone_takeoff(2, 15)

class Search(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['done','aborted'])

    def execute(self, userdata):
        rospy.loginfo('\n\nExecuting state Search\n\n')
        return 'done'

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

class Wait(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['done','aborted'])

    def execute(self, userdata):
        rospy.loginfo('\n\nExecuting state Wait\n\n')
        return 'done'

class GetToMailbox(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['done','aborted'])

    def execute(self, userdata):
        rospy.loginfo('\n\nExecuting state Wait\n\n')
        return 'done'

#drop the box into the mail box using de pwm of jetson
class DropBox(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['done'])

    def execute(self, userdata):
        rospy.loginfo('Executing state DropBox')
	rospy.loginfo('Executing state DropBox')
        velocity = 0.3
        ds = velocity/20.0
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

        #rospy.loginfo('Position: (' + str(drone_pose.pose.position.x) + ', ' + str(drone_pose.pose.position.y) + ', ' + str(drone_pose.pose.position.z) + ')')
        for i in range(100):
            set_position(drone_pose.pose.position.x,drone_pose.pose.position.y, drone_pose.pose.position.z)
            rate.sleep()
        rospy.loginfo('Position: (' + str(drone_pose.pose.position.x) + ', ' + str(drone_pose.pose.position.y) + ', ' + str(drone_pose.pose.position.z) + ')')
        rospy.loginfo('Goal Position: (' + str(goal_pose.pose.position.x) + ', ' + str(goal_pose.pose.position.y) + ', ' + str(goal_pose.pose.position.z) + ')')
        #########################################################
        initial_pose = PoseStamped()
        initial_pose.pose.position.x = drone_pose.pose.position.x
        initial_pose.pose.position.y = drone_pose.pose.position.y
        initial_pose.pose.position.z = drone_pose.pose.position.z
        final_pose = PoseStamped()
        final_pose.pose.position.x = drone_pose.pose.position.x
        final_pose.pose.position.y = drone_pose.pose.position.y
        final_pose.pose.position.z = ALTURA_DE_LARGAR_A_CAIXA
        ########################################################
        while not drone_pose.pose.position.z < ALTURA_DE_LARGAR_A_CAIXA:
            rospy.logwarn('Dropping box!')
            rospy.loginfo('Position: (' + str(drone_pose.pose.position.x) + ', ' + str(drone_pose.pose.position.y) + ', '+ str(drone_pose.pose.position.z) + ')')
            set_position(drone_pose.pose.position.x,drone_pose.pose.position.y, drone_pose.pose.position.z - 0.1)
            rate.sleep()	
	os.system("python3 PWM_JetsonGPIO.py")
	h = 2
	while not drone_pose.pose.position.z >= h:
	    set_position(0, 0, h)
            rospy.loginfo('Position: (' + str(drone_pose.pose.position.x) + ', ' + str(drone_pose.pose.position.y) + ', '+ str(drone_pose.pose.position.z) + ')')
	    rate.sleep()
	return 'done'


 # define state RTL
class ReturnToLand(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['succeeded'])
        self.state = mavros_msgs.msg.State()
        self.state_status_subscribe = rospy.Subscriber('/mavros/state', mavros_msgs.msg.State, self.state_callback)

    def state_callback(self, data):
        self.state = data


    def execute(self, userdata):
        drone_RTL()
        rospy.loginfo('Executing state RTL')
        drone_disarm()
        # set_mode = rospy.ServiceProxy('/mavros/set_mode', mavros_msgs.srv.SetMode)
        # set_mode(custom_mode="RTL")
        # for i in range(600):
        #     rate.sleep()
        # land = rospy.ServiceProxy('/mavros/cmd/land', mavros_msgs.srv.CommandTOL)
        # land(0, 0, 0, 0, 0)

        return 'succeeded'


rospy.init_node('drone_state_machine', anonymous = True)
rate = rospy.Rate(50) # 10hz

def main():
    # Create a SMACH state machine
    sm = smach.StateMachine(outcomes=['Mission executed successfully!'])
    # Open the container
    with sm:
        # Add states to the container
        smach.StateMachine.add('TAKEOFF', Takeoff(),
                                transitions={'done':'DROP_BOX', 'aborted':'RTL'})
        #smach.StateMachine.add('SEARCH', Search(),
        #                        transitions={'done':'ALLIGN', 'aborted':'RTL'})
#        smach.StateMachine.add('ALLIGN', AllignMailbox(),
#                                transitions={'done':'RTL', 'aborted':'RTL'})
        # smach.StateMachine.add('WAIT', Wait(),
        #                         transitions={'done':'GET_TO_MAILBOX'})
        # smach.StateMachine.add('GET_TO_MAILBOX', GetToMailbox(),
        #                         transitions={'done':'DROP_BOX'})
        smach.StateMachine.add('DROP_BOX', DropBox(),
                                transitions={'done':'RTL'})
        smach.StateMachine.add('RTL', ReturnToLand(),
                                transitions={'succeeded':'Mission executed successfully!'})

     # Execute SMACH plan
    outcome = sm.execute()
    print outcome

if __name__ == '__main__':
    main()
