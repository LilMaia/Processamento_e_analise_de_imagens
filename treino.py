import os
import sklearn.metrics as metrics
from armazenamento import salvar_população, carregar_população
from PIL import Image
from modelo import criar_modelo
from numpy import asarray

def treino():
    
    #armazenando caminho dos diretorios
    diretorio_treino = "../mamografias_treino2/" 
    diretorio_teste = "../mamografias/"
    
    #armazenando as imagens de treino e teste e suas labels
    x_treino = []
    y_treino = []
    x_teste = []
    y_teste = []
    
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

    # carregando as imagens de treino e suas labels
    for nome_arquivo in os.listdir(diretorio_treino):
        if nome_arquivo.endswith(".png"):
            # Carregar imagem
            imagem = Image.open(os.path.join(diretorio_treino, nome_arquivo))
            imagem_array = asarray(imagem)  # Converter imagem para array NumPy
            x_treino.append(imagem_array)

            # Adicionar nome do arquivo a y_treino
            y_treino.append(nome_arquivo)

    # carregando as imagens de teste e suas labels
    arquivos = os.listdir(diretorio_teste) 
    for i, nome_arquivo in enumerate(arquivos, start=1):
        if i % 4 == 1 and nome_arquivo.endswith(".png"):
            # Carregar imagem
            imagem = Image.open(os.path.join(diretorio_teste, nome_arquivo))
            imagem_array = asarray(imagem)  # Converter imagem para array NumPy
            x_teste.append(imagem_array)

            # Adicionar nome do arquivo a y_teste
            y_teste.append(nome_arquivo)
  
    #treinando o modelo
    modelo.fit(x_treino, y_treino, batch_size=128, epochs=5, verbose=1, validation_data=(x_teste, y_teste))
    
    #salve os pesos da população
    salvar_população(modelo, nome_do_arquivo)
    
    #classifica as imagens
    classificacao = modelo.predict_classes(x_teste, verbose=1)
    
    #crie uma matriz de confusão
    matriz_de_confusao = metrics.confusion_matrix(y_teste, classificacao)
    
    print(matriz_de_confusao)
    
    
