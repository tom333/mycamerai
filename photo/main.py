import json
import os
import traceback

import cv2
import time

from cv2.dnn import readNetFromCaffe
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import Clock, ConfigParser, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy.uix.settings import Settings
from kivy_garden.xcamera import XCamera
from kivy.uix.camera import Camera
import numpy as np

MODULE_DIRECTORY = os.path.dirname(os.path.realpath(__file__))

from kivy.logger import Logger
import logging
Logger.setLevel(logging.TRACE)


class Capture(Screen):
    pass


class Send(Screen):
    pass


class PhotoApp(App):
    def build(self):
        app = super().build()
        self.model = readNetFromCaffe(self.prototxt_path, self.model_path)
        self.config = ConfigParser()
        self.config.read('photo_config.ini')
        return app

    @property
    def prototxt_path(self):
        return os.path.join(self.user_data_dir, "./app/data/deploy.prototxt")

    @property
    def model_path(self):
        return os.path.join(self.user_data_dir, "./app/data/res10_300x300_ssd_iter_140000_fp16.caffemodel")

    model = None
    config = None

    @property
    def camera(self):
        return self.root.screens[0].ids['camera']

    @property
    def image(self):
        return self.root.screens[1].ids['image']

    @property
    def commentaire(self):
        return self.root.screens[1].ids['commentaire']

    def envoyer_photo(self):
        print("envoyer photo")
        self.root.current = "Capture"

    def _on_picture_taken(self):
        print('#######################################################################################')
        print("_on_picture_taken")
        print('#######################################################################################')
        filename = "/storage/emulated/0/DCIM/IMG_{}.png".format(time.strftime("%Y%m%d_%H%M%S"))
        self.camera.export_to_png(filename)
        self.detect_face(filename)
        self.image.source = filename
        self.root.current = "Send"

    def detect_face(self, filename):
        print('#######################################################################################')
        print("detection de visage")
        print('#######################################################################################')

        print("analyse de l'image %s " % self.user_data_dir)
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
                face = image[start_y: end_y, start_x: end_x]
                # apply gaussian blur to this face
                face = cv2.GaussianBlur(face, (kernel_width, kernel_height), 0)
                # put the blurred face into the original image
                image[start_y: end_y, start_x: end_x] = face
        if cpt > 0:
            self.commentaire.text = "%s visage(s) détécté(s) et flouté(s)" % cpt
            print("avant ecriture fichier")
            popup = Popup(title='Visages détéctés', content=Label(text="%s visage(s) détécté(s) et flouté(s)" % cpt), size_hint=(.7, .2))
            popup.open()
            cv2.imwrite(filename, image)

    def get_settings_screen(self):
        jsondata = json.dumps([
            {
                "type": "title",
                "title": "Configuration"
            },
            {
                "type": "bool",
                "title": "Détécter et brouiller les visages automatiquement",
                "desc" : "Activer la détéction de visages et le floutage automatique",
                "key": "detect_and_blur",
                "default": ":true"
            }

        ])
        s = Settings()
        s.add_json_panel("Configuration", self.config, jsondata)



if __name__ == '__main__':
    PhotoApp().run()
