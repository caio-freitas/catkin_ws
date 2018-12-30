# import the necessary packages
import numpy as np
import argparse
import cv2
import time


# to the new height, clone it, and resize it

def showCorners(image):
    img = image.copy()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    corners = cv2.goodFeaturesToTrack(gray, 100, 0.3, 15)
    corners = np.int0(corners)

    print(corners.shape)
    print(gray.shape)
    for corner in corners:
        x, y = corner.ravel()
        cv2.circle(img, (x, y), 5, (0,255,0), -1)
        cv2.imshow("Corners", img)

    #return corners
cap = cv2.VideoCapture(-1)
while True:
    rec, image = cap.read()

    showCorners(image)
    cv2.imshow("Camera", image)

    #### MAGICA ######
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
    #################

cap.release()
cv2.destroyAllWindows()
