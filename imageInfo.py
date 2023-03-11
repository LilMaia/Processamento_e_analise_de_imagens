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

class ImageInfo:
    def __init__(self):
        self.image_tk : Image = None
        self.image_resized : Image = None
        self.img_original : Image  = None
        self.image : Image = None