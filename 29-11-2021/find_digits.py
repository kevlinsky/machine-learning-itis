import cv2
from tensorflow.keras.models import load_model
from numpy import argmax
import numpy as np

model = load_model('final_model.h5')
ex = []


def to_grayscale(images_array):
    result = [list() for _ in range(images_array.shape[0])]
    for i in range(images_array.shape[0]):
        result1 = [list() for _ in range(images_array.shape[1])]
        for j in range(images_array.shape[1]):
            rgb = images_array[i][j]
            x = int(0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2])
            result1[j] = [x]
        result[i] = result1
    result_array = np.array(result, dtype='uint8')
    return result_array.reshape((1, 28, 28, 1))


def makeSquare(not_square):
    BLACK = [0, 0, 0]
    img_dim = not_square.shape
    height = img_dim[0]
    width = img_dim[1]

    if height == width:
        square = not_square
        return square
    else:
        doublesize = cv2.resize(not_square, (2 * width, 2 * height), interpolation=cv2.INTER_CUBIC)
        height = height * 2
        width = width * 2

        if height > width:
            pad = int((height - width) / 2)

            doublesize_square = cv2.copyMakeBorder(doublesize, 0, 0, pad, pad, cv2.BORDER_CONSTANT, value=BLACK)
        else:
            pad = int((width - height) / 2)

            doublesize_square = cv2.copyMakeBorder(doublesize, pad, pad, 0, 0, cv2.BORDER_CONSTANT, value=BLACK)

    return doublesize_square


def check_exist(coors):
    for e in ex:
        if abs(e[0] - coors[0]) <= 50:
            return True
    ex.append(coors)
    return False


def recognize_number(filename):
    result_number = []

    im = cv2.imread(filename)
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.adaptiveThreshold(blur, 255, 1, 1, 11, 2)

    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=lambda c: cv2.boundingRect(c)[0])

    for idx, cnt in enumerate(contours):
        if cv2.contourArea(cnt) > 200:
            x, y, w, h = cv2.boundingRect(cnt)
            digit = im[y:y + h, x:x + w]
            squared_digit = makeSquare(digit)

            if 150 < squared_digit.shape[0] < 250 and 150 < squared_digit.shape[1] < 250 and not check_exist((x, y)):
                resized_squared_digit = cv2.resize(squared_digit, dsize=(28, 28))
                cv2.imwrite(f'digit{idx}.png', resized_squared_digit)
                x = to_grayscale(resized_squared_digit)
                predict_value = model.predict(x)
                result_number.append(argmax(predict_value))

    return result_number
