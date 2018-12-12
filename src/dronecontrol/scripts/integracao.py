import rospy
import mavros_msgs
from mavros_msgs import srv
from geometry_msgs.msg import PoseStamped, TwistStamped
from mavros_msgs.msg import State

import smach

goal_pose = PoseStamped()
current_state = State()
vel_state = TwistStamped()

rospy.init_node('Vel_Control_Node', anonymous=True)
rate = rospy.Rate(20)
local_position_pub = rospy.Publisher('mavros/setpoint_position/local', PoseStamped, queue_size=10)
state_status_subscribe = rospy.Subscriber('/mavros/state', State, state_callback)
arm = rospy.ServiceProxy('/mavros/cmd/arming', mavros_msgs.srv.CommandBool)
set_mode = rospy.ServiceProxy('/mavros/set_mode', mavros_msgs.srv.SetMode)
vel_publisher = rospy.Publisher('/mavros/setpoint_velocity/cmd_vel', geometry_msgs/TwistStamped, vel_callback)

# def set_position(x, y, z):
#     global goal_pose
#     goal_pose.pose.position.x = x
#     goal_pose.pose.position.y = y
#     goal_pose.pose.position.z = z
#     local_position_pub.publish(goal_pose)
#
# def state_callback(state_data):
#     global current_state
#     current_state = state_data

def vel_callback(vel_data):
    global vel_state
    vel_state.twist.linear.x = vel_data.twist.linear.x
    vel_state.twist.linear.y = vel_data.twist.linear.y
    vel_state.twist.linear.y = vel_data.twist.linear.y

    vel_state.twist.angular.x = vel_data.twist.angular.x
    vel_state.twist.angular.y = vel_data.twist.angular.y
    vel_state.twist.angular.z = vel_data.twist.angular.z

for i in range(300):
    local_position_pub.publish(goal_pose)
    rate.sleep()
    rospy.loginfo("[ ROS] SETUP CONCLUIDO")

while not rospy.is_shutdown():
# -------- VERIFICAO OFFBOARD E SE ESTA ARMADO --------------- #
    if current_state.mode != "OFFBOARD" or not current_state.armed:
        arm(True)
        set_mode(custom_mode="OFFBOARD")
    print(str(current_state.mode))

    elif current_state.armed == True:
        rospy.loginfo("Drone armed")

    elif current_state.mode == "OFFBOARD":
        rospy.loginfo('OFFBOARD mode setted')
# ------------------------------------------------------------------ #
    set_position(0, 0, 2)
    rate.sleep()
