import rospy
import time
from geometry_msgs.msg import PoseStamped
drone_pose = PoseStamped()

def local_callback(local):
    global drone_pose

    drone_pose.pose.position.x = local.pose.position.x
    drone_pose.pose.position.y = local.pose.position.y
    drone_pose.pose.position.z = local.pose.position.z

rospy.init_node('position_printer')
rate = rospy.Rate(60)
local_atual = rospy.Subscriber('/mavros/local_position/pose', PoseStamped, local_callback)

while not rospy.is_shutdown():
    #info = 'Position: (' + str(drone_pose.pose.position.x) + ', ' + str(drone_pose.pose.position.y) + ', ' + str(drone_pose.pose.position.z) +   ')'
    rospy.loginfo(drone_pose)
    rate.sleep()
