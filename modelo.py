import tensorflow
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D,  Dropout
from tensorflow.keras.applications import DenseNet121
from tensorflow.keras.models import Model

def densenet121_model():
    inputs = tensorflow.keras.Input(shape=(200, 200, 3))
    model_d = DenseNet121(weights=None,
                          include_top=False,
                          input_tensor=inputs)

    x = model_d(inputs)

    x = GlobalAveragePooling2D()(x)
    x = Dropout(0.5)(x)
    x = Dense(1024, activation='relu')(x)
    x = Dense(512, activation='relu')(x)
    x = Dropout(0.5)(x)

    preds = Dense(4, activation='softmax')(x)
    model = Model(inputs=inputs, outputs=preds)
    #model.summary()
    print(F"Total de pesos : {Model.count_params(model)}")

    return model