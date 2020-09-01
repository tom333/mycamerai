import logging

from kivy.app import App
from kivy.core.window import Window
from kivy.logger import Logger
from kivy.properties import ObjectProperty

from face_detector import FaceDetector
from screen_manager import AppScreenManager
from screens import Capture, Send

Logger.setLevel(logging.TRACE)


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
        Window.bind(on_rotate=self._on_flip_screen)

        return self.manager

    def _on_flip_screen(self, *args):
        Logger.debug("flipping %s " % list(args))

    def on_start(self):
        pass

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

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
        Logger.debug("envoyer photo")
        self.manager.switch_to("Capture")


if __name__ == "__main__":
    PhotoApp().run()
