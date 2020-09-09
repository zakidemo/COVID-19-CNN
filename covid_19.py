# -*- coding: utf-8 -*-
"""COVID-19.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1_7z84JlgPjMZEV-2mFkPO4GyC-b-LGUU
"""

# Commented out IPython magic to ensure Python compatibility.
# install tensorflow version 2
# %tensorflow_version 2.x
import tensorflow as tf

# Upload google drive in our colab
from google.colab import drive
drive.mount('/content/drive')

# Improting Libraries
import tensorflow.keras
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense, Activation, Flatten, Conv2D, MaxPool2D , Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.losses import binary_crossentropy
from tensorflow.keras import metrics
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report, confusion_matrix, plot_confusion_matrix, ConfusionMatrixDisplay
import numpy as np

# Create Path fro Both (Train/Test)
train_loc = '/content/drive/My Drive/our_DATA/train/'
test_loc = '/content/drive/My Drive/our_DATA/val/'

# resize images & do DA 
trdata = ImageDataGenerator(rescale = 1./255,
                            shear_range = 0.2,
                            zoom_range = 0.2,
                            horizontal_flip =True,
                            )

traindata = trdata.flow_from_directory( directory = train_loc, target_size = (224, 224))

tsdata = ImageDataGenerator(rescale = 1./255,
                            shear_range = 0.2,
                            zoom_range = 0.2,
                            horizontal_flip = True,
                            )

testndata = tsdata.flow_from_directory( directory = test_loc, target_size = (224, 224))

traindata.class_indices

# define input
input_shape = (224,224,3)

# Create the network

# Input Layer
img_input = Input(shape = input_shape, name = 'img_input')

# Build the model

x = Conv2D(32, (3,3) , padding = 'same', activation='relu', name ='layer_1') (img_input)
x = Conv2D(64, (3,3) , padding = 'same', activation='relu', name ='layer_2') (x)
x = MaxPool2D((2,2), strides=(2,2), name ='layer_3') (x)
x =Dropout(0.25)(x)

x = Conv2D(64, (3,3) , padding = 'same', activation='relu', name ='layer_4') (x)
x = MaxPool2D((2,2), strides=(2,2), name ='layer_5') (x)
x =Dropout(0.25)(x)

x = Conv2D(128, (3,3) , padding = 'same', activation='relu', name ='layer_6') (x)
x = MaxPool2D((2,2), strides=(2,2), name ='layer_7') (x)
x =Dropout(0.25)(x)

x =Flatten(name='layer_8')(x)
x = Dense(64, name = 'layer_9')(x)
x =Dropout(0.5)(x)
x =Dense(2, activation='sigmoid', name ='predections')(x)

# generate the model
model = Model(inputs = img_input, outputs  =x, name = 'CNN_COVID_19' )

# pint network structure
model.summary()

# Cmpiling the model
model.compile(optimizer = 'adam', loss = binary_crossentropy , metrics=['accuracy'])

# Start trian/Test
batch_size = 32
hist = model.fit(traindata, 
                 steps_per_epoch = traindata.samples//batch_size,
                 validation_data = testndata,
                 validation_steps = testndata.samples//batch_size,
                 epochs = 10
                 )

plt.plot(hist.history['loss'], label = 'train')
plt.plot(hist.history['val_loss'], label= 'val')
plt.title('CNN_COVID_19 : Loss & Valdation Loss')
plt.legend()
plt.show()

plt.plot(hist.history['accuracy'], label = 'train')
plt.plot(hist.history['val_accuracy'], label= 'val')
plt.title('CNN_COVID_19 : Accuracy & Valdation Loss')
plt.legend()
plt.show()

# Confusion Matrix & Precision & recall F1-score

target_names = ['COVID+','COVID-']
labels_names = [0,1]

Y_pred = model.predict_generator(testndata)
y_pred = np.argmax(Y_pred, axis = 1)
cm = confusion_matrix(testndata.classes, y_pred, labels = labels_names)

print('Confusion Matrix')
print(confusion_matrix(testndata.classes, y_pred))

print('Classification_report')
print(classification_report(testndata.classes, y_pred, target_names = target_names ))

disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels = target_names)
disp = disp.plot(cmap = plt.cm.Blues, values_format = 'g')

plt.show()