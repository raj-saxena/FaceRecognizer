from bottle import route, run, hook, response, request
from FaceRecognizer import Recognizer, readFrame
import cv2
import time
from collections import Counter
import numpy as np
import sqlite3

connection = sqlite3.connect('FaceRecognizer.db')
dbCursor = connection.cursor()


host = "10.136.23.38"  # Change this to machine IP

@hook('after_request')
def enable_cors():
    response.headers['Access-Control-Allow-Origin'] = '*'

@route('/train')
def train():

    dbCursor.execute("CREATE TABLE IF NOT EXISTS users( mapped_id INTEGER PRIMARY KEY AUTOINCREMENT,uuid TEXT NOT NULL UNIQUE );")

    uuid = request.query['uuid']
    print "uuid=>'%s'" % uuid
    if not uuid:
        return "Invalid Action"  # Empty string is False

    try:
        dbCursor.execute("INSERT INTO users(uuid) values(?)", (uuid,))
        dbCursor.execute("SELECT mapped_id FROM users WHERE uuid = ?", (uuid,))
        mapped_id = dbCursor.fetchone()[0]
        connection.commit()
        print mapped_id
        trainMe(mapped_id)
        #p = Process(target=trainMe, args=(mapped_id,))
        #p.start()
        return "trained"
    except sqlite3.IntegrityError:
        return "I Know You"

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
    dbCursor.execute("SELECT uuid FROM users WHERE mapped_id = ?", (predicted,))
    result = dbCursor.fetchone()

    print 'result',result
    if result is not None:
        returnString = "You are %s" % (result[0],)
        return returnString
    return "Unable to Recognize You"



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
    #label = int(label)
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
