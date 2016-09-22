import time
from collections import Counter

import cv2
import numpy as np
from bottle import route, run, hook, response, request

from DB import DB
import sqlite3
from FaceRecognizer import Recognizer, readFrame

host = "10.136.20.77"  # Change this to machine IP
port = 8080


@hook('after_request')
def enable_cors():
    response.headers['Access-Control-Allow-Origin'] = '*'


db = DB()


@route('/train')
def train():
    uuid = request.query['uuid']
    print "uuid=>'%s'" % uuid
    if not uuid:
        return "Invalid Action"  # Empty string is False
    try:
        mappedId = db.add(uuid)
        trainForFace(mappedId)
        return "Trained for %s => %s " % uuid, mappedId
    except sqlite3.IntegrityError:
        print "User with uuid=%s already exists, initiating re-training."
        mappedId = db.getId(uuid)
        trainForFace(mappedId)
        return "I Know You"


@route('/predict')
def predict():
    predictedId = recognizeFace()
    result = getUUID(predictedId)

    print 'result', result
    if result is not None:
        returnString = "You are %s" % (result[0],)
        return returnString
    return "Unable to Recognize You"


def getUUID(predictedId):
    result = db.getUuid(predictedId)
    return result


file = 'learnedData.yml'
faceRecognizer = Recognizer(file)


def recognizeFace():
    predictedFace = None
    photos = readFrame(10)
    if len(photos) != 0:
        predicted = faceRecognizer.predict(photos)
        data = Counter(predicted)
        print "Predicted", data.most_common(1)[0][0]
        predictedFace = data.most_common(1)[0][0]
    cv2.destroyAllWindows()
    return predictedFace


def trainForFace(label):
    photos = readFrame(10)
    # For face recognition we will the the LBPH Face Recognizer
    # label = int(label)
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


run(host=host, port=port, debug=True)
