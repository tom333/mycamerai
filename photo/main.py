import json
import logging
import time

from kivy.app import App
from kivy.logger import Logger
from kivy.properties import ConfigParser, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.settings import Settings

from face_detector import FaceDetector

Logger.setLevel(logging.TRACE)


class DefaultScreen(Screen):
    layout = BoxLayout(orientation="vertical", padding=10)

    def finalize_widgets(self):
        # self.layout.add_widget(self.top_buttons)
        self.add_widget(self.layout)


class Capture(Screen):
    def display_settings(self):
        self.manager.display_settings()


class Send(DefaultScreen):
    pass


class AppScreenManager(ScreenManager):

    back_screen_name = None

    # def __init__(self):
    #

    def switch_to(self, name):
        self.current = name

    def display_settings(self):
        settings = App.get_running_app().get_settings_screen()
        manager = self.manager
        if not manager.has_screen("Settings"):
            s = Screen(name="Settings")
            s.add_widget(settings)
            manager.add_widget(s)
        manager.switch_and_set_back("Settings")

    def close_settings(self, *args):
        print("Closing settings")
        if self.manager.current == "Settings":
            self.manager.go_back()

    def switch_and_set_back(self, newcurrent):
        print("Asked to switch and set back")
        self.back_screen_name = self.current
        self.switch_to(newcurrent)

    def go_back(self):
        if self.back_screen_name is not None:
            self.switch_to(self.back_screen_name)
            self.back_screen_name = None


class PhotoApp(App):
    manager = ObjectProperty(None)

    config = None
    face_detector = None

    def build_config(self, config):
        config.setdefaults("Label", {"Content": "Default label text"})

    def build_settings(self, settings):
        jsondata = """[
            {
                "type": "title",
                "title": "Configuration"
            },
            {
                "type": "bool",
                "title": "Détécter et brouiller les visages automatiquement",
                "desc": "Activer la détéction de visages et le floutage automatique",
                "key": "detect_and_blur",
                "default": ":true"
            }
        ]
        """
        settings.add_json_panel("Configuration", self.config, data=jsondata)

    def build(self):
        self.manager = AppScreenManager()
        self.manager.add_widget(Capture(name="Capture"))
        self.manager.add_widget(Send(name="Send"))
        self.face_detector = FaceDetector(self.user_data_dir)

        return self.manager

    @property
    def camera(self):
        return self.root.screens[0].ids["camera"]

    @property
    def image(self):
        return self.root.screens[1].ids["image"]

    @property
    def commentaire(self):
        return self.root.screens[1].ids["commentaire"]

    def envoyer_photo(self):
        print("envoyer photo")
        self.manager.switch_to("Capture")

    def _on_picture_taken(self):
        print("#######################################################################################")
        print("_on_picture_taken")
        print("#######################################################################################")
        filename = "/storage/emulated/0/DCIM/IMG_{}.png".format(time.strftime("%Y%m%d_%H%M%S"))
        self.camera.export_to_png(filename)
        self.face_detector.detect_face(filename)
        self.image.source = filename
        # self.root.current = "Send"
        self.manager.switch_to("Send")


if __name__ == "__main__":
    PhotoApp().run()
