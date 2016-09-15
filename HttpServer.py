from bottle import route, run
from FaceRecognizer import Recognizer, readFrame
import cv2
import time
from collections import Counter
import numpy as np
from multiprocessing import Process, Manager


@route('/train/<label>')
def train(label=None):
    if label is None: return "Invalid Action"
    # trainMe(int(label))
    # p = Process(target=trainMe, args=(int(label),)).start()
    # photos = readFrame(10)
    # # Change the lavel for every learning
    # # For face recognition we will the the LBPH Face Recognizer
    # label = int(label)
    # labels = [label for i in range(len(photos))]
    # print labels
    #
    # cv2.namedWindow('face')
    # print len(photos)
    # for faces in photos:
    #     cv2.imshow('face', faces)
    #     cv2.waitKey(60)
    #     time.sleep(1)
    # # Train
    # faceRecognizer.update(photos, np.array(labels))
    # cv2.destroyAllWindows()
    # cv2.destroyAllWindows()
    trainMe(9)
    return "trained"


@route('/predict/')
def predict():
    # photos = readFrame(10)
    # if len(photos) != 0:
    #     predicted = faceRecognizer.predict(photos)
    #     data = Counter(predicted)
    #     print "Predicted", data.most_common(1)[0][0]
    # cv2.destroyAllWindows()
    # cv2.destroyAllWindows()
    predicted = Manager().Value('i', 0)
    # p = Process(target=recognizeFace, args=(predicted,))
    # p.start()
    # p.join()
    # print 'Predicted', predicted.value
    recognizeFace(predicted)
    result = "predicted %d" % predicted.value
    return result


file = 'learnedData'
faceRecognizer = Recognizer(file)


def recognizeFace(predict):
    photos = readFrame(10)
    predict.value = 0
    if len(photos) != 0:
        predicted = faceRecognizer.predict(photos)
        data = Counter(predicted)
        print "Predicted", data.most_common(1)[0][0]
        predict.value = data.most_common(1)[0][0]
    cv2.destroyAllWindows()
    return predict


def trainMe(label):
    photos = readFrame(10)
    # Change the lavel for every learning
    # For face recognition we will the the LBPH Face Recognizer
    label = int(label)
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
    cv2.destroyAllWindows()


run(host='localhost', port=8080, debug=True)
