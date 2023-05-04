from PIL import Image, ImageFilter, ImageDraw, ImageOps
from imageUtils import atualizar_imagem
from skimage.filters import threshold_otsu
from contraste import ajustar_contraste

import numpy as np

def segmentar_mama(imagem, image_label, min_value, max_value):
    # Converte a imagem para escala de cinza
    imagem_cinza = imagem.image_resized.convert('L')
    
    # Aplica limiarização de Otsu para separar o primeiro plano (mama) do fundo e anotações
    limiar = threshold_otsu(np.array(imagem_cinza))
    
    # Encontra os contornos da mama
    contornos = limiar.filter(ImageFilter.CONTOUR)
    
    # Cria uma nova imagem com a mesma dimensão da imagem original e preenche com valor preto
    mascara = Image.new('1', imagem.image_resized.size, color=0)
    
    # Desenha os contornos da mama na imagem de máscara
    mascara_draw = ImageDraw.Draw(mascara)
    mascara_draw.polygon(contornos.getdata(), outline=1, fill=1)
    
    # Aplica a máscara na imagem original para remover o fundo e anotações
    imagem_sem_fundo = ImageOps.fit(imagem.image_resized, mascara.size, centering=(0.5, 0.5))
    imagem_sem_fundo.putalpha(mascara)
    
    # Recorta a imagem para manter apenas a região da mama
    caixa = imagem_sem_fundo.getbbox()
    imagem_mama = imagem_sem_fundo.crop(caixa)
    imagem.image_resized = imagem_mama
    
    atualizar_imagem(imagem.image_resized, image_label, imagem)
    
    if min_value or max_value:
        ajustar_contraste(min_value, max_value, image_label, imagem)
