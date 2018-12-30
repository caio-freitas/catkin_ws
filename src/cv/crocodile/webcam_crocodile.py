import numpy as np
import cv2
import keras


model = keras.models.load_model('convNN.model')
print(model)
IMG_SIZE = 80

#run with KERAS_BACKEND=theano python detect.py

def crocodile(img):
    image = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
    #blur = cv2.GaussianBlur(image,(5,5),0)
    blur = image
    ready_to_predict = np.array(blur).reshape(-1, IMG_SIZE, IMG_SIZE, 1)
    ready_to_predict = ready_to_predict/255.0
    prediction = model.predict(ready_to_predict)
    #Hello, Bayes
    print(prediction)
    if prediction[0][0] > 0.5:
        print("CROCODILE")
    else:
        print("NOT A CROCODILE")

# run with KERAS_BACKEND=theano python detect.py
def main():
    cap = cv2.VideoCapture(-1)
    while (1):
        rec, image = cap.read()
        crocodile(image)
        cv2.imshow("WebCam", image)

        ### MAGICA ######
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break
        #################



if __name__ == "__main__":
    main()
