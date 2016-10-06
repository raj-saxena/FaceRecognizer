import serial
import re
import time
import httplib, urllib, ssl
from JsonExtractor import *
from BahmniServerHelper import BahmniServerHelper
# from HttpServer import host, port
import HttpServer
import RecordsUpdater
from TemperatureSensor import TemperatureSensor

port = "/dev/cu.usbmodem1421"
baudRate = 9600
# userName = "superman"
# password = "Admin123"

print "Monitoring temperature"

serialInput = serial.Serial(port, baudRate)

temperatureSensor = TemperatureSensor(serialInput)
temperatureSensor.setTemperature()

#
# thresholdValue = 90
#
#
# def getAbsoluteTemperatureFromSerial():
#     valueRead = re.findall("\d+\.\d+", ser.readline())
#     return float(valueRead[0]) if len(valueRead) else 0
#
#
# def getAverageValue():
#     readings = []
#     for i in range(1, 11):
#         readings.append(getAbsoluteTemperatureFromSerial())
#     return round(reduce(lambda x, y: x + y, readings) / float(len(readings)), 2)


# def recognizePatientAndUpdateObservation(key, avgValue):
#     print "Firing request to recognize patient"
#     # print HttpServer.host,HttpServer.port
#     conn = httplib.HTTPConnection(HttpServer.host, HttpServer.port)
#     # print conn
#     conn.request("GET", "/predict")
#     resp = conn.getresponse()
#     result = resp.read()
#     print resp.status, resp.reason, result, avgValue
#     conn.close()
#
#     uuid = result.split()[2]
#
#     payload = setObservationValue(uuid, key, avgValue)
#     print "Saving in Bahmni =>", uuid, avgValue,  # , "=>", payload
#     # print payload
#     headers = {"Content-type": "application/json;charset=UTF-8",
#                'Cookie': BahmniServerHelper().getAuthenticatedCookie(userName, password)}
#     # print headers
#     conn = httplib.HTTPSConnection("192.168.33.10", context=ssl._create_unverified_context())
#     conn.request("POST", "/openmrs/ws/rest/v1/bahmnicore/bahmniencounter", payload, headers)
#     response = conn.getresponse()
#     respBody = response.read()
#     # print respBody
#     print "Response => ", response.status  # , "=>", respBody
#     conn.close()
#     # print "saved in Bahmni"
#     time.sleep(3)


# recognizePatientAndUpdateObservation('Temperature', 25)
#
# while True:
#     value = getAbsoluteTemperatureFromSerial()
#     isValid = value > thresholdValue
#     if isValid:
#         print "calculating avg temp =>"
#         avgValue = getAverageValue()
#         print avgValue
#         recordsUpdater = RecordsUpdater.RecordsUpdater()
#         recordsUpdater.updateLatestRecords('Temperature', avgValue)
#         # recognizePatientAndUpdateObservation('Temperature', avgValue)
#         isValid = False
#         value = getAbsoluteTemperatureFromSerial()
#         while value > thresholdValue:
#             print "Resetting sensor temperature, current=>%.2f" % value
#             time.sleep(3)
#             value = getAbsoluteTemperatureFromSerial()
#     else:
#         print "value=%.2fF smaller than threshold." % value
#
#     time.sleep(2)
