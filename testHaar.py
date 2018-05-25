import numpy as np
import cv2

# multiple cascades: https://github.com/Itseez/opencv/tree/master/data/haarcascades

# https://github.com/Itseez/opencv/blob/master/data/haarcascades/haarcascade_frontalface_default.xml
# face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
# face_cascade = cv2.CascadeClassifier('open_palm.xml')
# https://github.com/Itseez/opencv/blob/master/data/haarcascades/haarcascade_eye.xml
# eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

cap = cv2.VideoCapture(0)


def kek():
    ret, img = cap.read()

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    res, res_m = [], []
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

        res.append([(x, y), (x+w, y+h),(w,h), w*h])
        res_m.append(w*h)

    biggest = list(filter(lambda x: x[3] == max(res_m), res))
    # print(biggest)
    # print(biggest[0][0][0]+biggest[0][2][0]//2)
    if biggest:
        cv2.circle(img, (biggest[0][0][0]+biggest[0][2][0]//2, biggest[0][0][1]+biggest[0][2][1]//2), 10, (0, 0, 255), -1)
        cv2.rectangle(img, biggest[0][0], biggest[0][1], (0, 255, 0), 2)


    cv2.imshow('img', img)
    k = cv2.waitKey(30) & 0xff
    return biggest[0][0][0]+biggest[0][2][0]//2 if biggest else 0


while 1:
    kek()

