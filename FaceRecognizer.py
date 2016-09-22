import os
from collections import Counter

import cv2
import numpy as np
import time

cascPath = "/usr/local/Cellar/opencv/2.4.13/share/OpenCV/haarcascades/haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)


def getBigRectangle(faces):
    return max(faces, key=lambda (x, y, w, h): w * h)


def readFrame(Time=20, Interval=2):
    camera = cv2.VideoCapture(0)
    cv2.namedWindow('Video', cv2.WINDOW_NORMAL)
    cv2.startWindowThread()

    facePhoto = list()
    interval_start = start = time.time()

    while True:
        isFrameReadCorrectly, frame = camera.read()

        # if isFrameReadCorrectly:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detectFacesInVideo(gray)

        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            # Display the resulting frame
            cv2.imshow('Video', frame)
            cv2.waitKey(60)

        if time.time() - interval_start >= Interval:
            print "faces detected => ", len(faces)
            if len(faces) != 0:
                (x, y, w, h) = getBigRectangle(faces)
                facePhoto.append(gray[y:y + h, x:x + w])
                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    # Display the resulting frame
                    cv2.imshow('frame', frame)
                    cv2.waitKey(200)
            interval_start = time.time()

        if time.time() - start >= Time: break
    cv2.destroyAllWindows()
    cv2.waitKey(1)
    camera.release()
    return facePhoto


def detectFacesInVideo(gray):
    return faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(100, 100),
        flags=cv2.CASCADE_SCALE_IMAGE
    )


class Recognizer:
    def __init__(self, fname):
        self.file = fname
        self.recognizer = cv2.face.createLBPHFaceRecognizer()
        if not os.path.isfile(self.file):
            print 'init'
            self.recognizer.save(fname)
        self.recognizer.load(fname)

    def update(self, images, labels):
        self.recognizer.update(images, np.array(labels))
        self.recognizer.save(self.file)

    def predict(self, photos):
        self.recognizer.load(self.file)
        predicted = list()
        for photo in photos:
            nbr_predicted = self.recognizer.predict(photo)
            predicted.append(nbr_predicted)
        return predicted


if __name__ == '__main__':
    file = 'learnedData'
    faceRecognizer = Recognizer(file)
    mode = 1
    if not mode:  # Train
        photos = readFrame(10)
        # Change the lavel for every learning
        label = 02
        # For face recognition we will the the LBPH Face Recognizer
        labels = [label for i in range(len(photos))]
        print labels

        cv2.namedWindow('face')
        print len(photos)
        for faces in photos:
            cv2.imshow('face', faces)
            cv2.waitKey(60)
            time.sleep(1)
        # Train
        faceRecognizer.update(photos, np.array(labels))
        cv2.namedWindow('face')

    else:  # predict
        photos = readFrame(10)
        if len(photos) != 0:
            predicted = faceRecognizer.predict(photos)
            data = Counter(predicted)
            print "Predicted", data.most_common(1)[0][0]
