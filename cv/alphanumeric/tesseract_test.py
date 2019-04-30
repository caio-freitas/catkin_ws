from PIL import Image #to load images
import pytesseract
import argparse
import cv2
import os
import time


cap = cv2.VideoCapture(0)
#ret, image = cap.read()
# load the example image and convert it to grayscale
#image = cv2.imread('ex.png')
#gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# check to see if we should apply thresholding to preprocess the
# image

#gray = cv2.threshold(gray, 100, 180,
	#cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
#th2 = gray

#th2 = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            #cv2.THRESH_BINARY_INV,15,15)


#blur = cv2.GaussianBlur(gray,(5,5),0)
#ret3, th3 = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

#th2 = cv2.adaptiveThreshold(gray,255,cv2.THRESH_BINARY_INV|cv2.THRESH_OTSU)[1]

# write the grayscale image to disk as a temporary file so we can
# apply OCR to it
'''
filename = "{}.png".format(os.getpid())
cv2.imwrite(filename, th2
'''

# load the image as a PIL/Pillow image, apply OCR, and then delete
# the temporary file
#text = pytesseract.image_to_string(Image.open(filename))
#text = pytesseract.image_to_string(th3)
# text2 = pytesseract.image_to_boxes(th3)
#os.remove(filename)
#print(text)
# print(text2)

# show the output images
# cv2.imshow("Image", image)
# cv2.imshow("Output", gray)
# cv2.imshow("Th2", th2)
#cv2.imshow("Th3", th3)

while True:
    ret, image = cap.read()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray,(5,5),0)
    ret3, th3 = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    text = pytesseract.image_to_string(th3)
    print(text)
    cv2.imshow("Th3", th3)
    time.sleep(0.03)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
