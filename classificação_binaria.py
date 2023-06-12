"""
Trabalho de Processamento e Análise de Imagens
Curso: Ciência da Computação - Campus Coração Eucarístico
Professor: Alexei Machado
Alunos:
Rafael Maia - 635921
Giulia Chiucchi - 662103
"""
import numpy as np
from keras.models import load_model
from modelo import densenet121_model
from treino_utils import pegar_imagens_e_labels
from treino_utils import split_data
import time
import tkinter as tk
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import matplotlib.pyplot as plt

def multi_classify_image():
    model = densenet121_model()

    #model = load_model('model.h5')

    model.load_weights('model.h5', by_name=True)

    data = []
    labels = []

    # pega as imagens e os labels para treino
    data, labels = pegar_imagens_e_labels(data, labels)

    # divide os dados em treino e teste
    (xtrain, xtest, ytrain, ytest) = split_data(data, labels)
    
    print(xtrain.shape[0], 'treino samples')
    print(xtest.shape[0], 'test samples')

    # Início da contagem do tempo de execução
    start_time = time.time()

    # faz a predição da imagem
    predictions = model.predict(xtest)

    # Transforma as previsões em classes (I+II = 0, III+IV = 1)
    predictions_binary = np.where(predictions <= 2, 0, 1)

    # Reorganiza as classes do ytest para a mesma representação (I+II = 0, III+IV = 1)
    ytest_binary = np.where(ytest <= 2, 0, 1)

    # Calcula as métricas
    accuracy_binary = accuracy_score(ytest_binary, predictions_binary)
    precision = precision_score(ytest_binary, predictions_binary, average='weighted', zero_division=1)
    recall = recall_score(ytest_binary, predictions_binary, average='weighted', zero_division=1)
    f1 = f1_score(ytest_binary, predictions_binary, average='weighted', zero_division=1)

    # Fim da contagem do tempo de execução
    end_time = time.time()

    # Calcula o tempo de execução em segundos
    execution_time_binary = end_time - start_time

    print("Accuracy:", accuracy_binary)
    print("Precision:", precision)
    print("Recall:", recall)
    print("F1 Score:", f1)
    print("Execution Time:", execution_time_binary, "seconds")
    
     # Início da contagem do tempo de execução
    start_time = time.time()

    # faz a predição da imagem
    predictions = model.predict(xtest)
    predictions_classes = np.argmax(predictions, axis=1)
    ytest_classes = np.argmax(ytest, axis=1)
    
    # Calcula a matriz de confusão
    confusion_mat = confusion_matrix(ytest_classes, predictions_classes)
    accuracy = np.sum(np.diag(confusion_mat)) / 1256
    sensitivity_mean = np.mean(np.diag(confusion_mat) / np.sum(confusion_mat, axis=1))
    specificity_mean = 1 - np.sum(confusion_mat - np.diag(np.diag(confusion_mat))) / 3768
    # Fim da contagem do tempo de execução
    end_time = time.time()
    # Calcula o tempo de execução em segundos
    execution_time = end_time - start_time
    print("Execution Time:", execution_time, "seconds")
    
    # Criação da tela
    fig, axes = plt.subplots(2, 2, figsize=(10, 8))

    # Plot da matriz de confusão para a classificação de 4 classes
    im1 = axes[0, 1].imshow(confusion_mat, interpolation='nearest', cmap=plt.cm.Blues)
    axes[0, 1].set_title('4-Class Confusion Matrix')
    axes[0, 1].set_xlabel('Predicted Class')
    axes[0, 1].set_ylabel('True Class')
    axes[0, 1].set_xticks(np.arange(4))
    axes[0, 1].set_xticklabels(['I', 'II', 'III', 'IV'])
    axes[0, 1].set_yticks(np.arange(4))
    axes[0, 1].set_yticklabels(['I', 'II', 'III', 'IV'])
    plt.colorbar(im1, ax=axes[0, 1])

    # Exibição das métricas da classificação binária
    axes[1, 0].axis('off')
    axes[1, 0].text(0, 0.8, f"Accuracy Binary: {accuracy_binary}", fontsize=12)
    axes[1, 0].text(0, 0.6, f"Precision: {precision}", fontsize=12)
    axes[1, 0].text(0, 0.4, f"Recall: {recall}", fontsize=12)
    axes[1, 0].text(0, 0.2, f"F1 Score: {f1}", fontsize=12)
    axes[1, 0].text(0, 0, f"Execution Time: {execution_time_binary} seconds", fontsize=12)

    # Exibição das métricas da classificação de 4 classes
    axes[1, 1].axis('off')
    axes[1, 1].text(0, 0.8, f"Accuracy 4-Class: {accuracy}", fontsize=12)
    axes[1, 1].text(0, 0.6, f"Sensitivity (Mean): {np.mean(sensitivity_mean)}", fontsize=12)
    axes[1, 1].text(0, 0.4, f"Specificity (Mean): {specificity_mean}", fontsize=12)
    axes[1, 1].text(0, 0, f"Execution Time: {execution_time} seconds", fontsize=12)

    plt.tight_layout()
    plt.show()