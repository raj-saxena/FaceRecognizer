import serial
import re
import time

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


def recognizePatientAndUpdateObservation(avgValue): pass


while True:
    value = getAbsoluteTemperatureFromSerial()
    isValid = value > threshold
    if isValid:
        print "calculating avg temp =>"
        avgValue = getAverageValue()
        print avgValue
        recognizePatientAndUpdateObservation(avgValue)
    else :
        print "value=%.2f smaller than threshold." % value

    time.sleep(2)
