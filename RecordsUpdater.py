import httplib
import ssl
import time

from BahmniServerHelper import BahmniServerHelper
from JsonExtractor import *

import HttpServer

class RecordsUpdater:
    def __init__(self):
        self.__userName = "superman"
        self.__password = "Admin123"

    def updateLatestRecords(self, key, value):
        uuid = self.getUUIDOfPatient()
        payload = setObservationValue(uuid, key, value)
        self.consoleOutput("Saving in Bahmni => " + str(uuid) + " " + str(value))
        headers = {"Content-type": "application/json;charset=UTF-8",
                   'Cookie': BahmniServerHelper().getAuthenticatedCookie(self.__userName, self.__password)}
        httpsConnection = httplib.HTTPSConnection("192.168.33.10", context=ssl._create_unverified_context())
        httpsConnection.request("POST", "/openmrs/ws/rest/v1/bahmnicore/bahmniencounter", payload, headers)
        self.consoleOutput("Response => " + str(httpsConnection.getresponse().status))
        httpsConnection.close()
        time.sleep(3)

    def getUUIDOfPatient(self):
        self.consoleOutput("Firing request to recognize patient")
        httpConnection = httplib.HTTPConnection(HttpServer.host, HttpServer.port)
        httpConnection.request("GET", "/predict")
        httpResponse = httpConnection.getresponse()
        result = httpResponse.read()
        httpConnection.close()
        self.consoleOutput(result)
        return result.split()[2]

    def consoleOutput(self, message):
        print message
