import cv2

from mycamerai.face_detector import FaceDetector


def test_2oui_faces_on_image():
    fd = FaceDetector("../mycamerai")
    nb_faces = fd.detect_face_from_files("./tests/assets/father-and-daughter.jpg")
    assert len(nb_faces) == 2


def test_1_faces_on_image():
    fd = FaceDetector("../mycamerai")
    nb_faces = fd.detect_face_from_files("./tests/assets/baby.jpeg")
    assert len(nb_faces) == 1


def test_1_faces_on_image_bis():
    fd = FaceDetector("../mycamerai")
    nb_faces = fd.detect_face_from_files("./tests/assets/baby2.jpg")
    assert len(nb_faces) == 1


def test_15_faces_on_image():
    fd = FaceDetector("../mycamerai")
    filename = "./tests/assets/group.jpg"
    image = cv2.imread(filename)
    #cv2.imshow(image)
    nb_faces = fd.detect_face_from_files(filename)
    assert len(nb_faces) == 15
