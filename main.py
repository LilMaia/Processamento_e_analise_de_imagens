# Importando os modulos necessários
import tkinter as tk
import cv2
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk, ImageOps
import numpy as np

# Iniciando as variáveis globais
zoom_level = 2
zoom_size = 300
zoom_width = 0
zoom_height = 0
zoom_max = 10
image_reduced = None

# Adicionando uma nova variável global para armazenar a imagem original
img_original = None

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
            global image_resized
            image_resized = image.resize((400, 400), Image.Resampling.LANCZOS)
            # Atualiza o image label com o tamanho redimensionado
            update_image(image_resized)
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
    global image, image_resized, image_tk, zoom_level
    # Restaura a imagem original e redefine o nível de zoom
    image = image_resized.copy()
    zoom_level = 0
    update_image(image)

# Função para dar zoom na imagem
def zoom_in():
    global zoom_level, image, image_resized, image_tk, zoom_width, zoom_height
    # Aumente o nível de zoom se ele ainda não estiver no máximo
    if zoom_level < zoom_max:
        zoom_level += 1
        if zoom_width > 0 and zoom_height > 0:
            zoomed_image = image_resized.resize((zoom_width, zoom_height), Image.Resampling.LANCZOS)
            x = max(0, image_label.winfo_rootx() - root.winfo_rootx() - zoom_size//2)
            y = max(0, image_label.winfo_rooty() - root.winfo_rooty() - zoom_size//2)
            cropped_image = zoomed_image.crop((x, y, x + zoom_size, y + zoom_size))
            # Atualize a variável global image com a imagem ampliada
            image = zoomed_image
            # Atualize o rótulo da imagem com a imagem ampliada
            image_tk = ImageTk.PhotoImage(cropped_image)
            image_label.config(image=image_tk)

# Função para diminuir o zoom na imagem
def zoom_out():
    global zoom_level, image, image_resized, image_tk, zoom_width, zoom_height, image_reduced
    # Verifique se o nível de zoom atual é maior que 0 antes de diminuir
    if zoom_level > 0:
        zoom_level -= 1
        if zoom_level == 0:
            image = image_resized.copy()
        else:
            if image_reduced is None or image_reduced.size != image.size:
                image_reduced = image.copy()
            image_reduced = image_reduced.resize((int(image.width * (1 - zoom_level * 0.1)), int(image.height * (1 - zoom_level * 0.1))), Image.Resampling.LANCZOS)
            image = image_reduced
        x = max(0, image_label.winfo_rootx() - root.winfo_rootx() - zoom_size//2)
        y = max(0, image_label.winfo_rooty() - root.winfo_rooty() - zoom_size//2)
        cropped_image = image.crop((x, y, x + zoom_size, y + zoom_size))
        # Atualize o rótulo da imagem com a imagem reduzida
        image_tk = ImageTk.PhotoImage(cropped_image)
        image_label.config(image=image_tk)
        
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

# Função que atualiza o contraste
def adjust_contrast(min_value, max_value):
    global img_original, image_label, image_tk
    # Calcula o nível de contraste
    level = (max_value - min_value) * 255 / 100
    # Verifica se a imagem original existe
    if img_original is not None:
        # Converte a imagem original para uma matriz numpy
        img_np = np.asarray(img_original)
        # Aplica o nível de contraste usando a função cv2.convertScaleAbs()
        img_contrast = cv2.convertScaleAbs(img_np, alpha=level/100)
        # Cria uma nova imagem a partir da matriz numpy com contraste ajustado
        img_new = Image.fromarray(img_contrast)
        # Redimensiona a nova imagem e atualiza o rótulo da imagem
        img_resized = img_new.resize((400, 400), Image.Resampling.LANCZOS)
        update_image(img_resized)

# Cria a janela principal e define o título
root = tk.Tk()
root.title("Image Viewer")

# Cria o rótulo da imagem e adiciona ele à janela principal
image_label = tk.Label(root)
image_label.bind("<Button-1>", update_zoomed_image)
image_label.pack()

# Cria o botão "Abrir" e adiciona ele à janela principal
open_button = tk.Button(root, text="Open", command=open_image)
open_button.pack()

# Cria o botão "Zoom In" e adiciona ele à janela principal
zoom_in_button = tk.Button(root, text="Zoom In", command=zoom_in)
zoom_in_button.pack()

# Cria o botão "Zoom Out" e adiciona ele à janela principal
zoom_out_button = tk.Button(root, text="Zoom Out", command=zoom_out)
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