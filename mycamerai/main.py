import logging

# from android.permissions import request_permissions, Permission
from kivy import platform
from kivymd.app import MDApp
from kivy.logger import Logger
from kivy.properties import ObjectProperty

from face_detector import FaceDetector
from screen_manager import AppScreenManager
from screens import Capture, Send

Logger.setLevel(logging.DEBUG)


class MyCamerAIApp(MDApp):

    manager = ObjectProperty(None)

    config = None
    face_detector = None

    def request_android_permissions(self):
        """
        Since API 23, Android requires permission to be requested at runtime.
        This function requests permission and handles the response via a
        callback.
        The request will produce a popup if permissions have not already been
        been granted, otherwise it will do nothing.
        """

    #
    #     def callback(permissions, results):
    #         """
    #         Defines the callback to be fired when runtime permission
    #         has been granted or denied. This is not strictly required,
    #         but added for the sake of completeness.
    #         """
    #         if all([res for res in results]):
    #             print("callback. All permissions granted.")
    #         else:
    #             print("callback. Some permissions refused.")
    #
    #     request_permissions([Permission.CAMERA, Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE], callback)

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
        if platform == "android":
            print("Android detected. Requesting permissions")
            self.request_android_permissions()
        self.manager = AppScreenManager()
        self.manager.add_widget(Capture(name="Capture"))
        self.manager.add_widget(Send(name="Send"))
        self.face_detector = FaceDetector(self.user_data_dir)
        self.theme_cls.theme_style = "Dark"

        return self.manager

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def envoyer_photo(self):
        Logger.debug("envoyer mycamerai")
        self.manager.switch_to("Capture")


if __name__ == "__main__":
    MyCamerAIApp().run()
