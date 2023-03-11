"""
Trabalho de Processamento e Análise de Imagens
Curso: Ciência da Computação - Campus Coração Eucarístico
Professor: Alexei Machado
Alunos:
Rafael Maia - 635921
Jonathan Tavares - 540504
Giulia Chiucchi - 662103
"""
"""
Arquivo: main.py
Data da última alteração: 23/02/2023
"""

#Imports
from PIL import Image
from imageUtils import atualizar_imagem
from contraste import ajustar_contraste

# Parâmetros
zoom_level = 2

# Função para resetar o zoom
def resetar_zoom(image_label, image_info):
    global zoom_level
    # Restaura a imagem original e redefine o nível de zoom
    image_info.image_resized = image_info.img_original.resize((400, 400), Image.LANCZOS)
    zoom_level = 0
    # Atualiza a imagem com o tamanho padrão
    atualizar_imagem(image_info.image_resized,image_label, image_info)

# Função para dar zoom na imagem
def aumentar_zoom(min_value, max_value, image_label, image_info):
    global zoom_level
    # Definindo o Zoom máximo
    zoom_max = 10
    # Calcula o novo nível de zoom
    new_zoom_level = zoom_level + 1
    # Verifica se o novo nível de zoom está dentro do limite máximo
    if new_zoom_level <= zoom_max:
        # Calcula o novo tamanho da imagem
        zoom_width = int(image_info.image_resized.width * (1 + new_zoom_level/10))
        zoom_height = int(image_info.image_resized.height * (1 + new_zoom_level/10))
        # Calcula a posição do canto superior esquerdo da área da imagem que será exibida (a imagem ampliada)
        x = int((zoom_width - image_info.image_resized.width) / 2)
        y = int((zoom_height - image_info.image_resized.height) / 2)
        # Calcula a posição do canto superior esquerdo da área da imagem original que será recortada para criar a imagem ampliada
        x_original = int(x / (1 + new_zoom_level/10))
        y_original = int(y / (1 + new_zoom_level/10))
        # Redimensiona a imagem original com o novo tamanho, recorta-a na área calculada acima e, em seguida, redimensiona-a novamente para o tamanho da exibição
        image_info.image = image_info.image_resized.resize((zoom_width, zoom_height), Image.LANCZOS).crop((x_original, y_original, x_original + image_info.image_resized.width, y_original + image_info.image_resized.height)).resize((400, 400), Image.LANCZOS)
        # Atualiza o nível de zoom e a imagem redimensionada
        zoom_level = new_zoom_level
        image_info.image_resized = image_info.image
        # Atualiza a imagem com o novo tamanho
        atualizar_imagem(image_info.image, image_label, image_info)
        if min_value or max_value:
            ajustar_contraste(min_value, max_value, image_label, image_info)