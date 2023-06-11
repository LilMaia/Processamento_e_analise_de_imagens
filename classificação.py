"""
Trabalho de Processamento e Análise de Imagens
Curso: Ciência da Computação - Campus Coração Eucarístico
Professor: Alexei Machado
Alunos:
Rafael Maia - 635921
Giulia Chiucchi - 662103
"""

# imports
import cv2
import numpy as np
from keras.models import load_model
from modelo import densenet121_model
from tensorflow.keras.preprocessing.image import img_to_array
import time
import tkinter as tk

# função para classificar a imagem entre 4 classes diferentes
def classify_image(image_info, multi_classification, result_label):
    start_time = time.time()
    # cria uma lista com o nome das classes
    class_names = ['BIRADS I', 'BIRADS II', 'BIRADS III', 'BIRADS IV']

    model = densenet121_model()
    # Carregando o modelo treinado

    model.load_weights('model.h5', by_name=True)

    image = np.array(image_info.image_resized)
    image = cv2.resize(image, (200, 200))

    # checa se a imagem é em escala de cinza
    if len(image.shape) == 2:
        # converte a imagem para RGB
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)

    image = img_to_array(image)

    # reshape na imagem para a entrada da rede
    image = np.reshape(image, (-1, 200, 200, 3))

    # faz a predição da imagem
    prediction = model.predict(image)

    # transforma a predição em um array
    prediction = prediction.flatten()

    # encontra o índice da classe com maior probabilidade
    predicted_class = prediction.argmax(axis=-1)

    # calcula o tempo de execução
    end_time = time.time()
    execution_time = end_time - start_time
    print("Tempo de execução: ", execution_time, "segundos")
    multi_classification.execution_time = execution_time

    # encontra o nome da classe com maior probabilidade
    predicted_class_name = class_names[predicted_class]
    multi_classification.result = predicted_class_name
    result_label.config(
        text=f"Resultado da classificação : {multi_classification.result} \n Tempo de execução: {multi_classification.execution_time} segundos")
