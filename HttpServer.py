from bottle import route, run, hook, response, request
from FaceProcessor import recognizeFace, trainForFace
from multiprocessing import Process, Manager

from DB import DB
import sqlite3

host = "10.136.22.231"  # Change this to machine IP
port = 8080
db = DB()


@hook('after_request')
def enable_cors():
    response.headers['Access-Control-Allow-Origin'] = '*'


@route('/train')
def train():
    uuid = request.query['uuid']
    print "uuid=>'%s'" % uuid
    if not uuid:
        return "Invalid Action"  # Empty string is False
    try:
        mappedId = db.add(uuid)
        p = Process(target=trainForFace, args=(mappedId,))
        p.start()
        return "Trained for " + uuid + " =>" + str(mappedId)
    except sqlite3.IntegrityError:
        print "User with uuid=%s already exists,"  # initiating re-training."
        return "I Know You"


@route('/predict')
def predict():
    predicted = Manager().Value('i', 0)
    p = Process(target=recognizeFace, args=(predicted,))
    p.start()
    p.join()

    predictedId = predicted.value
    result = db.getUuid(predictedId)

    print 'result', result
    if result is not None:
        returnString = "You are %s" % (result[0],)
        return returnString
    return "UnRegistered"


if __name__ == '__main__':
    run(host=host, port=port, debug=True)
