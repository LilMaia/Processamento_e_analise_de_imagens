import tensorflow as tf

def criar_modelo(pesos=None):
    
    # Cria um modelo sequencial utilizando camadas convolucionais e totalmente conectadas.
    modelo = tf.keras.applications.DenseNet121(
    include_top=True,
    weights=pesos,
    input_tensor=None,
    input_shape=None,
    pooling=None,
    classes=4,
    classifier_activation="relu",
    )
        
    # Retorna o modelo criado
    return modelo