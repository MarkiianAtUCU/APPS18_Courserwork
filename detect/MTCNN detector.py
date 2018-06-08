from mtcnn.mtcnn import MTCNN
import cv2
import os


detector = MTCNN()
cap = cv2.VideoCapture(0)


def find_face(img):
    """
    (cv2.Img) -> list

    Find faces on photo and returns face coords
    """
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = detector.detect_faces(img)
    res = []
    for x in faces:
        x, y, w, h = x["box"]

        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

        res.append([(x, y), (x+w, y+h), (w, h)])

    cv2.imshow('img', img)

    return res


def write_info(file, name, info):
    """
    (str, str, list) -> None

    Writes info to file
    """
    with open(file, "w", encoding="utf-8") as f:
        x = [str(i+1)+". "+", ".join(info[i]) for i in range(len(info))]
        f.write(name+" "+";".join(i))


def main(loc):
    """
    (str) -> int

    Detect faces on all images in location
    """
    for filename in os.listdir(loc):
        img = cv2.imread(filename)
        write_info(log, filename, find_face(img))
    return 0
