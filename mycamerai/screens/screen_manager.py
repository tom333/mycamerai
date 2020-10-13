from kivy import Logger
from kivy.app import App
from kivy.core.window import Window
from kivy.modules import inspector
from kivy.uix.screenmanager import Screen, ScreenManager

from screens.editor import Editor


class AppScreenManager(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.add_widget(Capture(name="Capture"))
        editor = Editor(name="Editor")
        inspector.create_inspector(Window, editor)
        self.add_widget(editor)

    back_screen_name = None

    def switch_to(self, name, **kwargs):
        Logger.debug("Asked to switch to %s " % name)
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
        Logger.debug("Closing settings")
        if self.manager.current == "Settings":
            self.manager.go_back()

    def switch_and_set_back(self, newcurrent):
        Logger.debug("Asked to switch and set back")
        self.back_screen_name = self.current
        self.switch_to(newcurrent)

    def go_back(self):
        if self.back_screen_name is not None:
            self.switch_to(self.back_screen_name)
            self.back_screen_name = None
