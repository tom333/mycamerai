__all__ = "CameraOpenCV"


from kivy.logger import Logger
from kivy_garden.xcamera import XCamera
from android.storage import primary_external_storage_path


class CameraOpenCV(XCamera):
    directory = "%s/DCIM/" % primary_external_storage_path()

    def on_camera_ready(self):
        Logger.debug("on_camera_ready %s " % self.directory)
