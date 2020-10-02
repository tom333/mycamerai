import logging
import os

from kivy import platform
from kivy.logger import Logger
from kivy.properties import ObjectProperty
from kivymd.app import MDApp

from face_detector import FaceDetector
from screens.capture import Capture
from screens.editor import Editor
from screens.screen_manager import AppScreenManager

Logger.setLevel(logging.DEBUG)


class MyCamerAIApp(MDApp):

    manager = ObjectProperty(None)

    face_detector = None

    def request_android_permissions(self):
        """
        Since API 23, Android requires permission to be requested at runtime.
        This function requests permission and handles the response via a
        callback.
        The request will produce a popup if permissions have not already been
        been granted, otherwise it will do nothing.
        """

        def callback(permissions, results):
            """
            Defines the callback to be fired when runtime permission
            has been granted or denied. This is not strictly required,
            but added for the sake of completeness.
            """
            if all([res for res in results]):
                print("callback. All permissions granted.")
            else:
                print("callback. Some permissions refused.")

        from android.permissions import request_permissions, Permission

        request_permissions([Permission.CAMERA, Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE], callback)

    def build(self):
        if platform == "android":
            print("Android detected. Requesting permissions")
            self.request_android_permissions()
        self.manager = AppScreenManager()
        self.manager.add_widget(Capture(name="Capture"))
        self.manager.add_widget(Editor(name="Editor"))
        self.face_detector = FaceDetector(os.path.join(self.user_data_dir, "app"))
        self.theme_cls.theme_style = "Dark"

        return self.manager


if __name__ == "__main__":
    MyCamerAIApp().run()
    Capture(name="Capture")
