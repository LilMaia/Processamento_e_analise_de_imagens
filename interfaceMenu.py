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

from imageInfo import ImageInfo
from imageUtils import abrir_imagem
from zoom import resetar_zoom, aumentar_zoom
from contraste import ajustar_contraste

def interfaceMenu():
    #variaveis : 
    
    image_info = ImageInfo()
    
    # Cria a janela principal e define o título
    root = tk.Tk()
    root.title("Trabalho de Processamento e Análise de Imagens - Ciência da Computação - 2023/1")
    
    new = tk.Toplevel(root)
    new.title("Nova Imagem")
    image_label = tk.Label(new)
    image_label.pack()

    # Define as dimensões da janela e sua posição no centro da tela
    x_cordinate = int((root.winfo_screenwidth() / 2) - (700 / 2)) # window_width
    y_cordinate = int((root.winfo_screenheight() / 2) - (200 / 2)) # window_height
    root.geometry(f"{700}x{200}+{x_cordinate}+{y_cordinate}")
    root.resizable(False, False)

    # Criando a barra de menus
    menu_bar = tk.Menu(root)
    root.config(menu=menu_bar)

    # Adicionando o menu "File" à barra de menus
    file_menu = tk.Menu(menu_bar, tearoff=0)
    file_menu.add_command(label="Fechar", command=root.quit)
    menu_bar.add_cascade(label="Opções", menu=file_menu)

    # Cria o botão "Abrir" e adiciona ele à janela principal
    open_button = tk.Button(root, text="Abrir imagem", command=  lambda : abrir_imagem(image_label,image_info))
    open_button.pack()

    # Cria o botão "Zoom In" e adiciona ele à janela principal
    zoom_in_button = tk.Button(root, text="Aumentar Zoom", command= lambda: aumentar_zoom(min_value_slider.get(), max_value_slider.get(), image_label, image_info))
    zoom_in_button.pack()

    # Cria o botão "Zoom Out" e adiciona ele à janela principal
    zoom_out_button = tk.Button(root, text="Retornar a proporção original", command=lambda: resetar_zoom(image_label, image_info))
    zoom_out_button.pack()
    
    # Cria o slider para ajustar o contraste mínimo
    min_value_slider = tk.Scale(root, from_=0, to=255, orient="horizontal", label="Diminuir Contraste", command= ajustar_contraste)
    min_value_slider.pack()
    min_value_slider.config(command=lambda val: ajustar_contraste(min_value_slider.get(), max_value_slider.get(), image_label, image_info))

    # Cria o slider para ajustar o contraste máximo
    max_value_slider = tk.Scale(root, from_=0, to=255, orient="horizontal", label="Aumentar Constraste", command= ajustar_contraste)
    max_value_slider.pack()
    max_value_slider.config(command=lambda val: ajustar_contraste(min_value_slider.get(), max_value_slider.get(), image_label, image_info))

    # Inicia o loop principal da janela
    root.mainloop()