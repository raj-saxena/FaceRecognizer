import cv2
import os
import numpy as np


class Recognizer:
    def __init__(self, fname):
        self.file = fname
        self.recognizer = cv2.face.createLBPHFaceRecognizer()
        if not os.path.isfile(self.file):
            print 'init'
            self.recognizer.save(self.file)
        self.recognizer.load(self.file)

    def update(self, images, labels):
        # images and labels are of type `array`
        self.recognizer.update(images, np.array(labels))
        self.recognizer.save(self.file)

    def predict(self, photos):
        predicted = list()
        for photo in photos:
            # for openCV >= 3.0.0
            # result = cv2.face.MinDistancePredictCollector(20)
            result = cv2.face.MinDistancePredictCollector()
            self.recognizer.predict(photo, result,0)
            nbr_predicted = result.getLabel()
            predicted.append(nbr_predicted)
            conf = result.getDist()
            # print nbr_predicted, "is predicted with distance ", conf
            nbr_predicted2 = self.recognizer.predict(photo)
            # print "nbr_predicted2 ", nbr_predicted2
            # nbr_predicted, conf = self.recognizer.predict(photo)
            nbr_predicted = self.recognizer.predict(photo)
        return predicted
