import serial
import re
import time
import httplib, urllib, ssl
from JsonExtractor import *
from BahmniServerHelper import BahmniServerHelper
from HttpServer import host, port

port = "/dev/cu.usbmodem1421"
baudRate = 9600

threshold = 32
uname = "superman"
pswd = "Admin123"

print "Monitoring temperature"

ser = None  # serial.Serial(port, baudRate)


def getAbsoluteTemperatureFromSerial():
    valueRead = re.findall("\d+\.\d+", ser.readline())
    return float(valueRead[0]) if len(valueRead) else 0


def getAverageValue():
    readings = []
    for i in range(1, 11):
        readings.append(getAbsoluteTemperatureFromSerial())
    return reduce(lambda x, y: x + y, readings) / float(len(readings))


def recognizePatientAndUpdateObservation(key, avgValue):
    print "Firing request to recognize patient"
    conn = httplib.HTTPConnection(host, port)
    conn.request("GET", "/predict")
    resp = conn.getresponse()
    result = resp.read()
    print resp.status, resp.reason, result
    conn.close()

    uuid = "2e9be152-992e-4a07-844f-357d55c59de3"

    payload = setObservationValue(uuid, key, avgValue, payloadTemperature)
    print "Saving in Bahmni =>", uuid, "=>", payload
    # print payload
    headers = {"Content-type": "application/json;charset=UTF-8",
               'Cookie': BahmniServerHelper().getAuthenticatedCookie(uname, pswd)}
    # print headers
    conn = httplib.HTTPSConnection("192.168.33.10", context=ssl._create_unverified_context())
    conn.request("POST", "/openmrs/ws/rest/v1/bahmnicore/bahmniencounter", payload, headers)
    response = conn.getresponse()
    respBody = response.read()
    # print respBody
    print "Response => ", response.status, "=>", respBody
    conn.close()
    # print "saved in Bahmni"
    time.sleep(3)


recognizePatientAndUpdateObservation('Temperature', 102)


while False:
    value = getAbsoluteTemperatureFromSerial()
    isValid = value > threshold
    if isValid:
        print "calculating avg temp =>"
        avgValue = getAverageValue()
        print avgValue
        recognizePatientAndUpdateObservation(avgValue)
        isValid = False
        value = getAbsoluteTemperatureFromSerial()
        while value > threshold:
            print "Resetting sensor temperature, current=>%.2f" % value
            time.sleep(3)
            value = getAbsoluteTemperatureFromSerial()
    else:
        print "value=%.2f smaller than threshold." % value

    time.sleep(2)


