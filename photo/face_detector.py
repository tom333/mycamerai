import os

import cv2
import numpy as np
from kivy import Logger


class FaceDetector:
    def __init__(self, path):
        self.path = path
        Logger.debug("FaceDetector.__init__()")
        self.scale_factor = 4
        self.detector = cv2.CascadeClassifier(os.path.join(self.path, "./app/data/haarcascade_frontalface_default.xml"))

    def detect_face_from_files(self, filename):
        image = cv2.imread(filename)
        self.detect_faces(image)

    def detect_faces(self, image):
        # Logger.debug("#######################################################################################")
        # Logger.debug("detection de visage")
        # Logger.debug("#######################################################################################")
        gray = cv2.cvtColor(cv2.resize(image, (0, 0), fx=1.0 / self.scale_factor, fy=1.0 / self.scale_factor), cv2.COLOR_RGB2GRAY)
        faces = self.detector.detectMultiScale(gray, scaleFactor=1.01, minNeighbors=3, flags=cv2.CASCADE_SCALE_IMAGE) * self.scale_factor

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
