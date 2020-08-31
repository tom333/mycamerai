

__all__ = ('CameraOpenCV')

import time

import cv2
import kivy
import numpy as np
from kivy.app import App
from kivy.core.window import Window
from kivy.graphics import Color
from kivy.graphics import Rectangle
from kivy.logger import Logger
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.core.camera import CameraBase
from kivy.properties import ObservableList
from kivy.uix.camera import Camera
from kivy.uix.image import Image

from jnius import autoclass
from kivy_garden.xcamera import XCamera

Environment = autoclass('android.os.Environment')


class CameraOpenCV(XCamera):
    def on_camera_ready(self):
        Logger.debug("on_camera_ready %s " % str(self.center))
        if self._camera is not None:
            self._camera.bind(on_texture=self._on_texture)

    def _on_texture(self, instance):
        # Logger.debug("_on_texture %s " % instance)
        height, width = self.texture.height, self.texture.width
        img = np.frombuffer(self.texture.pixels, np.uint8)
        img = img.reshape(height, width, 4)
        Logger.debug("avant detection visage")
        detected_faces = App.get_running_app().face_detector.detect_faces(img)
        # Logger.debug(detected_faces)
        Logger.debug("test  %s %s vs %s  => %s, %s" % (width, height, self.size, self.center, self.pos))
        #self.canvas.before.clear()
        for (x, y, w, h) in detected_faces:
            Logger.debug("#######################################################################################")
            Logger.debug("visage détécté %s, %s => %s %s" % (x, y, w, h))
            Logger.debug("#######################################################################################")

            with self.canvas.after:
                new_y = y * self.size[1] / width
                new_x = x * self.size[0] / height
                Logger.debug("new pos %s : %s" % (new_y, new_x))
                Color(1, 0, 0, 0.5, mode="rgba")
                Rectangle(size=(300, 300), pos=(300,0)) # new_y, new_x

    def _setup(self):
        """
        Postpones some setup tasks that require self.ids dictionary.
        """
        self._remove_shoot_button()

        self.bind(on_camera_ready=self._on_camera_ready)
        # camera may still be ready before we bind the event
        if self._camera is not None:
            self._on_camera_ready(self)

    def _remove_shoot_button(self):
        shoot_button = self.children[0]
        self.remove_widget(shoot_button)

    def __init__(self, **kwargs):
        super(CameraOpenCV, self).__init__(**kwargs)
        Logger.debug("__init__")

    def picture_taken(self,  obj, filename):
        Logger.debug("#######################################################################################")
        Logger.debug("_on_picture_taken %s => %s" % (obj, filename))
        Logger.debug("#######################################################################################")
        # filename = "/storage/emulated/0/DCIM/IMG_{}.png".format(time.strftime("%Y%m%d_%H%M%S"))
        # self.camera.export_to_png(filename)
        # self.face_detector.detect_face(filename)
        # self.image.source = filename
        # # self.root.current = "Send"
        # self.manager.switch_to("Send")

    def update(self, dt):
        Logger.debug("test update ")
        # ret, frame = self.capture.read()
        # if ret:
        #     Logger.debug("camera update")
        #     # convert it to texture
        #     buf1 = cv2.flip(frame, 0)
        #     buf = buf1.tostring()
        #     image_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt="bgr")
        #     image_texture.blit_buffer(buf, colorfmt="bgr", bufferfmt="ubyte")
        #     # display image from the texture
        #     self.texture = image_texture
        #     # self.canvas.clear()
        #     # with self.canvas:
        #     #     Rectangle(pos=(10, 10), size=(20, 20))
