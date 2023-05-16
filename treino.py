from sklearn.model_selection import train_test_split
from tensorflow.keras.callbacks import ModelCheckpoint
from modelo import densenet121_model
from treino_utils import pegar_imagens_e_labels

def train_model():
    model = densenet121_model()

    model.compile(optimizer='adam', loss='categorical_crossentropy',
                  metrics=['accuracy'])

    data = []
    labels = []
    
    data, labels = pegar_imagens_e_labels(data, labels)

    (xtrain, xtest, ytrain, ytest) = train_test_split(data, labels, test_size=0.4, random_state=42)
    print(xtrain.shape, xtest.shape)

    checkpoint = ModelCheckpoint('model.h5', verbose=1, save_best_only=True)

    model.fit(xtrain, ytrain, batch_size=128,
                        steps_per_epoch=xtrain.shape[0] // 128,
                        epochs=50,
                        verbose=2,
                        callbacks=[checkpoint],
                        validation_data=(xtest, ytest))

    score = model.evaluate(xtrain, ytrain, verbose=0)

    print('Test loss:', score[0])
    print('Test accuracy:', score[1])