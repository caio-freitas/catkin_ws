import numpy as np
import cv2
import keras
from drone_video import Video

model = keras.models.load_model('full_dataset_model.model')

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
    video = Video()
    #image = video.frame()
    #cap = cv2.VideoCapture(-1)
    #cap = cv2.VideoCapture("udpsrc port=5600 caps='application/x-rtp, media=(string)video, clock-rate=(int)90000, encoding-name=(string)H264 ! rtph264depay ! avdec_h264 ! clockoverlay valignment=bottom ! autovideosink fps-update-interval=1000 sync=false")
    while (1):
        if not video.frame_available():
            continue
        image = video.frame()
        crocodile(image)
        cv2.imshow("Frame", image)

        ### MAGICA ######
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        #################



if __name__ == "__main__":
    main()
