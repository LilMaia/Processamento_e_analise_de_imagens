import numpy as np

# função para salvar os pesos atuais
def salvar_população(pesos, nome_do_arquivo):
    with open(nome_do_arquivo, 'wb') as f:
        np.savez(nome_do_arquivo, *pesos)

# função para carregar os pesos de um arquivo
def carregar_população(nome_do_arquivo):
    with np.load(nome_do_arquivo) as data:
        pesos = [data[f] for f in data.files]
        pesos = np.vstack(pesos)
    return pesos
