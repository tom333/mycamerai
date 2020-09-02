import logging

from kivymd.app import MDApp
from kivy.logger import Logger
from kivy.properties import ObjectProperty

from face_detector import FaceDetector
from screen_manager import AppScreenManager
from screens import Capture, Send

Logger.setLevel(logging.TRACE)


class PhotoApp(MDApp):
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
        self.theme_cls.theme_style = "Dark"

        return self.manager

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def envoyer_photo(self):
        Logger.debug("envoyer photo")
        self.manager.switch_to("Capture")


if __name__ == "__main__":
    PhotoApp().run()
