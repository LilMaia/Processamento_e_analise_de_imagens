# Rafael Maia - 635921, Coração Eucarístico
# Jonathan Tavares - 540504, Coração Eucarístico
# Giulia Chiucchi - 662103, Coração Eucarístico

# Importando os modulos necessários
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import filedialog, messagebox

import cv2
import numpy as np
from PIL import Image, ImageOps, ImageTk

# Iniciando as variáveis globais
zoom_level = 2
zoom_size = 300
zoom_width = 0
zoom_height = 0
zoom_max = 10
image_reduced = None

# Adicionando uma nova variável global para armazenar a imagem original
img_original = None
min_value = None
max_value = None


min_value = None
max_value = None

# Função para abrir a imagem a partir de um arquivo
def open_image():
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
            global image
            image = Image.fromarray(img)
            # Redimensiona e salva a imagem como variável global
            global image_resized, img_original
            image_resized = image.resize((400, 400), Image.Resampling.LANCZOS)
            img_original = image_resized.copy()
            # Atualiza o image label com o tamanho redimensionado
            open_win(image_resized)
            """ update_image(image_resized) """
        except Exception as e:
            # Mostra um erro se houver falha na hora de abrir a imagem
            messagebox.showerror("Error", "Failed to open image: {}".format(e))

# Função para atualizar o image label com uma imagem nova
def update_image(image):
    global image_label, image_tk, img_original
    # Salva a imagem original se ela estiver sendo exibida
    if img_original is None or img_original.size != image.size:
        img_original = image.copy()
    # Atualiza o image label com a nova imagem
    image_tk = ImageTk.PhotoImage(image)
    image_label.config(image=image_tk)

# Função para resetar o zoom
def reset_zoom():
    global image, image_resized, image_tk, zoom_level, img_original
    # Restaura a imagem original e redefine o nível de zoom
    image_resized = img_original.resize((400, 400), Image.LANCZOS)
    zoom_level = 0
    # Atualiza a imagem com o tamanho padrão
    update_image(image_resized)

def adjust_contrast(min_value, max_value):
    global img_original, image_label, image_tk, image_resized
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
        update_image(img_resized2)


# Função que atualiza o contraste usando contraste por janelamento
def adjust_contrast(min_value, max_value):
    global img_original, image_label, image_tk, image_resized
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
        update_image(img_resized2)


# Função para dar zoom na imagem
def zoom_in():
    global image, image_resized, zoom_level, zoom_width, zoom_height, zoom_max, img_original, min_value, max_value
    global image, image_resized, zoom_level, zoom_width, zoom_height, zoom_max, img_original, min_value, max_value
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
        image = image_resized.resize((zoom_width, zoom_height), Image.LANCZOS).crop((x_original, y_original, x_original + image_resized.width, y_original + image_resized.height)).resize((400, 400), Image.LANCZOS)
        # Atualiza o nível de zoom e a imagem redimensionada
        zoom_level = new_zoom_level
        image_resized = image
        # Atualiza a imagem com o novo tamanho
        update_image(image)

   
        
# Atualiza a imagem com zoom
def update_zoomed_image(event=None):
    global zoom_level, zoom_size, image, image_label, image_tk, zoom_width, zoom_height
    if event is not None and event.widget is image_label:
        # Calcule o tamanho e a posição da imagem ampliada
        zoom_width = int(image.width * (1 + zoom_level * 0.1))
        zoom_height = int(image.height * (1 + zoom_level * 0.1))
        zoomed_image = image.resize((zoom_width, zoom_height), Image.Resampling.LANCZOS)
        x = max(0, event.x - zoom_size//2)
        y = max(0, event.y - zoom_size//2)
        cropped_image = zoomed_image.crop((x, y, x + zoom_size, y + zoom_size))
        # Atualize a variável global image com a imagem ampliada
        image = zoomed_image
        # Atualize o rótulo da imagem com a imagem ampliada
        image_tk = ImageTk.PhotoImage(cropped_image)
        image_label.config(image=image_tk)

# Função que atualiza o contraste usando contraste por janelamento


# Cria a janela principal e define o título
root = tk.Tk()
root.title("Image Viewer")
root.geometry("400x400")

# Criando a barra de menus
menu_bar = tk.Menu(root)

# Setando o menu da janela principal
root.config(menu=menu_bar)

# Cria o rótulo da imagem e adiciona ele à janela principal
def open_win(image):
   global image_label, image_tk, img_original
    
   new = tk.Toplevel(root)
   new = tk.Toplevel(root)
   new.title("New Window")
   image_label = tk.Label(new)
   image_label.pack()
   # Salva a imagem original se ela estiver sendo exibida
   if img_original is None or img_original.size != image.size:
      img_original = image.copy()
   # Atualiza o image label com a nova imagem
   image_tk = ImageTk.PhotoImage(image)
   image_label.config(image=image_tk)
   new.geometry("400x400")
   
# Adicionando o menu "File" à barra de menus
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Exit", command=root.quit)
menu_bar.add_cascade(label="File", menu=file_menu)


# Cria o botão "Abrir" e adiciona ele à janela principal
open_button = tk.Button(root, text="Open", command=open_image)
open_button.pack()

# Cria o botão "Zoom In" e adiciona ele à janela principal
zoom_in_button = tk.Button(root, text="Zoom In", command=zoom_in)
zoom_in_button.pack()

# Cria o botão "Reset Zoom" e adiciona ele à janela principal
zoom_out_button = tk.Button(root, text="Reset Zoom", command=reset_zoom)
zoom_out_button.pack()

# Cria o botão "Min Value" e adiciona ele à janela principal
min_value_slider = tk.Scale(root, from_=0, to=255, orient="horizontal", label="Min Value")
min_value_slider.pack()
min_value_slider.config(command=lambda val: adjust_contrast(min_value_slider.get(), max_value_slider.get()))

# Cria o botão "Max Value" e adiciona ele à janela principal
max_value_slider = tk.Scale(root, from_=0, to=255, orient="horizontal", label="Max Value")
max_value_slider.pack()
max_value_slider.config(command=lambda val: adjust_contrast(min_value_slider.get(), max_value_slider.get()))

#Inicia o lmainloop
root.mainloop()