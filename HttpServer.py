from bottle import route, run, hook, response, request
from FaceProcessor import recognizeFace, trainForFace
import sqlite3

from Constants import HOST_IP
from Constants import HOST_PORT
from Constants import DataBase


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
        mappedId = DataBase.add(uuid)
        trainForFace(mappedId)
        return "Trained for " + uuid + " =>" + str(mappedId)
    except sqlite3.IntegrityError:
        print "User with uuid=%s already exists,"  # initiating re-training."
        return "I Know You"


@route('/predict')
def predict():
    predictedId = recognizeFace()
    # if predictedId==0:
    #     return "UnRegistered"
    result = DataBase.getUuid(predictedId)

    print 'result', result
    if result is not None:
        returnString = "You are %s" % (result[0],)
        return returnString
    return "UnRegistered"



if __name__ == '__main__':
    run(host=HOST_IP, port=HOST_PORT, debug=True)
