"""
Trabalho de Processamento e Análise de Imagens
Curso: Ciência da Computação - Campus Coração Eucarístico
Professor: Alexei Machado
Alunos:
Rafael Maia - 635921
Giulia Chiucchi - 662103
"""

# imports
from PIL import Image, ImageOps
import os
import re
import numpy as np
import cv2
from sklearn.preprocessing import LabelBinarizer
from tensorflow.keras.preprocessing.image import img_to_array
from sklearn.model_selection import train_test_split

input_folder = "../mamografias/"
output_folder = "../mamografias_treino/"

# função para separar as imagens em treino e teste, sendo as imagens de teste 1/4 do total


def split_data(data, labels):
    train_indices = []
    test_indices = []
    for i in range(len(data)):
        if (i+1) % 4 == 0:
            test_indices.append(i)
        else:
            train_indices.append(i)

    xtrain = data[train_indices]
    xtest = data[test_indices]
    ytrain = labels[train_indices]
    ytest = labels[test_indices]

    return xtrain, xtest, ytrain, ytest


# função para pegar as imagens e os labels para treino
def pegar_imagens_e_labels(data, labels):
    imagePaths = sorted(os.listdir("../mamografias_treino/"))

    for imagePath in imagePaths:
        image = cv2.imread(os.path.join("../mamografias_treino/", imagePath))
        if image is None or image.size == 0:
            continue
        image = cv2.resize(image, (200, 200))
        image = img_to_array(image)
        data.append(image)

        label = imagePath[0]
        labels.append(label)

    data = np.array(data, dtype="float32") / 255.0
    labels = np.array(labels)
    mlb = LabelBinarizer()
    labels = mlb.fit_transform(labels)

    return data, labels


# função para gerar novas imagens a partir das imagens de treino
def generateTrainImages():
    for filename in os.listdir(input_folder):
        if os.path.isdir(os.path.join(input_folder, filename)):
            print("Gerando novas imagens...")
            for subfilename in os.listdir(os.path.join(input_folder, filename)):
                if subfilename.endswith(".png") or subfilename.endswith(".ttf"):
                    subfilename_number = re.search(r'\((\d+)\)', subfilename)
                    if subfilename:
                        subfilename_number = subfilename_number.group(1)
                        # pegar só as imagens reservadas para treino
                        if int(subfilename_number) % 4 != 0:
                            image_path = os.path.join(
                                input_folder, filename, subfilename)
                            with Image.open(image_path) as img:
                                # aqui iremos aplicar as funções para aumentar o dataset, a partir da geração de images espelhas e equalizadas, espelhadas e não equalizadas,
                                # não espelhadas e equalizadas e por fim não espelhadas e não equalizadas (original)
                                print("Gerando imagens a partir de: " + subfilename)
                                img_gray = ImageOps.grayscale(img)
                                # img equalizada
                                img_gray_eq = ImageOps.equalize(img_gray)
                                # img refletida
                                img_reflected = ImageOps.mirror(img)
                                # img equalizada refletida
                                img_reflected_eq = ImageOps.equalize(
                                    img_reflected)
                                # salvar novas imagens
                                img.save(os.path.join(
                                    output_folder, subfilename))
                                img_gray_eq.save(os.path.join(
                                    output_folder, subfilename.replace(".png", "_eq.png")))
                                img_reflected.save(os.path.join(
                                    output_folder, subfilename.replace(".png", "_ref.png")))
                                img_reflected_eq.save(os.path.join(
                                    output_folder, subfilename.replace(".png", "_ref_eq.png")))

            print("Imagens geradas com sucesso!")
