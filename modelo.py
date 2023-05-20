import tensorflow
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D,  Dropout
from tensorflow.keras.applications import DenseNet121
from tensorflow.keras.models import Model

def densenet121_model():
    inputs = tensorflow.keras.Input(shape=(200, 200, 3))
    base_model = DenseNet121(weights='imagenet',
                          include_top=False,
                          input_tensor=inputs)
    
    for layer in base_model.layers:
        if not isinstance(layer, Dense):
            layer.trainable = False

    x = base_model(inputs)
    x = GlobalAveragePooling2D()(x)
    x = Dense(2048, activation='relu')(x)
    x = Dropout(0.5)(x)
    x = Dense(1024, activation='relu')(x)
    x = Dropout(0.5)(x)

    preds = Dense(4, activation='softmax')(x)
    model = Model(inputs=inputs, outputs=preds)
    #model.summary()
    print(F"Total de pesos : {Model.count_params(model)}")

    return model