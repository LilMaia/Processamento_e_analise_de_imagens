from PIL import Image, ImageFilter, ImageDraw, ImageOps
from imageUtils import atualizar_imagem
from skimage import filters, measure
from contraste import ajustar_contraste

import numpy as np

def segmentar_mama(imagem, image_label):
    # Converte a imagem para escala de cinza
    imagem_cinza = imagem.image_resized.convert('L')

    img = np.array(imagem_cinza)

    blurred = filters.gaussian(img, sigma=2)

    # limiarizou a imagem
    thresh = filters.threshold_otsu(blurred)
    mask = blurred > thresh
    
    # Label the regions in the mask
    labels = measure.label(mask)

    # Find the largest region, which should be the breast
    regions = measure.regionprops(labels)
    areas = [r.area for r in regions]
    max_region = regions[np.argmax(areas)]

    # Create a new mask with just the breast region
    breast_mask = np.zeros_like(mask)
    breast_mask[max_region.coords[:,0], max_region.coords[:,1]] = 1

    # Apply the mask to the original image to extract the breast region
    breast = Image.fromarray((img * breast_mask).astype(np.uint8))
    
    # Create a mask for the background
    background_mask = np.ones_like(mask)
    background_mask[max_region.coords[:,0], max_region.coords[:,1]] = 0

    # Apply the mask to the original image to extract the background
    background = Image.fromarray((img * background_mask).astype(np.uint8))

    # Recorta a imagem para manter apenas a região da mama
    imagem.image_resized = breast
    
    atualizar_imagem(imagem.image_resized, image_label, imagem)
    
    
