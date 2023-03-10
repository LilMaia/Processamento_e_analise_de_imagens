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
import tkinter as tk
from tkinter import filedialog, messagebox

import cv2
import numpy as np
from PIL import Image, ImageTk
from variaveis_globais import zoom_level, zoom_width, zoom_height, zoom_max, img_original

# Função para abrir a imagem a partir de um arquivo
def abrir_imagem(root):
    global image_resized, img_original
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
            image_resized = image.resize((400, 400), Image.Resampling.LANCZOS)
            img_original = image_resized.copy()
            # Atualiza o image label com o tamanho redimensionado
            abrir_janela(image_resized, root)
        except Exception as e:
            # Mostra um erro se houver falha na hora de abrir a imagem
            messagebox.showerror("Error", "Failed to open image: {}".format(e))

# Função para atualizar o image label com uma imagem nova
def atualizar_imagem(image):
    global image_label, image_tk, img_original
    # Salva a imagem original se ela estiver sendo exibida
    if img_original is None or img_original.size != image.size:
        img_original = image.copy()
    # Atualiza o image label com a nova imagem
    image_tk = ImageTk.PhotoImage(image)
    image_label.config(image=image_tk)

# Função para resetar o zoom
def resetar_zoom():
    global image_resized, zoom_level, img_original
    # Restaura a imagem original e redefine o nível de zoom
    image_resized = img_original.resize((400, 400), Image.LANCZOS)
    zoom_level = 0
    # Atualiza a imagem com o tamanho padrão
    atualizar_imagem(image_resized)

# Função que atualiza o contraste usando contraste por janelamento
def ajustar_contraste(min_value, max_value):
    global img_original, image_resized
    # Verifica se a imagem original existe
    if img_original is not None:
        # Converte a imagem original para uma matriz numpy
        img_np = np.asarray(image_resized)
        # Aplica o janelamento
        img_janelado = np.clip(img_np, min_value, max_value)
        # Normaliza a imagem
        img_norm = cv2.normalize(img_janelado, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
        # Cria uma nova imagem a partir da matriz numpy com contraste ajustado
        img_new = Image.fromarray(img_norm)
        # Redimensiona a nova imagem e atualiza o rótulo da imagem
        img_resized2 = img_new.resize((400, 400), Image.Resampling.LANCZOS)
        atualizar_imagem(img_resized2)

# Função para dar zoom na imagem
def aumentar_zoom(min_value, max_value):
    global image, image_resized, zoom_level, zoom_width, zoom_height, zoom_max
    # Calcula o novo nível de zoom
    new_zoom_level = zoom_level + 1
    # Verifica se o novo nível de zoom está dentro do limite máximo
    if new_zoom_level <= zoom_max:
        # Calcula o novo tamanho da imagem
        zoom_width = int(image_resized.width * (1 + new_zoom_level/10))
        zoom_height = int(image_resized.height * (1 + new_zoom_level/10))
        # Calcula a posição do canto superior esquerdo da área da imagem que será exibida (a imagem ampliada)
        x = int((zoom_width - image_resized.width) / 2)
        y = int((zoom_height - image_resized.height) / 2)
        # Calcula a posição do canto superior esquerdo da área da imagem original que será recortada para criar a imagem ampliada
        x_original = int(x / (1 + new_zoom_level/10))
        y_original = int(y / (1 + new_zoom_level/10))
        # Redimensiona a imagem original com o novo tamanho, recorta-a na área calculada acima e, em seguida, redimensiona-a novamente para o tamanho da exibição
        image = image_resized.resize((zoom_width, zoom_height), Image.LANCZOS).crop((x_original, y_original, x_original + image_resized.width, y_original + image_resized.height)).resize((400, 400), Image.LANCZOS)
        # Atualiza o nível de zoom e a imagem redimensionada
        zoom_level = new_zoom_level
        image_resized = image
        # Atualiza a imagem com o novo tamanho
        atualizar_imagem(image)
        if(min_value != 0 or max_value != 0) :
            ajustar_contraste(min_value, max_value)

# Cria o rótulo da imagem e adiciona ele à janela principal
def abrir_janela(image, root):
   global image_label
   new = tk.Toplevel(root)
   new.title("Nova Imagem")
   image_label = tk.Label(new)
   image_label.pack()
   # Salva a imagem original se ela estiver sendo exibida
   atualizar_imagem(image)
   new.geometry(str(image.width) + "x" + str(image.height))

def main():
    # Cria a janela principal e define o título
    root = tk.Tk()
    root.title("Trabalho de Processamento e Análise de Imagens - Ciência da Computação - 2023/1")
    window_width = 700
    window_height = 200

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x_cordinate = int((screen_width/2) - (window_width/2))
    y_cordinate = int((screen_height/2) - (window_height/2))

    root.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))
    root.resizable(False, False)

    # Criando a barra de menus
    menu_bar = tk.Menu(root)
    root.config(menu=menu_bar)

    # Adicionando o menu "File" à barra de menus
    file_menu = tk.Menu(menu_bar, tearoff=0)
    file_menu.add_command(label="Fechar", command=root.quit)
    menu_bar.add_cascade(label="Opções", menu=file_menu)

    # Cria o botão "Abrir" e adiciona ele à janela principal
    open_button = tk.Button(root, text="Abrir imagem", command=lambda: abrir_imagem(root))
    open_button.pack()

    # Cria o botão "Zoom In" e adiciona ele à janela principal
    zoom_in_button = tk.Button(root, text="Aumentar Zoom", command=lambda: aumentar_zoom(min_value_slider.get(), max_value_slider.get()))
    zoom_in_button.pack()

    # Cria o botão "Zoom Out" e adiciona ele à janela principal
    zoom_out_button = tk.Button(root, text="Retornar a proporção original", command=resetar_zoom)
    zoom_out_button.pack()
    
    # Cria o slider para ajustar o contraste mínimo
    min_value_slider = tk.Scale(root, from_=0, to=255, orient="horizontal", label="Diminuir Contraste", command= ajustar_contraste)
    min_value_slider.pack()
    min_value_slider.config(command=lambda val: ajustar_contraste(min_value_slider.get(), max_value_slider.get()))

    # Cria o slider para ajustar o contraste máximo
    max_value_slider = tk.Scale(root, from_=0, to=255, orient="horizontal", label="Aumentar Constraste", command= ajustar_contraste)
    max_value_slider.pack()
    max_value_slider.config(command=lambda val: ajustar_contraste(min_value_slider.get(), max_value_slider.get()))

    # Inicia o loop principal da janela
    root.mainloop()
    
if __name__ == '__main__':
    main()