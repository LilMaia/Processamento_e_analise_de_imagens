import cv2
import numpy as np
from keras.models import load_model
from modelo import densenet121_model
from tensorflow.keras.preprocessing.image import img_to_array
import time
import tkinter as tk


def classify_image(image_info, multi_classification, result_label):
    start_time = time.time()
    # Create a list of class names
    class_names = ['BIRADS I', 'BIRADS II', 'BIRADS III', 'BIRADS IV']

    model = densenet121_model()
    # Carregando o modelo treinado
    model = load_model('model.h5')

    model.load_weights('model.h5', by_name=True)

    image = np.array(image_info.image_resized)
    image = cv2.resize(image, (200, 200))

    # Check if the image is grayscale
    if len(image.shape) == 2:
        # Convert grayscale image to RGB
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)

    image = img_to_array(image)

    # Reshape the image to have the correct shape
    image = np.reshape(image, (-1, 200, 200, 3))

    # Fazendo a previsão
    prediction = model.predict(image)

    # Flatten the prediction array
    prediction = prediction.flatten()

    # Get the predicted class label
    predicted_class = prediction.argmax(axis=-1)

    # Map the predicted class label to a class name
    predicted_class_name = class_names[predicted_class]
    multi_classification.result = predicted_class_name
    result_label.config(
        text=f"Resultado da classificação : {multi_classification.result}")

    end_time = time.time()
    execution_time = end_time - start_time
    print("Tempo de execução: ", execution_time, "segundos")
    multi_classification.execution_time = execution_time

    # Retornando a classe prevista
    return predicted_class_name
