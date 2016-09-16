from bottle import route, run, hook, response, request
from FaceRecognizer import Recognizer, readFrame
import cv2
import time
from collections import Counter
import numpy as np


host = "10.136.23.38"  # Change this to machine IP

@hook('after_request')
def enable_cors():
    response.headers['Access-Control-Allow-Origin'] = '*'

@route('/train')
def train():
    uuid = request.query['uuid']
    print "uuid=>'%s'" % uuid
    if not uuid:
        return "Invalid Action"  # Empty string is False

    uuid = "786"  # hard-coding for now till DB isn't present
    trainMe(uuid)
    return "trained for ", uuid


@route('/predict')
def predict():
    # photos = readFrame(10)
    # if len(photos) != 0:
    #     predicted = faceRecognizer.predict(photos)
    #     data = Counter(predicted)
    #     print "Predicted", data.most_common(1)[0][0]
    # cv2.destroyAllWindows()
    # cv2.destroyAllWindows()
    # p = Process(target=recognizeFace, args=(predicted,))
    # p.start()
    # p.join()
    # print 'Predicted', predicted.value
    predicted = recognizeFace()
    return str(predicted)


file = 'learnedData'
faceRecognizer = Recognizer(file)


def recognizeFace():
    photos = readFrame(10)
    if len(photos) != 0:
        predicted = faceRecognizer.predict(photos)
        data = Counter(predicted)
        print "Predicted", data.most_common(1)[0][0]
        predictedFace = data.most_common(1)[0][0]
    cv2.destroyAllWindows()
    return predictedFace


def trainMe(label):
    photos = readFrame(10)
    # Change the lavel for every learning
    # For face recognition we will the the LBPH Face Recognizer
    label = int(label)
    labels = [label for i in range(len(photos))]

    cv2.namedWindow('face')
    for faces in photos:
        cv2.imshow('face', faces)
        cv2.waitKey(60)
        time.sleep(1)
    # Train
    faceRecognizer.update(photos, np.array(labels))
    cv2.destroyAllWindows()
    print "captured and trained for => " + str(labels)


run(host=host, port=8080, debug=True)
