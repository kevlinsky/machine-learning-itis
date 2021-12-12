from tensorflow.keras.datasets import mnist
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D
from tensorflow.keras.layers import Flatten, Dense
from tensorflow.keras.optimizers import SGD


# def read_labels(filename):
#     result = []
#     with open(filename, 'r') as file:
#         labels = file.read().splitlines()
#     for label in labels:
#         if label != '':
#             result.append(int(label))
#     return np.array(result, dtype='uint8').reshape((len(result),))
#
#
# def to_grayscale(images_array):
#     result = [list() for _ in range(images_array.shape[0])]
#     for i in range(images_array.shape[0]):
#         print(f'Image #{i}')
#         result1 = [list() for _ in range(images_array.shape[1])]
#         for j in range(images_array.shape[1]):
#             result2 = [list() for _ in range(images_array.shape[2])]
#             for k in range(images_array.shape[2]):
#                 rgb = images_array[i][j][k]
#                 x = int(0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2])
#                 result2[k] = [x]
#             result1[j] = result2
#         result[i] = result1
#     return np.array(result, dtype='uint8')
#
#
# def load_dataset():
#     # load dataset
#     filename_dataset_train = tf.data.Dataset.list_files('train_images/*.png')
#     filename_dataset_test = tf.data.Dataset.list_files('test_images/*.png')
#     train_images = filename_dataset_train.map(lambda x: tf.io.decode_png(tf.io.read_file(x))).batch(
#         60000).as_numpy_iterator().next()
#     test_images = filename_dataset_test.map(lambda x: tf.io.decode_png(tf.io.read_file(x))).batch(
#         10000).as_numpy_iterator().next()
#     train_labels = read_labels('train_labels.csv')
#     test_labels = read_labels('test_labels.csv')
#     # (train_images, train_labels), (test_images, test_labels) = mnist.load_data()
#
#     # convert RGB to grayscale
#     train_images = to_grayscale(train_images)
#     print(train_images.shape)
#     test_images = to_grayscale(test_images)
#     print(test_images.shape)
#
#     # # reshape dataset to have a single channel
#     # train_images = train_images.reshape((1, 28, 28, 1))
#     # test_images = test_images.reshape((1, 28, 28, 1))
#
#     # one hot encode target values
#     train_labels = to_categorical(train_labels)
#     test_labels = to_categorical(test_labels)
#
#     return train_images, train_labels, test_images, test_labels

# load train and test dataset
def load_dataset():
    # load dataset
    (trainX, trainY), (testX, testY) = mnist.load_data()
    # reshape dataset to have a single channel
    trainX = trainX.reshape((trainX.shape[0], 28, 28, 1))
    testX = testX.reshape((testX.shape[0], 28, 28, 1))
    # one hot encode target values
    trainY = to_categorical(trainY)
    testY = to_categorical(testY)
    return trainX, trainY, testX, testY


# scale pixels
def prep_pixels(train, test):
    # convert from integers to floats
    train_norm = train.astype('float32')
    test_norm = test.astype('float32')
    # normalize to range 0-1
    train_norm = train_norm / 255.0
    test_norm = test_norm / 255.0
    # return normalized images
    return train_norm, test_norm


# define cnn model
def define_model():
    model = Sequential()
    model.add(Conv2D(32, (3, 3), activation='relu', kernel_initializer='he_uniform', input_shape=(28, 28, 1)))
    model.add(MaxPooling2D((2, 2)))
    model.add(Conv2D(64, (3, 3), activation='relu', kernel_initializer='he_uniform'))
    model.add(Conv2D(64, (3, 3), activation='relu', kernel_initializer='he_uniform'))
    model.add(MaxPooling2D((2, 2)))
    model.add(Flatten())
    model.add(Dense(100, activation='relu', kernel_initializer='he_uniform'))
    model.add(Dense(10, activation='softmax'))
    # compile model
    opt = SGD(learning_rate=0.01, momentum=0.9)
    model.compile(optimizer=opt, loss='categorical_crossentropy', metrics=['accuracy'])
    return model


# run the test harness for evaluating a model
def run_test_harness():
    # load dataset
    train_images, train_labels, test_images, test_labels = load_dataset()
    print('Dataset loaded')

    # prepare pixel data
    train_images, test_images = prep_pixels(train_images, test_images)
    print('Pixels prepared')

    # define model
    model = define_model()
    print('Model defined')

    # fit model
    model.fit(train_images, train_labels, epochs=50, batch_size=256, verbose=1, validation_batch_size=256,
                        validation_data=(test_images, test_labels))
    print('Model trained')

    # save model
    model.save('model.h5')
    print('Model saved to file')


# entry point, run the test harness
if __name__ == '__main__':
    run_test_harness()
