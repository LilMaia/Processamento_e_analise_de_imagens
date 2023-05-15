import tensorflow

import pandas as pd
import numpy as np
import os
import keras
import random
import cv2
import math
import seaborn as sns

from sklearn.metrics import confusion_matrix
from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train_test_split

import matplotlib.pyplot as plt

from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Convolution2D, BatchNormalization
from tensorflow.keras.layers import Flatten, MaxPooling2D, Dropout

from tensorflow.keras.applications import DenseNet121
from tensorflow.keras.applications.densenet import preprocess_input

from tensorflow.keras.preprocessing import image
from tensorflow.keras.preprocessing.image import ImageDataGenerator, img_to_array

from tensorflow.keras.models import Model

from tensorflow.keras.optimizers import Adam

from tensorflow.keras.callbacks import ModelCheckpoint, ReduceLROnPlateau


def densenet121_model():
    inputs = tensorflow.keras.Input(shape=(128, 128, 3))
    model_d = DenseNet121(weights=None,
                          include_top=False,
                          input_tensor=inputs)

    x = model_d(inputs)

    x = GlobalAveragePooling2D()(x)
    x = BatchNormalization()(x)
    x = Dropout(0.5)(x)
    x = Dense(512, activation='relu')(x)
    x = BatchNormalization()(x)
    x = Dropout(0.5)(x)

    preds = Dense(4, activation='softmax')(x)
    model = Model(inputs=inputs, outputs=preds)
    model.summary()

    return model


def train_model():
    model = densenet121_model()
    tensorflow.config.run_functions_eagerly(True)
    model.compile(optimizer='adam', loss='categorical_crossentropy',
                  metrics=['accuracy'], run_eagerly=True)

    data = []
    labels = []

    imagePaths = sorted(os.listdir("../mamografias_treino/"))

    for imagePath in imagePaths:
        image = cv2.imread(os.path.join("../mamografias_treino/", imagePath))
        if image is None or image.size == 0:
            continue
        image = cv2.resize(image, (128, 128))
        image = img_to_array(image)
        data.append(image)

        label = imagePath[0]
        labels.append(label)

    data = np.array(data, dtype="float32") / 255.0
    labels = np.array(labels)
    mlb = LabelBinarizer()
    labels = mlb.fit_transform(labels)

    (xtrain, xtest, ytrain, ytest) = train_test_split(
        data, labels, test_size=0.4, random_state=42)
    print(xtrain.shape, xtest.shape)

    anne = ReduceLROnPlateau(monitor='val_accuracy',
                             factor=0.5, patience=5, verbose=1, min_lr=1e-3)
    checkpoint = ModelCheckpoint('model.h5', verbose=1, save_best_only=True)

    """     datagen = ImageDataGenerator(
        zoom_range=0.2, horizontal_flip=True, shear_range=0.2)

    datagen.fit(xtrain) """

    # Fits-the-model
    history = model.fit(xtrain, ytrain, batch_size=128,
                        steps_per_epoch=xtrain.shape[0] // 128,
                        epochs=50,
                        verbose=2,
                        callbacks=[anne, checkpoint],
                        validation_data=(xtest, ytest))
