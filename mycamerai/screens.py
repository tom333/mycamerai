from kivy import Logger
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.screen import MDScreen


# class DefaultScreen(MDScreen):
#     layout = MDBoxLayout(orientation="vertical", padding=10)

#     def finalize_widgets(self):
#         self.add_widget(self.layout)


class Capture(MDScreen):
    def display_settings(self):
        self.manager.display_settings()

    def callback(self):
        Logger.debug("callback")


class Editor(MDScreen):
    pass
