from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen


class DefaultScreen(Screen):
    layout = BoxLayout(orientation="vertical", padding=10)

    def finalize_widgets(self):
        self.add_widget(self.layout)


class Capture(Screen):
    def display_settings(self):
        self.manager.display_settings()


class Send(DefaultScreen):
    pass
