from kivy import Logger
from kivy.app import App
from kivy.properties import StringProperty

from screen_manager import SelfRegisterScreen


class Capture(SelfRegisterScreen):
    def display_settings(self):
        self.manager.display_settings()

    def callback(self):
        Logger.debug("callback")


class Editor(SelfRegisterScreen):
    source = StringProperty("")

    def go_back_to_capture_screen(self):
        App.get_running_app().manager.switch_to("Capture")

    def removing_people_enable(self, instance):
        Logger.debug("removing_people_enable %s " % instance)
