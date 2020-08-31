import os

import cv2
import numpy as np
from kivy import Logger


class FaceDetector:
    def __init__(self, path):
        self.path = path
        Logger.debug("FaceDetector.__init__()")
        # self.model = readNetFromCaffe(self.prototxt_path, self.model_path)
        self.detector = cv2.CascadeClassifier(os.path.join(self.path, "./app/data/haarcascade_frontalface_default.xml"))

    @property
    def prototxt_path(self):
        return os.path.join(self.path, "./app/data/deploy.prototxt")

    @property
    def model_path(self):
        return os.path.join(self.path, "./app/data/res10_300x300_ssd_iter_140000_fp16.caffemodel")

    def detect_face_from_files(self, filename):
        image = cv2.imread(filename)
        self.detect_faces(image)

    def detect_faces(self, image):
        # Logger.debug("#######################################################################################")
        # Logger.debug("detection de visage")
        # Logger.debug("#######################################################################################")
        # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = self.detector.detectMultiScale(image, scaleFactor=1.01, minNeighbors=3)

        # get width and height of the image
        # h, w = image.shape[:2]
        # # gaussian blur kernel size depends on width and height of original image
        # kernel_width = (w // 7) | 1
        # kernel_height = (h // 7) | 1
        # # preprocess the image: resize and performs mean subtraction
        # blob = cv2.dnn.blobFromImage(image, 1.0, (300, 300), (104.0, 177.0, 123.0))
        # # set the image into the input of the neural network
        # self.model.setInput(blob)
        # # perform inference and get the result
        # output = np.squeeze(self.model.forward())
        # Logger.debug("Inference")
        # cpt = 0
        # faces = []
        # for i in range(0, output.shape[0]):
        #
        #     confidence = output[i, 2]
        #     # get the confidence
        #     # if confidence is above 40%, then blur the bounding box (face)
        #     if confidence > 0.4:
        #         print("Floutage de visage")
        #         cpt += 1
        #         faces.append(i)
        # #         self.blur_image(h, i, image, kernel_height, kernel_width, output, w)
        # # if cpt > 0:
        # #     self.commentaire.text = "%s visage(s) détécté(s) et flouté(s)" % cpt
        # #     Logger.debug("avant ecriture fichier")
        # #     popup = Popup(title="Visages détéctés", content=Label(text="%s visage(s) détécté(s) et flouté(s)" % cpt), size_hint=(0.7, 0.2))
        # #     popup.open()
        # #     cv2.imwrite(filename, image)
        return faces

    def blur_image(self, h, i, image, kernel_height, kernel_width, output, w):
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
