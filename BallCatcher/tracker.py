import cv2
import time


class ObjectTracker():
    def __init__(self, tracker):
        self.tracker = tracker
        self.face_cascade = cv2.CascadeClassifier(tracker)
        self.previous_success = (0, 0)
        self.all_faces = []
        self.all_faces_area = []
        self.res = (0, 0)

    def start_web_cam(self, id=0):
        self.cap = cv2.VideoCapture(id)

    def find_matches(self):
        self.all_faces=[]
        self.all_area =[]

        ret, self.img = self.cap.read()
        gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:

            self.all_faces.append([(x, y), (x+w, y+h), (w, h), w*h])
            self.all_faces_area.append(w*h)

    def find_nearest(self):
        biggest = list(
            filter(lambda x: x[3] == max(self.all_faces_area), self.all_faces))

        if biggest:
            self.previous_success = (
                biggest[0][0][0]+biggest[0][2][0]//2, biggest[0][0][1]+biggest[0][2][1]//2)

        self.res = (biggest[0][0][0]+biggest[0][2][0]//2, biggest[0]
                    [0][1]+biggest[0][2][1]//2) if biggest else self.previous_success

    def show_processing(self):
        cv2.circle(self.img, (self.res[0], self.res[1]), 10, (0, 0, 255), -1)
        # cv2.rectangle(self.img, biggest[0][0], biggest[0][1], (0, 255, 0), 2)

        for i in self.all_faces:
            cv2.rectangle(self.img, i[0], i[1], (255, 0, 0), 2)

        cv2.imshow('img', self.img)



x = ObjectTracker('haarcascade_frontalface_default.xml')
x.start_web_cam()

while True:
    x.find_matches()
    x.find_nearest()
    x.show_processing()
    cv2.waitKey(25)
    # print(x.res)


# face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
# # face_cascade = cv2.CascadeClassifier('closed_frontal_palm.xml')
# # face_cascade = cv2.CascadeClassifier('cascade.xml')

# cap = cv2.VideoCapture(0)

# def kek():
#     global previous_success
#     ret, img = cap.read()

#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     faces = face_cascade.detectMultiScale(gray, 1.3, 5)
#     res, res_m = [], []
#     for (x, y, w, h) in faces:
#         cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

#         res.append([(x, y), (x+w, y+h),(w,h), w*h])
#         res_m.append(w*h)

#     biggest = list(filter(lambda x: x[3] == max(res_m), res))
#     # print(biggest)
#     # print(biggest[0][0][0]+biggest[0][2][0]//2)
#     if biggest:
#         cv2.circle(img, (biggest[0][0][0]+biggest[0][2][0]//2, biggest[0][0][1]+biggest[0][2][1]//2), 10, (0, 0, 255), -1)
#         cv2.rectangle(img, biggest[0][0], biggest[0][1], (0, 255, 0), 2)
#         previous_success=biggest[0][0][0]+biggest[0][2][0]//2
#         # last_success=previous_success
#     # else:
#         # last_success=previous_success

#     cv2.imshow('img', img)
#     cv2.waitKey(25)
#     return biggest[0][0][0]+biggest[0][2][0]//2 if biggest else previous_success

# while True:
#     kek()
