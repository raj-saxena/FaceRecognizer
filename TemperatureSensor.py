import re
import time
import serial
from RecordsUpdater import RecordsUpdater

from Values import SERIAL_PORT
from Values import BAUD_RATE


class TemperatureSensor:
    def __init__(self, serialInput):
        self.__serialInput = serialInput
        self.__thresholdValue = 90

    def read(self):
        while True:
            temperature = self.getAbsoluteTemperatureFromSerial()
            self.__isValid = temperature > self.__thresholdValue
            if self.__isValid:
                self.update()
                self.reset()
            else:
                self.consoleOutput("value=%.2fF smaller than threshold." % temperature)

    def getAbsoluteTemperatureFromSerial(self):
        temperature = re.findall("\d+\.\d+", self.__serialInput.readline())
        if (len(temperature)):
            return float(temperature[0])
        return 0

    def update(self):
        self.consoleOutput("calculating avg temp =>")
        averageTemperature = self.getAverageValue()
        self.consoleOutput(averageTemperature)
        recordsUpdater = RecordsUpdater()
        recordsUpdater.update('Temperature', averageTemperature)
        self.__isValid = False
        time.sleep(3)

    def getAverageValue(self):
        readings = []
        for i in range(10):
            readings.append(self.getAbsoluteTemperatureFromSerial())
        return round(reduce(lambda x, y: x + y, readings) / float(len(readings)), 2)

    def reset(self):
        temperature = self.getAbsoluteTemperatureFromSerial()
        while temperature > self.__thresholdValue:
            self.consoleOutput("Resetting sensor temperature, current=>%.2f" % temperature)
            time.sleep(3)
            temperature = self.getAbsoluteTemperatureFromSerial()

    def consoleOutput(self, message):
        print message


temperatureSensor = TemperatureSensor(serial.Serial(SERIAL_PORT, BAUD_RATE))
temperatureSensor.read()
