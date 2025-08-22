import os
import cv2
import numpy as np
from PIL import Image

def TrainImage(haarcasecade_path, trainimage_path, trainimagelabel_path, message, text_to_speech):
    try:
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        faces, Ids = getImagesAndLabels(trainimage_path)

        if not faces:
            text_to_speech("No images found for training.")
            message.configure(text="No images found for training.")
            return

        recognizer.train(faces, np.array(Ids))
        recognizer.save(trainimagelabel_path)

        res = "Images trained successfully."
        message.configure(text=res)
        text_to_speech(res)

    except Exception as e:
        print(f"Training error: {e}")
        text_to_speech("An error occurred during training.")

def getImagesAndLabels(path):
    faces = []
    Ids = []

    for root, dirs, files in os.walk(path):
        for file in files:
            if file.lower().endswith((".jpg", ".png")):
                try:
                    imagePath = os.path.join(root, file)
                    pilImage = Image.open(imagePath).convert("L")  # grayscale
                    imageNp = np.array(pilImage, "uint8")
                    Id = int(file.split("_")[1])  # assumes filename format: name_id_num.jpg
                    faces.append(imageNp)
                    Ids.append(Id)
                except Exception as e:
                    print(f"Error processing {file}: {e}")

    return faces, Ids
