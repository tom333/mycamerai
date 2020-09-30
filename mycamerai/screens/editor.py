from kivy import Logger
from kivy.app import App
from kivy.properties import StringProperty
from kivymd.uix.screen import MDScreen


class Editor(MDScreen):
    source = StringProperty("")

    def go_back_to_capture_screen(self):
        App.get_running_app().manager.switch_to("Capture")

    def removing_people_enable(self, instance):
        Logger.debug("removing_people_enable %s " % instance)
