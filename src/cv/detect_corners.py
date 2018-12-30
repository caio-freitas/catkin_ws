#!/usr/bin/env python

import cv2
import sys
import rospy
import numpy as np
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError


class DetectCorners:
    def __init__(self):
        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber("/camera1/image_raw", Image, self.image_callback)

    def image_callback(self, image):
        try:
            self.cv_image = self.bridge.imgmsg_to_cv2(image, "bgr8")
            self.showCorners()
        except CvBridgeError as e:
            print (e)


        #cv2.imshow("camera1", self.cv_image)
        #self.showCorners()
        cv2.waitKey(3)

    def showCorners(self):
        img = self.cv_image.copy()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        corners = cv2.goodFeaturesToTrack(gray, 100, 0.7, 15)
        corners = np.int0(corners)

        print(corners.shape)
        print(gray.shape)
        for corner in corners:
            x, y = corner.ravel()
            cv2.circle(img, (x, y), 5, (0,255,0), -1)
            print('drawing circles')
        cv2.imshow("Corners", img)

        #return corners


def main(args):
    detecter = DetectCorners()
    rospy.init_node('Detect', anonymous=True)
    rate = rospy.Rate(20)
    while True:
        try:
            rospy.spin()
        except KeyboardInterrupt:
            print('Shutting Down')
    cv2.destroyAllWindows()



if __name__ == "__main__":
    main(sys.argv)
