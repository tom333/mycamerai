import os

import cv2
from cv2.dnn import readNetFromCaffe
from kivy.uix.label import Label
from kivy.uix.popup import Popup
import numpy as np


class FaceDetector:
    MODULE_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
    model = None

    def __init__(self, path):
        self.path = path
        self.model = readNetFromCaffe(self.prototxt_path, self.model_path)

    @property
    def prototxt_path(self):
        return os.path.join(self.path, "./app/data/deploy.prototxt")

    @property
    def model_path(self):
        return os.path.join(self.path, "./app/data/res10_300x300_ssd_iter_140000_fp16.caffemodel")

    def detect_face(self, filename):
        print("#######################################################################################")
        print("detection de visage")
        print("#######################################################################################")

        print("analyse de l'image %s " % self.path)
        image = cv2.imread(filename)
        # get width and height of the image
        h, w = image.shape[:2]
        # gaussian blur kernel size depends on width and height of original image
        kernel_width = (w // 7) | 1
        kernel_height = (h // 7) | 1
        # preprocess the image: resize and performs mean subtraction
        blob = cv2.dnn.blobFromImage(image, 1.0, (300, 300), (104.0, 177.0, 123.0))
        # set the image into the input of the neural network
        self.model.setInput(blob)
        # perform inference and get the result
        output = np.squeeze(self.model.forward())
        print("Inference")
        cpt = 0
        for i in range(0, output.shape[0]):

            confidence = output[i, 2]
            # get the confidence
            # if confidence is above 40%, then blur the bounding box (face)
            if confidence > 0.4:
                print("Floutage de visage")
                cpt += 1
                # get the surrounding box cordinates and upscale them to original image
                box = output[i, 3:7] * np.array([w, h, w, h])
                # convert to integers
                start_x, start_y, end_x, end_y = box.astype(np.int)
                # get the face image
                face = image[start_y:end_y, start_x:end_x]
                # apply gaussian blur to this face
                face = cv2.GaussianBlur(face, (kernel_width, kernel_height), 0)
                # put the blurred face into the original image
                image[start_y:end_y, start_x:end_x] = face
        if cpt > 0:
            self.commentaire.text = "%s visage(s) détécté(s) et flouté(s)" % cpt
            print("avant ecriture fichier")
            popup = Popup(title="Visages détéctés", content=Label(text="%s visage(s) détécté(s) et flouté(s)" % cpt), size_hint=(0.7, 0.2))
            popup.open()
            cv2.imwrite(filename, image)
