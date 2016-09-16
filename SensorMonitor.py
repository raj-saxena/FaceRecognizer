import serial
import re
import time
import httplib

port = "/dev/cu.usbmodem1421"
baudRate = 9600

threshold = 32

print "Monitoring temperature"

ser = serial.Serial(port, baudRate)


def getAbsoluteTemperatureFromSerial():
    valueRead = re.findall("\d+\.\d+", ser.readline())
    return float(valueRead[0]) if len(valueRead) else 0


def getAverageValue():
    readings = []
    for i in range(1, 11):
        readings.append(getAbsoluteTemperatureFromSerial())
    return reduce(lambda x, y: x + y, readings) / float(len(readings))


def recognizePatientAndUpdateObservation(avgValue):
    print "Firing request to recognize patient"
    conn = httplib.HTTPConnection('localhost', 8080)
    conn.request("GET", "/predict")
    resp = conn.getresponse()
    result = resp.read()
    print resp.status, resp.reason, result
    conn.close()
    print "Saving in Bahmni =>"

    #conn = httplib.HTTPConnection("https://192.168.33.10/openmrs/ws/rest/v1/bahmnicore/bahmniencounter")
    time.sleep(5)


while True:
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


