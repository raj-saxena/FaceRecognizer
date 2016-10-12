import httplib
import ssl

from BahmniServerHelper import BahmniServerHelper
from JsonExtractor import *

from Values import HOST_IP
from Values import HOST_PORT

class RecordsUpdater:
    def __init__(self):
        self.__userName = "superman"
        self.__password = "Admin123"

    def update(self, key, value):
        uuid = self.getUUIDOfPatient()
        if uuid == -1:
            return
        payload = setObservationValue(uuid, key, value)
        self.consoleOutput("Saving in Bahmni => " + str(uuid) + " " + str(value))
        headers = {"Content-type": "application/json;charset=UTF-8",
                   'Cookie': BahmniServerHelper().getAuthenticatedCookie(self.__userName, self.__password)}
        httpsConnection = httplib.HTTPSConnection("192.168.33.10", context=ssl._create_unverified_context())
        httpsConnection.request("POST", "/openmrs/ws/rest/v1/bahmnicore/bahmniencounter", payload, headers)
        self.consoleOutput("Response => " + str(httpsConnection.getresponse().status))
        httpsConnection.close()

    def getUUIDOfPatient(self):
        self.consoleOutput("Firing request to recognize patient")
        httpConnection = httplib.HTTPConnection(HOST_IP, HOST_PORT)
        httpConnection.request("GET", "/predict")
        httpResponse = httpConnection.getresponse()
        result = httpResponse.read()
        httpConnection.close()
        self.consoleOutput(result)
        if result == "UnRegistered":
            #call trained method again to get patient face #dont delete this comment
            return -1
        return result.split()[2]

    def consoleOutput(self, message):
        print message
