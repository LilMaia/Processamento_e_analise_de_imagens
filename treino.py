import os
import sklearn.metrics as metrics
from armazenamento import salvar_população, carregar_população
from PIL import Image

def treino(modelo, nome_do_arquivo):
    
    diretorio_treino = "../mamografias_treino2/" 
    diretorio_teste = "../mamografias/"
    
    x_treino = []
    y_treino = []
    x_teste = []
    y_teste = []

    try:
        # Tenta carregar os pesos de um arquivo
        pesos_da_população = carregar_população(nome_do_arquivo)
        print(f"População carregada de {nome_do_arquivo}")
    except FileNotFoundError:
        # Se o arquivo não existe
        print(f"Arquivo {nome_do_arquivo} não encontrado. Iniciando o modelo.")
        

    for nome_arquivo in os.listdir(diretorio_treino):
        if nome_arquivo.endswith(".png"):
            # Carregar imagem
            imagem = Image.open(os.path.join(diretorio_treino, nome_arquivo))
            x_treino.append(imagem)

            # Adicionar nome do arquivo a y_treino
            y_treino.append(nome_arquivo)

    arquivos = os.listdir(diretorio_teste)

    for i, nome_arquivo in enumerate(arquivos, start=1):
        if i % 4 == 1 and nome_arquivo.endswith(".png"):
            # Carregar imagem
            imagem = Image.open(os.path.join(diretorio_teste, nome_arquivo))
            x_teste.append(imagem)

            # Adicionar nome do arquivo a yteste
            y_teste.append(nome_arquivo)
    
    #treinando o modelo
    modelo.fit(x_treino, y_treino, batch_size=128, epochs=5, verbose=1, validation_data=(x_teste, y_teste))
    
    #salve os pesos da população
    salvar_população(modelo, nome_do_arquivo)
    #classifique as imagens
    classificacao = modelo.predict_classes(x_teste, verbose=1)
    #crie uma matriz de confusão
    matriz_de_confusao = metrics.confusion_matrix(y_teste, classificacao)
    #faça o import do confusion_matrix
    
    
