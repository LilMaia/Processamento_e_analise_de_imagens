"""
Trabalho de Processamento e Análise de Imagens
Curso: Ciência da Computação - Campus Coração Eucarístico
Professor: Alexei Machado
Alunos:
Rafael Maia - 635921
Jonathan Tavares - 540504
Giulia Chiucchi - 662103
"""

# Imports
import tkinter as tk

from imageInfo import ImageInfo
from resultsInfo import BinaryClassification, MultiClassification
from imageUtils import abrir_imagem
from zoom import resetar_zoom, aumentar_zoom
from contraste import ajustar_contraste
from segmentar import segmentar_mama
from treino_utils import generateTrainImages
from treino import train_model
from classificação import classify_image


def interfaceMenu():
    # Cria o objeto que conterá as imagens
    image_info = ImageInfo()
    binary_classification = BinaryClassification()
    multi_classification = MultiClassification()

    # Cria a janela principal e define o título
    root = tk.Tk()
    root.title(
        "Trabalho de Processamento e Análise de Imagens - Ciência da Computação - 2023/1")

    # Cria a janela secundaria e define o título
    janela = tk.Toplevel(root)
    janela.title("Nova Imagem")
    image_label = tk.Label(janela)
    image_label.pack()

    result_label = tk.Label(
        janela, text="")
    result_label.pack()

    # Define as dimensões da janela e sua posição no centro da tela
    root.geometry(
        f"{600}x{300}+{int((root.winfo_screenwidth() / 2) - (600 / 2))}+{int((root.winfo_screenheight() / 2) - (300 / 2))}")
    root.resizable(False, False)

    # Criando a barra de menus
    menu_bar = tk.Menu(root)
    root.config(menu=menu_bar)

    # Adicionando o menu "File" à barra de menus
    file_menu = tk.Menu(menu_bar, tearoff=0)
    file_menu.add_command(label="Fechar", command=root.quit)
    menu_bar.add_cascade(label="Opções", menu=file_menu)

    # Cria o botão "Abrir" e adiciona ele à janela principal
    open_button = tk.Button(root, text="Abrir imagem",
                            command=lambda: abrir_imagem(image_label, image_info, result_label))
    open_button.pack()

    # Cria o botão "Zoom In" e adiciona ele à janela principal
    zoom_in_button = tk.Button(
        root, text="Aumentar Zoom", command=lambda: aumentar_zoom(image_label, image_info))
    zoom_in_button.pack()

    # Cria o botão "Zoom Out" e adiciona ele à janela principal
    zoom_out_button = tk.Button(root, text="Retornar a imagem original",
                                command=lambda: resetar_zoom(image_label, image_info))
    zoom_out_button.pack()

    # Cria o slider para ajustar o contraste mínimo
    min_value_slider = tk.Scale(root, from_=0, to=255, orient="horizontal", label="Aum. Contraste", command=lambda val: ajustar_contraste(
        min_value_slider.get(), max_value_slider.get(), image_label, image_info))
    min_value_slider.pack()

    # Cria o slider para ajustar o contraste máximo
    max_value_slider = tk.Scale(root, from_=0, to=255, orient="horizontal", label="Dim. Contraste", command=lambda val: ajustar_contraste(
        min_value_slider.get(), max_value_slider.get(), image_label, image_info))
    max_value_slider.pack()

    # Cria o botão "Segmentar" e adiciona ele à janela principal
    segmentar_button = tk.Button(
        root, text="Segmentar", command=lambda: segmentar_mama(image_info, image_label))
    segmentar_button.pack()

    # Cria o botão de treino e o adiciona à janela principal
    generate_images_button = tk.Button(
        root, text="Gerar imagens de treinio", command=lambda: generateTrainImages())
    generate_images_button.pack()

    instance_model_button = tk.Button(
        root, text="Treinar modelo", command=lambda: train_model())
    instance_model_button.pack()

    instance_model_button = tk.Button(
        root, text="Classificar imagem", command=lambda: classify_image(image_info, multi_classification, result_label))
    instance_model_button.pack()

    # Inicia o loop principal da janela
    root.mainloop()
