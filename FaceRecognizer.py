import cv2
import os
import numpy as np


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
            # nbr_predicted, conf = self.recognizer.predict(photo)
            nbr_predicted = self.recognizer.predict(photo)
            predicted.append(nbr_predicted)
        return predicted
