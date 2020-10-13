import cv2
from kivy import Logger


class PeopleDetector:
    def __init__(self):
        self.hog = cv2.HOGDescriptor()
        self.hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    def detect_people_from_file(self, filename):
        image = cv2.imread(filename)
        return self.detect_people(image)

    def detect_people(self, image):
        found, _w = self.hog.detectMultiScale(image, winStride=(8, 8), padding=(32, 32), scale=1.05)
        height, width, channels = image.shape
        # Logger.debug("found %s : %s ; size=(%s, %s): %s" % (found, _w, width, height, channels))
        # for x, y, w, h in found:
        # the HOG detector returns slightly larger rectangles than the real objects.
        # so we slightly shrink the rectangles to get a nicer output.
        # Logger.debug("rectangle : pos=(%s, %s), size=(%s, %s)" % (x, y, x+w, y+h))
        # ratio = 0.15
        # pad_w, pad_h = int(0.15 * w), int(0.05 * h)
        # #cv2.rectangle(image, (x + pad_w, y + pad_h), (x + w - pad_w, y + h - pad_h), (0, 255, 0), 1)
        # cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 1)
        # cv2.imwrite('img.png', image)
        return found
