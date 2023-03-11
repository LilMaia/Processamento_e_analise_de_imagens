"""
Trabalho de Processamento e Análise de Imagens
Curso: Ciência da Computação - Campus Coração Eucarístico
Professor: Alexei Machado
Alunos:
Rafael Maia - 635921
Jonathan Tavares - 540504
Giulia Chiucchi - 662103
"""

#Imports
import cv2

from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

# Função para abrir a imagem a partir de um arquivo
def abrir_imagem(image_label, image_info):
    # Abre uma janela para escolher o arquivo de imagem
    file_path = filedialog.askopenfilename(filetypes=[("PNG files", "*.png"), ("TIFF files", "*.tiff")])
    # Verifica se o arquivo foi escolhido
    if file_path:
        try:
            # Abre a imagem usando o modulo de imagem do OpenCV
            img = cv2.imread(file_path, cv2.IMREAD_COLOR)
            # Converte a imagem para o formato RGB
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            # Cria um objeto Image do PIL a partir da matriz numpy
            image = Image.fromarray(img)
            # Redimensiona e salva a imagem como variável global
            image_info.image_resized = image.resize((400, 400), Image.Resampling.LANCZOS)
            image_info.img_original = image_info.image_resized.copy()
            atualizar_imagem(image_info.image_resized, image_label, image_info)
        except Exception as e:
            # Mostra um erro se houver falha na hora de abrir a imagem
            messagebox.showerror("Error", "Failed to open image: {}".format(e))

# Função para atualizar o image label com uma imagem nova
def atualizar_imagem(image, image_label, image_info):
    # Salva a imagem original se ela estiver sendo exibida
    if image_info.img_original is None or image_info.img_original.size != image.size:
        image_info.img_original = image.copy()
    # Atualiza o image label com a nova imagem
    image_info.image_tk = ImageTk.PhotoImage(image)
    image_label.config(image=image_info.image_tk)