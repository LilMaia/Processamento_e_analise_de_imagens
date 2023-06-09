"""
Trabalho de Processamento e Análise de Imagens
Curso: Ciência da Computação - Campus Coração Eucarístico
Professor: Alexei Machado
Alunos:
Rafael Maia - 635921
Giulia Chiucchi - 662103
"""
import cv2
import numpy as np
from keras.models import load_model
from modelo import densenet121_model
from tensorflow.keras.preprocessing.image import img_to_array
from treino_utils import pegar_imagens_e_labels
from treino_utils import split_data
import time
import tkinter as tk
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.preprocessing import LabelBinarizer

def classify_image():
    model = densenet121_model()

    #model = load_model('model.h5')

    model.load_weights('model.h5', by_name=True)

    data = []
    labels = []

    # pega as imagens e os labels para treino
    data, labels = pegar_imagens_e_labels(data, labels)

    # divide os dados em treino e teste
    (xtrain, xtest, ytrain, ytest) = split_data(data, labels)

    print(xtest.shape[0], 'test samples')

    # Início da contagem do tempo de execução
    start_time = time.time()

    # faz a predição da imagem
    predictions = model.predict(xtest)

    # Transforma as previsões em classes (I+II = 0, III+IV = 1)
    predictions_binary = np.where(predictions <= 2, 0, 1)

    # Reorganiza as classes do ytest para a mesma representação (I+II = 0, III+IV = 1)
    lb = LabelBinarizer()
    ytest_binary = lb.fit_transform(ytest)
    ytest_binary = np.where(ytest_binary <= 2, 0, 1)

    # Calcula as métricas
    accuracy = accuracy_score(ytest_binary, predictions_binary)
    precision = precision_score(ytest_binary, predictions_binary)
    recall = recall_score(ytest_binary, predictions_binary)
    f1 = f1_score(ytest_binary, predictions_binary)

    # Fim da contagem do tempo de execução
    end_time = time.time()

    # Calcula o tempo de execução em segundos
    execution_time = end_time - start_time

    print("Accuracy:", accuracy)
    print("Precision:", precision)
    print("Recall:", recall)
    print("F1 Score:", f1)
    print("Execution Time:", execution_time, "seconds")
