from tensorflow.keras.callbacks import ModelCheckpoint
from modelo import densenet121_model
from treino_utils import pegar_imagens_e_labels
from treino_utils import split_data
import time


def train_model():
    start_time = time.time()

    model = densenet121_model()

    model.compile(optimizer='adam', loss='categorical_crossentropy',
                  metrics=['accuracy'])

    data = []
    labels = []

    data, labels = pegar_imagens_e_labels(data, labels)

    (xtrain, xtest, ytrain, ytest) = split_data(data, labels)

    print(xtrain.shape[0], 'train samples')
    print(xtest.shape[0], 'test samples')

    checkpoint = ModelCheckpoint('model.h5', verbose=1, save_best_only=True)

    model.fit(xtrain, ytrain, batch_size=227,
              steps_per_epoch=xtrain.shape[0] // 227,
              epochs=50,
              verbose=1,
              callbacks=[checkpoint],
              validation_data=(xtest, ytest))

    score = model.evaluate(xtrain, ytrain, verbose=0)

    print('Test loss:', score[0])
    print('Test accuracy:', score[1])
    end_time = time.time()
    execution_time = end_time - start_time
    print("Tempo de execução: ", execution_time, "segundos")
