import numpy as np

from armazenamento import salvar_população, carregar_população

def treino(modelo, nome_do_arquivo):

    try:
        # Tenta carregar os pesos de um arquivo
        pesos_da_população = carregar_população(nome_do_arquivo)
        print(f"População carregada de {nome_do_arquivo}")
    except FileNotFoundError:
        # Se o arquivo não existe
        print(f"Arquivo {nome_do_arquivo} não encontrado. Iniciando o modelo.")

   
