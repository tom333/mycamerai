import os

from kivy import Logger
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.properties import BooleanProperty
from kivymd.uix.screen import MDScreen

import cv2
import numpy as np
from android.storage import primary_external_storage_path

from kivy.graphics import Color
from kivy.graphics import Rectangle


class Capture(MDScreen):
    event_callback = None
    directory = "/storage/emulated/0/DCIM/"

    def __init__(self, **kw):
        super().__init__(**kw)
        self.faces = []
        self.event_callback = Clock.schedule_interval(self.detect_face, 1 / 2.0)

    faces_detection_active = BooleanProperty(True)

    def switch_face_detection(self, *args):
        self.faces_detection_active = not self.faces_detection_active
        Logger.debug("switch_face_detection %s" % self.faces_detection_active)
        args[0].text_color = (1, 1, 0, 1) if self.faces_detection_active else (0, 0, 1, 1)

    def picture_taken(self, obj, filename):
        Logger.debug("picture_taken %s => %s" % (obj, filename))
        App.get_running_app().manager.switch_to("Editor")
        App.get_running_app().manager.current_screen.source = os.path.join("%s/DCIM/" % primary_external_storage_path(), filename)

    def detect_face(self, dt):
        height, width = self.ids.camera.texture.height, self.ids.camera.texture.width
        img = np.frombuffer(self.ids.camera.texture.pixels, np.uint8)
        img = img.reshape(height, width, 4)
        img = np.flipud(img)
        factor = Window.height / self.ids.camera.resolution[1]
        img = cv2.resize(img, None, fx=factor, fy=factor)
        if self.faces_detection_active:
            # Logger.debug("avant detection visage")
            detected_faces = App.get_running_app().face_detector.detect_faces(img)
            for c in self.faces:
                self.canvas.remove(c)
            self.faces = []
            for (x, y, w, h) in detected_faces:
                Logger.debug("visage détécté %s, %s => %s %s" % (x, y, w, h))
                with self.canvas:
                    Color(1, 0, 0, 0.8, mode="rgba")
                    # TODO: remove this magic numbers
                    r = Rectangle(size=(h, w), pos=(x + 200, y + 75))
                    self.faces.append(r)
