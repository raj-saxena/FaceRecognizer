import re
import time
import serial
from RecordsUpdater import RecordsUpdater

class TemperatureSensor:
    def __init__(self, serialInput):
        self.__serialInput = serialInput
        self.__thresholdValue = 90

    def setTemperature(self):
        while True:
            temperature = self.getAbsoluteTemperatureFromSerial()
            self.__isValid = temperature > self.__thresholdValue
            if self.__isValid:
                self.addTemperature()
                temperature = self.getAbsoluteTemperatureFromSerial()
                while temperature > self.__thresholdValue:
                    self.consoleOutput("Resetting sensor temperature, current=>%.2f" % temperature)
                    time.sleep(3)
                    temperature = self.getAbsoluteTemperatureFromSerial()

            else:
                self.consoleOutput("value=%.2fF smaller than threshold." % temperature)

    def addTemperature(self):
        self.consoleOutput("calculating avg temp =>")
        averageTemperature = self.getAverageTemperatureValue()
        self.consoleOutput(averageTemperature)
        recordsUpdater = RecordsUpdater()
        recordsUpdater.updateLatestRecords('Temperature', averageTemperature)
        self.__isValid = False
        time.sleep(2)

    def getAverageTemperatureValue(self):
        readings = []
        for i in range(10):
            readings.append(self.getAbsoluteTemperatureFromSerial())
        return round(reduce(lambda x, y: x + y, readings) / float(len(readings)), 2)

    def getAbsoluteTemperatureFromSerial(self):
        temperature = re.findall("\d+\.\d+", self.__serialInput.readline())
        if (len(temperature)):
            return float(temperature[0])
        return 0

    def consoleOutput(self, message):
        print message

temperatureSensor = TemperatureSensor(serial.Serial("/dev/cu.usbmodem1421", 9600))
temperatureSensor.setTemperature()
