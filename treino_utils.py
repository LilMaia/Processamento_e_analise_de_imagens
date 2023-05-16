from PIL import Image, ImageOps
import os
import re
import numpy as np
import cv2
from sklearn.preprocessing import LabelBinarizer
from tensorflow.keras.preprocessing.image import img_to_array

input_folder = "../mamografias/"
output_folder = "../mamografias_treino/"

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
