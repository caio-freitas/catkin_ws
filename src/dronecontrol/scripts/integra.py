import rospy
import mavros_msgs
from mavros_msgs import srv
from geometry_msgs.msg import PoseStamped, TwistStamped
from mavros_msgs.msg import State
from std_msgs.msg import String

current_state = State()
msg = String()
drone_pose = PoseStamped()
goal_pose = PoseStamped()
twist = TwistStamped()

def msg_callback(data):
    global msg
    msg = data

def local_callback(local):
    global drone_pose
    drone_pose = pose

def state_callback(state):
    global drone_state
    drone_state = state

local_position_pub = rospy.Publisher('/mavros/setpoint_position/local', PoseStamped, queue_size = 10)

vel_pos_pub = rospy.Publisher('/mavros/setpoint_velocity/cmd_vel', TwistStamped, queue_size = 10)

local_atual = rospy.Subscriber('/mavros/local_position/pose', PoseStamped, local_callback)

state_sub = rospy.Subscriber('/mavros/state', State, state_callback)

arm = rospy.ServiceProxy('/mavros/cmd/arming', mavros_msgs.srv.CommandBool)
set_mode = rospy.ServiceProxy('/mavros/set_mode', mavros_msgs.srv.SetMode)
#arming_client = rospy.ServiceClient('/mavros/cmd/arming')

controle_sub = rospy.Subscriber('controle', String, msg_callback)

def main():
    rospy.init_node("integra")
    rate = rospy.Rate(20)

    while not rospy.is_shutdown() and not current_state.connected:
        rospy.spin()
        rospy.sleep()

    goal_pose.pose.position.x=0
    goal_pose.pose.position.y=0
    goal_pose.pose.position.z=2

    for i in range(300):
        local_position_pub.publish(goal_pose)
        rospy.spin()
        rate.sleep()

    if drone_state != "OFFBOARD":
        rospy.loginfo("SETTING OFFBOARD FLIGHT MODE")
        set_mode(custom_mode = "OFFBOARD")

    if not drone_state.armed:
        rospy.logwarn("ARMING DRONE")
        arm(True)

    # last_request = rospy.Time.now()
    #
    # if current_state.mode != "OFFBOARD" and (ros.Time.now() - last_request > ros.Duration(5.0)):
    #     if arming_client.call(arm)
        while not rospy.is_shutdown():
            while msg.data == "forward":
                twist.twist.linear.x = 1.0
            	twist.twist.linear.y = 0.0
            	twist.twist.linear.z = 0.0
                vel_pos_pub.publish(twist)
                rospy.spin()
                rate.sleep()

            while msg.data == "back":
                twist.twist.linear.x = -1.0
            	twist.twist.linear.y = 0.0
            	twist.twist.linear.z = 0.0
                vel_pos_pub.publish(twist)
                rospy.spin()
                rate.sleep()

            while msg.data == "left":
                twist.twist.linear.x = 0.0
            	twist.twist.linear.y = 1.0
            	twist.twist.linear.z = 0.0
                vel_pos_pub.publish(twist)
                rospy.spin()
                rate.sleep()

            while msg.data == "right":
                twist.twist.linear.x = 0.0
            	twist.twist.linear.y = -1.0
            	twist.twist.linear.z = 0.0
                vel_pos_pub.publish(twist)
                rospy.spin()
                rate.sleep()

            while msg.data == "up":
                twist.twist.linear.x = 0.0
            	twist.twist.linear.y = 0.0
            	twist.twist.linear.z = 1.0
                vel_pos_pub.publish(twist)
                rospy.spin()
                rate.sleep()

            while msg.data == "down":
                twist.twist.linear.x = 0.0
            	twist.twist.linear.y = 0.0
            	twist.twist.linear.z = -1.0
                vel_pos_pub.publish(twist)
                rospy.spin()
                rate.sleep()

            while msg.data == "stop":
                twist.twist.linear.z = 0
            	twist.twist.linear.y = 0.0
            	twist.twist.linear.x = 0.0
            	twist.twist.angular.z = 0.0
            	twist.twist.angular.x = 0.0
            	twist.twist.angular.y = 0.0
                vel_pos_pub.publish(twist)
                rospy.spin()
                rate.sleep()

            rospy.spin()
            rospy.sleep()
            local_position_pub.publish(drone_pose)

if __name__ == "__main__":
    main()
