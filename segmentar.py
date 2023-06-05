"""
Trabalho de Processamento e Análise de Imagens
Curso: Ciência da Computação - Campus Coração Eucarístico
Professor: Alexei Machado
Alunos:
Rafael Maia - 635921
Giulia Chiucchi - 662103
"""

# imports
from PIL import Image
from imageUtils import atualizar_imagem
from skimage import filters, measure

import numpy as np


def segmentar_mama(imagem, image_label, result_label):
    # Converte a imagem para escala de cinza
    imagem_cinza = imagem.image_resized.convert('L')

    img = np.array(imagem_cinza)

    blurred = filters.gaussian(img, sigma=8)

    # limiariza a imagem
    thresh = filters.threshold_otsu(blurred)
    mask = blurred > thresh

    # Rotula as regiões da imagem
    labels = measure.label(mask)

    # Encontra a maior região (que deve ser a mama)
    regions = measure.regionprops(labels)
    areas = [r.area for r in regions]
    max_region = regions[np.argmax(areas)]

    # Cria uma máscara para a mama
    breast_mask = np.zeros_like(mask)
    breast_mask[max_region.coords[:, 0], max_region.coords[:, 1]] = 1

    # Aplica a máscara à imagem original para extrair a mama
    breast = Image.fromarray((img * breast_mask).astype(np.uint8))

    # Cria uma máscara para o fundo
    background_mask = np.ones_like(mask)
    background_mask[max_region.coords[:, 0], max_region.coords[:, 1]] = 0

    # Aplica a máscara à imagem original para extrair o fundo
    background = Image.fromarray((img * background_mask).astype(np.uint8))

    # Recorta a imagem para manter apenas a região da mama
    imagem.image_resized = breast
    imagem.img_original = imagem.image_resized

    # atualiza a imagem com a imagem segmentada
    atualizar_imagem(imagem.image_resized, image_label, imagem, result_label)
