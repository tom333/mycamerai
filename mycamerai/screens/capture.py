import os

from kivy import Logger
from kivy.app import App
from kivy.properties import BooleanProperty
from kivymd.uix.screen import MDScreen


class Capture(MDScreen):

    faces_detection_active = BooleanProperty(True)

    def switch_face_detection(self, *args):
        self.faces_detection_active = not self.faces_detection_active
        Logger.debug("switch_face_detection %s" % self.faces_detection_active)
        args[0].text_color = (1, 1, 0, 1) if self.faces_detection_active else (0, 0, 1, 1)

    def picture_taken(self, obj, filename):
        Logger.debug("_on_picture_taken %s => %s" % (obj, filename))
        App.get_running_app().manager.switch_to("Editor")
        App.get_running_app().manager.current_screen.source = os.path.join(self.directory, filename)
