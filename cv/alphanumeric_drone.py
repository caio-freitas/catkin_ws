import rospy
import numpy as np
import cv2
import cv_bridge
from sensor_msgs.msg import Image
from drone_video import Video
import pytesseract


class DetectAlphanumeric:
    def __init__(self):
        self.video = Video()
        self.frame = self.video.frame()

    def detect(self):
        self.frame = self.video.frame()
        self.cv_image = cv_bridge.imgmsg_to_cv2(self.frame)
        #blur = cv2.GaussianBlur(self.frame,(3,3),0)
        ret3, th3 = cv2.threshold(self.frame, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        cv2.imshow("Camera", self.frame)
        cv2.imshow("Threshold",th3)
        text = pytesseract.image_to_string(th3)
        print(text)
        return text

def main():
    detecter = DetectAlphanumeric()
    rospy.init_node('alphanumeric', anonymous=True)
    rate = rospy.Rate(20)
    while True:
        try:
            detecter.detect()
            rate.sleep()
        except KeyboardInterrupt:
            print('Shutting Down')
    cv2.destroyAllWindows()
    rate.sleep()

if __name__ == "__main__":
    main()
