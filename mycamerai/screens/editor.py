from kivy import Logger
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Rectangle
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivymd.uix.screen import MDScreen

from ia.people_detector import PeopleDetector


class Editor(MDScreen):
    source = StringProperty("/home/moi/Projets/transfo/PhotoPNord/tests/assets/basketball2.png")
    people = []

    def __init__(self, **kw):
        Builder.load_file("screens/editor.kv")
        super().__init__(**kw)

    def removing_people_enable(self):
        Logger.debug("removing_people_enable")
        pd = PeopleDetector()
        detected_people = pd.detect_people_from_file(self.source)
        with self.canvas:
            for (x, y, w, h) in detected_people:
                Logger.debug("personne détéctée pos=(%s, %s), size=(%s, %s) " % (x, y, w, h))
                # Logger.debug("widget size %s " % self.size)
                Color(1, 0, 0, 0.5, mode="rgba")
                # cf https://github.com/opencv/opencv/blob/master/samples/python/peopledetect.py#L27
                pad_w, pad_h = int(0.15 * w), int(0.05 * h)
                ratio = 1.25
                box_size = (int(w * ratio - pad_w), int(h * ratio - pad_h))
                box_pos = (int(x * ratio + pad_w), int((y - 75) * ratio + pad_h))
                Logger.debug("Box pos : %s, size: %s " % (str(box_pos), str(box_size)))
                r = Rectangle(size=box_size, position=box_pos)
                self.people.append(r)
