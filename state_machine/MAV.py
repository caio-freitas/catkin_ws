#!/usr/bin/env python
#import roslib
import rospy
import smach
import smach_ros
import mavros_msgs
from mavros_msgs import srv
from geometry_msgs.msg import PoseStamped, TwistStamped
from mavros_msgs.msg import State
import time

TOL = 0.2
MAX_TIME_DISARM = 15

class MAV:
    def __init__(self):
        rospy.init_node("MAV")
        self.rate = rospy.Rate(60)

        self.drone_pose = PoseStamped()
        self.goal_pose = PoseStamped()
        self.goal_vel = TwistStamped()
        self.drone_state = State()
        ############### Publishers ###############
        self.local_position_pub = rospy.Publisher('/mavros/setpoint_position/local', PoseStamped, queue_size = 100)
        self.velocity_pub = rospy.Publisher('/mavros/setpoint_velocity/cmd_vel',  TwistStamped, queue_size=1)
        ########### Subscribers ##################
        self.local_atual = rospy.Subscriber('/mavros/local_position/pose', PoseStamped, self.local_callback)
        self.state_status_subscribe = rospy.Subscriber('/mavros/state', State, self.state_callback)

        ############## Services ##################
        self.arm = rospy.ServiceProxy('/mavros/cmd/arming', mavros_msgs.srv.CommandBool)
        self.set_mode = rospy.ServiceProxy('/mavros/set_mode', mavros_msgs.srv.SetMode)




    ###### Callback Functions ##########
    def state_callback(self, state_data):
        self.drone_state = state_data


    def local_callback(self, local):
        self.drone_pose.pose.position.x = local.pose.position.x
        self.drone_pose.pose.position.y = local.pose.position.y
        self.drone_pose.pose.position.z = local.pose.position.z
    ####### Set Position and Velocity ################
    def set_position(self, x, y, z):
        self.goal_pose.pose.position.x = x
        self.goal_pose.pose.position.y = y
        self.goal_pose.pose.position.z = z
        self.local_position_pub.publish(self.goal_pose)
        self.rate.sleep()

    def set_vel(self, x, y, z, roll=0, pitch=0, yaw=0):
        self.goal_vel.twist.linear.x = x
        self.goal_vel.twist.linear.y = y
        self.goal_vel.twist.linear.z = z

        self.goal_vel.twist.angular.x = roll
        self.goal_vel.twist.angular.y = pitch
        self.goal_vel.twist.angular.z = yaw
        self.velocity_pub.publish(self.goal_vel)

    def chegou(self):
        if (abs(self.goal_pose.pose.position.x - self.drone_pose.pose.position.x) < TOL) and (abs(self.goal_pose.pose.position.y - self.drone_pose.pose.position.y) < TOL) and (abs(self.goal_pose.pose.position.z - self.drone_pose.pose.position.z) < TOL):
            return True
        else:
            return False

    def takeoff(self, height):
        velocity = 0.3
        part = velocity/60.0

        while not self.drone_state.armed:
            rospy.logwarn("ARMING DRONE")
            self.arm(True)
            self.rate.sleep()

        init_time = time.time()

        t=0
        while not rospy.is_shutdown() and self.drone_pose.pose.position.z <= height:
            rospy.loginfo('Executing State TAKEOFF')

            if self.drone_state != "OFFBOARD":
                rospy.loginfo("SETTING OFFBOARD FLIGHT MODE")
                self.set_mode(custom_mode = "OFFBOARD")

            if not self.drone_state.armed:
                rospy.logwarn("ARMING DRONE")
                self.arm(True)
            else:
                rospy.loginfo("DRONE ARMED")

            if t < height:
                rospy.logwarn('TAKING OFF AT ' + str(velocity) + ' m/s')
                self.set_position(0, 0, t)
                t += part
            else:
                self.set_position(0, 0, height)

            rospy.loginfo('Position: (' + str(self.drone_pose.pose.position.x) + ', ' + str(self.drone_pose.pose.position.y) + ', '+ str(self.drone_pose.pose.position.z) + ')')
            self.rate.sleep()

        self.set_position(0, 0, height)

        return "done"


    def RTL(self):
        init_time = time.time()
        velocity = 0.3
        ds = velocity/60.0

        transition_time = time.time() - init_time
        rospy.logwarn('Time in setup: ' + str(transition_time))
        self.rate.sleep()
        height = self.drone_pose.pose.position.z
        rospy.loginfo('Position: (' + str(self.drone_pose.pose.position.x) + ', ' + str(self.drone_pose.pose.position.y) + ', ' + str(self.drone_pose.pose.position.z) + ')')

        self.set_position(0,0,height)
        self.rate.sleep()
        rospy.loginfo('Position: (' + str(self.drone_pose.pose.position.x) + ', ' + str(self.drone_pose.pose.position.y) + ', ' + str(self.drone_pose.pose.position.z) + ')')
        rospy.loginfo('Goal Position: (' + str(self.goal_pose.pose.position.x) + ', ' + str(self.goal_pose.pose.position.y) + ', ' + str(self.goal_pose.pose.position.z) + ')')


        while not self.chegou():
            rospy.loginfo('Executing State RTL')
            rospy.loginfo ("STARING HOME")
            self.set_position(0,0,height)
            self.rate.sleep()

        t=0
        self.set_position(0,0,height-ds)
        self.rate.sleep()

        init_time = time.time()
        while not (self.drone_pose.pose.position.z < -0.1) and time.time() - init_time < (height/velocity)*1.25: #25% tolerance in time
            rospy.loginfo('Executing State RTL')

            rospy.loginfo('Height: ' + str(abs(self.drone_pose.pose.position.z)))
            #print self.drone_pose
            #################### Position Control ##############
            # if not self.chegou():
            #     rospy.logwarn ('LANDING AT ' + str(velocity) + 'm/s')
            #     if t <= height:
            #         t += ds
            #     self.set_position(0,0,height - t)
            #     self.rate.sleep()
            #
            # else:
            #     if t <= height:
            #         t += ds
            #         self.set_position(0,0,height - t)
            #     else:
            #         self.set_position(0,0,0)
            #     self.rate.sleep()
            ####################################################
            ################# Velocity Control #################
            self.set_vel(0, 0, -0.3, 0, 0, 0)
            ####################################################
        print("\nCHEGUEEEI\n")
        rospy.logwarn("DESARMANDO DRONE")
        self.arm(False)
        return "succeeded"

if __name__ == '__main__':
    rospy.init_node("MAV")
    mav = MAV()
    mav.takeoff()
    mav.RTL()
