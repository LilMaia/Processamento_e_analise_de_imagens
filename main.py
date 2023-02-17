# Importando os modulos necessários
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk, ImageOps

# Iniciando as váriaveis globais
zoom_level = 0
zoom_size = 400

# Função para abrir a imagem a partir de um arquivo
def open_image():
    # Abre uma janela para escolher o arquivo de imagem
    file_path = filedialog.askopenfilename(filetypes=[("PNG files", "*.png"), ("TIFF files", "*.tiff")])
    # Verifica se o arquivo foi escolhido
    if file_path:
        try:
            # Abre a imagem usando o modulo de imagem do PIL
            global image
            image = Image.open(file_path)
            # Redimensiona e salva a imagem como variável global
            global image_resized
            image_resized = image.resize((600, 600), Image.Resampling.LANCZOS)
            # Atualiza o image label com o tamanho redimensionado
            update_image(image_resized)
        except Exception as e:
            # Mostra um erro se houver falha na hora de abrir a imagem
            messagebox.showerror("Error", "Failed to open image: {}".format(e))

# Função para atualizar o image label com uma imagem nova
def update_image(image):
    # Salva a imagem como uma PhotoImage object e atualiza o image label
    global image_label, image_tk
    image_tk = ImageTk.PhotoImage(image)
    image_label.config(image=image_tk)

# Função para dar zoom na imagem
def zoom_in():
    # Aumente o nível de zoom e atualize a imagem ampliada
    global zoom_level
    zoom_level += 1
    update_zoomed_image()

# Função para diminuir o zoom na imagem
def zoom_out():
    # Diminua o nível de zoom e atualize a imagem ampliada
    global zoom_level
    zoom_level = max(0, zoom_level - 1)
    update_zoomed_image()

# Função para atualizar a imagem ampliada
def update_zoomed_image():
    # Calcule o tamanho e a posição da imagem ampliada
    global zoom_level, zoom_size, image, image_resized, image_label, image_tk
    zoomed_image = image.resize((int(image.width * (1 + zoom_level * 0.1)), int(image.height * (1 + zoom_level * 0.1))), Image.Resampling.LANCZOS)
    x = max(0, image_label.winfo_width()//2 - zoom_size//2)
    y = max(0, image_label.winfo_height()//2 - zoom_size//2)
    cropped_image = zoomed_image.crop((x, y, x + zoom_size, y + zoom_size))
    # Atualize o rótulo da imagem com a imagem ampliada
    image_tk = ImageTk.PhotoImage(cropped_image)
    image_label.config(image=image_tk)

# Função para ajustar o contraste da imagem
def adjust_contrast(min_value, max_value):   
    # Converta a imagem para tons de cinza se ainda não estiver
    global image, image_resized
    if image.mode not in ('L', 'P'):
        image = image.convert('L')
    # Ajusta o contraste usando o módulo PIL ImageOps e atualiza o rótulo da imagem
    image = ImageOps.autocontrast(image, cutoff=(min_value, max_value))
    update_image(image)

# Cria a janela principal e define o título
root = tk.Tk()
root.title("Image Viewer")

# Cria o rótulo da imagem e adiciona ele à janela principal
image_label = tk.Label(root)
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

# Cria o botão "Max Value" e adiciona ele à janela principal
max_value_slider = tk.Scale(root, from_=0, to=255, orient="horizontal", label="Max Value")
max_value_slider.pack()

# Cria o botão "Adjust Contrast" e adiciona ele à janela principal
adjust_button = tk.Button(root, text="Adjust Contrast", command=lambda: adjust_contrast(min_value_slider.get(), max_value_slider.get()))
adjust_button.pack()

#Inicia o lmainloop
root.mainloop()