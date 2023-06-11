"""
Trabalho de Processamento e Análise de Imagens
Curso: Ciência da Computação - Campus Coração Eucarístico
Professor: Alexei Machado
Alunos:
Rafael Maia - 635921
Giulia Chiucchi - 662103
"""

# imports
from tensorflow.keras.callbacks import ModelCheckpoint
from modelo import densenet121_model
from treino_utils import pegar_imagens_e_labels
from treino_utils import split_data
import time


def train_model():
    # inicia o tempo de execução
    start_time = time.time()

    # cria o modelo
    model = densenet121_model()

    # compila o modelo
    model.compile(optimizer='adam', loss='categorical_crossentropy',
                  metrics=['accuracy'])

    data = []
    labels = []

    # pega as imagens e os labels para treino
    data, labels = pegar_imagens_e_labels(data, labels)

    # divide os dados em treino e teste
    (xtrain, xtest, ytrain, ytest) = split_data(data, labels)

    print(xtrain.shape[0], 'train samples')
    print(xtest.shape[0], 'test samples')

    # salva o modelo com a melhor acurácia
    checkpoint = ModelCheckpoint('model.h5', verbose=1, save_best_only=True)

    # treina o modelo
    model.fit(xtrain, ytrain, batch_size=227,
              steps_per_epoch=xtrain.shape[0] // 227,
              epochs=50,
              verbose=1,
              callbacks=[checkpoint],
              validation_data=(xtest, ytest))

    # avalia o modelo
    score = model.evaluate(xtrain, ytrain, verbose=0)

    # imprime a acurácia, a perda do modelo e o tempo de execução
    print('Test loss:', score[0])
    print('Test accuracy:', score[1])
    end_time = time.time()
    execution_time = end_time - start_time
    print("Tempo de execução: ", execution_time, "segundos")
