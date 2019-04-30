import rospy
import mavros_msgs
from mavros_msgs import srv
from geometry_msgs.msg import PoseStamped, TwistStamped
from std_msgs.msg import String
from mavros_msgs.msg import State


goal_pose = PoseStamped()
current_state = State()
velocity_set = TwistStamped()
current_pose = PoseStamped()
controle = String()

def set_position(x, y, z):
    global goal_pose
    goal_pose.pose.position.x = x
    goal_pose.pose.position.y = y
    goal_pose.pose.position.z = z
    local_position_pub.publish(goal_pose)

def state_callback(state_data):
    global current_state
    current_state = state_data

def pose_callback(pose_data):
    global current_pose
    current_pose = pose_data

def publish_vel(i, j, k):
    global velocity_set
    velocity_set.twist.linear.x = i
    velocity_set.twist.linear.y = j
    velocity_set.twist.linear.z = k
    velocity_set.twist.angular.x = 0
    velocity_set.twist.angular.y = 0
    velocity_set.twist.angular.z = 0
    vel_publisher.publish(velocity_set)
    print("PUBLISHED MSG " + str(velocity_set))

def publish_ang_vel(w):
    global velocity_set
    velocity_set.twist.linear.x = 0
    velocity_set.twist.linear.y = 0
    velocity_set.twist.linear.z = 0
    velocity_set.twist.angular.x = 0
    velocity_set.twist.angular.y = 0
    velocity_set.twist.angular.z = w
    vel_publisher.publish(velocity_set)

def controle_callback(msg):
    global controle
    controle = msg

rospy.init_node('Vel_Control_Node', anonymous=True)
rate = rospy.Rate(20)
local_position_pub = rospy.Publisher('mavros/setpoint_position/local', PoseStamped, queue_size=10)
state_status_subscribe = rospy.Subscriber('/mavros/state', State, state_callback)
arm = rospy.ServiceProxy('/mavros/cmd/arming', mavros_msgs.srv.CommandBool)
set_mode = rospy.ServiceProxy('/mavros/set_mode', mavros_msgs.srv.SetMode)
vel_publisher = rospy.Publisher('/mavros/setpoint_velocity/cmd_vel', TwistStamped, queue_size=100)
control_sub = rospy.Subscriber('controle', String, controle_callback)
pose_sub = rospy.Subscriber('/mavros/local_position/pose',PoseStamped, pose_callback, queue_size=3)


for i in range(300):
    local_position_pub.publish(goal_pose)
    rate.sleep()
    rospy.loginfo("[ROS] SETUP CONCLUIDO  " + str(i))

# -------- VERIFICAO OFFBOARD E SE ESTA ARMADO --------------- #
while not current_state.armed:
    if current_state.mode != "OFFBOARD" or not current_state.armed:
        arm(True)
        set_mode(custom_mode="OFFBOARD")
    print(str(current_state.mode))

if current_state.armed == True:
    rospy.loginfo("Drone armed")

rospy.logwarn("TAKING OFF")
for i in range(30):
    set_position(0, 0, 2)
    rate.sleep()

publish_vel(0, 0, 0)
publish_ang_vel(0)
while not rospy.is_shutdown():
    #publish_vel(1, 0, 0)
    #print(controle)
    # if current_state.mode == "OFFBOARD":
    #     rospy.loginfo('OFFBOARD mode setted')
    if controle.data == "forward":
        rospy.loginfo("Going" + str(controle.data))
        publish_vel(1,0,0)
        rate.sleep()
    elif controle.data == "back":
        rospy.loginfo("Going" + str(controle.data))
        publish_vel(-1,0,0)
        rate.sleep()
    elif controle.data == "left":
        rospy.loginfo("Going" + str(controle.data))
        publish_vel(0,1,0)
        rate.sleep()
    elif controle.data == "right":
        rospy.loginfo("Going" + str(controle.data))
        publish_vel(0,-1,0)
        rate.sleep()
    elif controle.data == "up":
        rospy.loginfo("Going" + str(controle.data))
        publish_vel(0,0,1)
        rate.sleep()
    elif controle.data == "down":
        rospy.loginfo("Going" + str(controle.data))
        publish_vel(0,0,-1)
        rate.sleep()
    elif controle.data == "stop":
        rospy.loginfo("Going" + str(controle.data))
        publish_vel(0,0,0)
        rate.sleep()
    elif controle.data == "yaw-antihorario":
        rospy.loginfo("Going" + str(controle.data))
        publish_ang_vel(0,0,1)
        rate.sleep()
    elif controle.data == "yaw-horario":
        rospy.loginfo("Going" + str(controle.data))
        publish_ang_vel(0,0,-1)
        rate.sleep()
    elif controle.data == "disarm":
        while not current_pose.pose.position.z < 0.5:
            rospy.loginfo("LANDING")
            publish_vel(0,0,-0.5)
            rate.sleep()
        rospy.logwarn('DISARMING DRONE')
        for i in range(30):
            arm(False)
        rospy.logwarn('DRONE DISARMED')
    else:
        rospy.loginfo("Stairing")
        publish_vel(0,0,0)
    rate.sleep()
# ------------------------------------------------------------------ #
