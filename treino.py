import os
import tensorflow as tf
from armazenamento import salvar_população, carregar_população
import PIL
from modelo import criar_modelo
import shutil

def treino():
    
    #armazenando caminho dos diretorios
    diretorio_imagens = "../mamografias/"
    diretorio_treino = "../mamografias_treino/" 
    diretorio_teste = "../mamografias_teste/"
    
    #modelo
    modelo = None
    
    #nome_do_arquivo
    nome_do_arquivo = "pesos.h5"

    #caso já exista pesos treinados, carregamos eles
    try:
        # Tenta carregar os pesos de um arquivo
        pesos_da_população = carregar_população(nome_do_arquivo)
        print(f"Pesos carregados de {nome_do_arquivo}")
        modelo = criar_modelo(pesos_da_população)
    except FileNotFoundError:
        # Se o arquivo não existe
        print(f"Arquivo {nome_do_arquivo} não encontrado. Iniciando o modelo.")
        modelo = criar_modelo(pesos=None)

    # carregando as imagens de teste e suas labels
    arquivos = os.listdir(diretorio_teste) 
    for i, nome_arquivo in enumerate(arquivos, start=1):
        if i % 4 == 1 and nome_arquivo.endswith(".png"):
            caminho_origem = os.path.join(diretorio_imagens, nome_arquivo)
            caminho_destino = os.path.join(diretorio_teste, nome_arquivo)
            shutil.copy(caminho_origem, caminho_destino)
            
    dados_treino = tf.keras.preprocessing.image_dataset_from_directory(
        diretorio_treino,
        labels="inferred",
        label_mode="int",
        color_mode="rgb",
        batch_size=32,
        image_size=(28, 28),
        shuffle=True,
        seed=42
    )
    
    dados_teste = tf.keras.preprocessing.image_dataset_from_directory(
        diretorio_teste,
        labels="inferred",
        label_mode="int",
        color_mode="rgb",
        batch_size=32,
        image_size=(28, 28),
        shuffle=True,
        seed=42
    )
    
    #treinando o modelo
    modelo.fit(dados_treino, batch_size=128, epochs=5, verbose=1, validation_data=dados_teste)
    
    #salve os pesos da população
    salvar_população(modelo, nome_do_arquivo)
    
    # Avaliar o desempenho da rede neural
    loss, accuracy = modelo.evaluate(dados_teste)
    print("Loss:", loss)
    print("Accuracy:", accuracy)
