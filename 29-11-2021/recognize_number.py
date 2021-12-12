from numpy import argmax
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
import numpy as np


def to_grayscale(images_array):
    result = [list() for _ in range(images_array.shape[0])]
    for i in range(images_array.shape[0]):
        result1 = [list() for _ in range(images_array.shape[1])]
        for j in range(images_array.shape[1]):
            rgb = images_array[i][j]
            x = int(0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2])
            result1[j] = [x]
        result[i] = result1
    return np.array(result, dtype='uint8')


# load and prepare the image
def load_image(filename):
    # load the image
    img = load_img(filename, color_mode='grayscale', target_size=(28, 28))
    # convert to array
    img = img_to_array(img)
    # reshape into a single sample with 1 channel
    img = img.reshape(1, 28, 28, 1)
    # prepare pixel data
    img = img.astype('float32')
    img = img / 255.0
    return img


# load an image and predict the class
def run_example(file_name):
    # load the image
    img = load_image(file_name)
    # load model
    model = load_model('final_model.h5')
    # predict the class
    predict_value = model.predict(img)
    digit = argmax(predict_value)
    return digit
