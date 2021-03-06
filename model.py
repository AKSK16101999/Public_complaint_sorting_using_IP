import numpy as np
import matplotlib.pyplot as plt
import os
from PIL import Image
from sklearn.model_selection import train_test_split
from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Conv2D, MaxPool2D, Dense, Flatten, Dropout
os.chdir("/Users/KANAWADE AKSHAY/Desktop/project/pcm/public/")

data = []
labels = []
# We have 3 Classes
classes = 3
cur_path = os.getcwd()
path = os.path.join(cur_path)
images = os.listdir(path)

for i in range(classes):
    path = os.path.join(cur_path, 'train', str(i))
    images = os.listdir(path)
    for a in images:
        try:
            image = Image.open(path + '/' + a)
            image = image.resize((128, 128))
            image = np.array(image)
            if image.shape == (128, 128, 3):
                data.append(image)
                labels.append(i)
        except Exception as e:
            print(e)

np.save("/Users/KANAWADE AKSHAY/Desktop/project/pcm/training/data", data)
np.save("/Users/KANAWADE AKSHAY/Desktop/project/pcm/training/target", labels)

data = np.load("/Users/KANAWADE AKSHAY/Desktop/project/pcm/training/data.npy")
labels = np.load("/Users/KANAWADE AKSHAY/Desktop/project/pcm/training/target.npy")

print(data.shape, labels.shape)
X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, random_state=0)

print(X_train.shape, X_test.shape, y_train.shape, y_test.shape)

y_train = to_categorical(y_train, 3)
y_test = to_categorical(y_test, 3)

model = Sequential()
model.add(Conv2D(filters=32, kernel_size=(5, 5), activation='relu', input_shape=X_train.shape[1:]))
model.add(Conv2D(filters=32, kernel_size=(5, 5), activation='relu'))
model.add(MaxPool2D(pool_size=(2, 2)))
model.add(Dropout(rate=0.25))

model.add(Conv2D(filters=64, kernel_size=(3, 3), activation='relu'))
model.add(Conv2D(filters=64, kernel_size=(3, 3), activation='relu'))
model.add(MaxPool2D(pool_size=(2, 2)))
model.add(Dropout(rate=0.25))

model.add(Flatten())
model.add(Dense(256, activation='relu'))
model.add(Dropout(rate=0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(rate=0.5))
model.add(Dense(3, activation='softmax'))

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
print("model summary", model.summary())
epochs = 20

history = model.fit(X_train, y_train, batch_size=8, epochs=epochs, validation_data=(X_test, y_test))
model.save("/Users/KANAWADE AKSHAY/Desktop/project/pcm/models/public_model3.h5")
# accuracy
plt.figure(0)
plt.plot(history.history['accuracy'], label='training accuracy')
plt.plot(history.history['val_accuracy'], label='val accuracy')
plt.title('Accuracy')
plt.xlabel('epochs')
plt.ylabel('accuracy')
plt.legend()
plt.show()

# Loss
plt.plot(history.history['loss'], label='training loss')
plt.plot(history.history['val_loss'], label='val loss')
plt.title('Loss')
plt.xlabel('epochs')
plt.ylabel('loss')
plt.legend()
plt.show()
