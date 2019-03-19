import numpy as np
import cv2
import keras
import tensorflow
import pandas as pd
import time
from keras.callbacks import TensorBoard
from keras.models import Sequential
from keras.layers import Conv2D, Dense, Activation, MaxPooling2D, Flatten

gpu_options = tensorflow.GPUOptions(per_process_gpu_memory_fraction=0.5)
sess = tensorflow.Session(config=tensorflow.ConfigProto(gpu_options=gpu_options))

trainX = np.load('train_data.npy')
trainY = pd.read_csv('train_labels.csv', names=["Labels"])

# dense_layers = [0, 1, 2, 3]
# layer_sizes = [32, 64, 128]
# conv_layers = [1, 2, 3]

dense_layers = [0]
layer_sizes = [32, 64]
conv_layers = [1, 3]

for dense_layer in dense_layers:
    for layer_size in layer_sizes:
        for conv_layer in conv_layers:
            NAME = "{}-conv-{}-nodes-{}-dense-{}".format(conv_layer, layer_size, dense_layer, int(time.time()))
            print(NAME)
            tensorboard = TensorBoard(log_dir='logs2/{}'.format(NAME))
            model = Sequential()

            #model.add(Conv2D(64, (3,3), input_shape = (IMG_SIZE, IMG_SIZE, 3), data_format='channels_last'))
            model.add(Conv2D(layer_size, (3,3), input_shape = trainX.shape[1:]))
            model.add(Activation("relu"))
            model.add(MaxPooling2D(2,2))

            for l in range(conv_layer-1):
                model.add(Conv2D(layer_size, (3,3)))
                model.add(Activation("relu"))
                model.add(MaxPooling2D(2,2))

            model.add(Flatten())

            for l in range(dense_layer):
                #model.add(Dropout(0.2))
                model.add(Dense(layer_size))
                model.add(Activation("relu"))


            model.add(Dense(1, activation="sigmoid"))

            model.compile(loss="binary_crossentropy",
                        optimizer = "Adadelta",
                        metrics = ["accuracy"])
            model.fit(trainX, trainY, batch_size=32, epochs=8, validation_split=0.1, callbacks=[tensorboard])
