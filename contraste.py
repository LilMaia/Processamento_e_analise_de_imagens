"""
Trabalho de Processamento e Análise de Imagens
Curso: Ciência da Computação - Campus Coração Eucarístico
Professor: Alexei Machado
Alunos:
Rafael Maia - 635921
Jonathan Tavares - 540504
Giulia Chiucchi - 662103
"""

# Imports
import numpy as np
import cv2

from imageUtils import atualizar_imagem
from PIL import Image

# Função que atualiza o contraste usando contraste por janelamento


def ajustar_contraste(min_value, max_value, image_label, image_info, result_label):
    # Verifica se a imagem original existe
    if image_info.img_original is not None:
        # Aplica o janelamento diretamente na imagem redimensionada
        img_janelado = np.clip(image_info.img_original, min_value, max_value)
        # Normaliza a imagem
        img_norm = cv2.normalize(
            img_janelado, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
        # Cria uma nova imagem a partir da matriz numpy com contraste ajustado
        img_new = Image.fromarray(img_norm)
        # Redimensiona a nova imagem e atualiza o rótulo da imagem
        img_resized = img_new.resize((400, 400), Image.Resampling.LANCZOS)
        # isso ta dando problema quando for ajustar o contraste dnv
        image_info.image_resized = img_resized
        atualizar_imagem(img_resized, image_label, image_info, result_label)
