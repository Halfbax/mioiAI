import tensorflow as tf
import numpy as np
import os

from PIL import Image
from gesture import Gesture

class Predictor:
    model = None
    data = None
    history = None

    def __init__(self):
        np.set_printoptions(suppress=True)


        self.model = tf.keras.models.load_model(os.path.join(os.path.dirname(__file__), "../models/keras_model.h5"))

        self.model.compile(optimizer=tf.keras.optimizers.RMSprop(),
                loss=tf.keras.losses.SparseCategoricalCrossentropy(),
                metrics=[tf.keras.metrics.SparseCategoricalAccuracy()])

        # Create the array of the right shape to feed into the keras model
        # The 'length' or number of images you can put into the array is
        # determined by the first position in the shape tuple, in this case 1.
        self.data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

        self.history = [None for i in range(20)]

    def predict(self, image, sock):
        image_array = np.asarray(image)
        normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1

        # Load the image into the array
        self.data[0] = normalized_image_array
        
        # run the inference
        pred = self.model.predict(self.data, use_multiprocessing=True, verbose=False)        

        # debug information
        self.history.append(np.argmax(pred))
        self.history.pop(0)

        if len(dict.fromkeys(self.history)) == 1:          
            SocketHelper.send(sock, self.history, True, True)