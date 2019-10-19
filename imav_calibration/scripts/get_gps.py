import numpy as np
import rospy
import cv2
from sensor_msgs.msg import NavSatFix
from geometry_msgs.msg import PoseStamped

drone_pose = NavSatFix()
relative_pose = PoseStamped()

def pose_callback(pose_data):
    global drone_pose
    drone_pose = pose_data

def rel_pose_callback(rel):
    global relative_pose
    relative_pose = rel

pose_sub = rospy.Subscriber('/mavros/global_position/global', NavSatFix, pose_callback, queue_size=3)
rel_sub = rospy.Subscriber('/mavros/local_position/pose', PoseStamped, rel_pose_callback, queue_size = 3)

file = open("vehicle_gps_coordinates.txt", "w+")



rospy.init_node("get_gps")
rate = rospy.Rate(20)

while not drone_pose.status != 0:
    rospy.loginfo("GPS Status: " + str(drone_pose.status))
    rospy.loginfo(str(drone_pose.latitude) + str(drone_pose.longitude))
    rate.sleep()

rospy.loginfo("Drone GPS Coordinates: (" +str(drone_pose.latitude) + ", " + str(drone_pose.longitude) + ")\n")
rospy.loginfo("Drone Relative Coordinates: " + str(relative_pose.pose.position.x) + ", " + str(relative_pose.pose.position.y) + ", " + str(relative_pose.pose.position.z))
file.write(str(drone_pose.latitude) + "\n" + str(drone_pose.longitude) + "\n")
rospy.loginfo("Drone Absolute Coordinates: " + str(relative_pose.pose.position.x) + ", " + str(relative_pose.pose.position.y) + ", " + str(relative_pose.pose.position.z))
