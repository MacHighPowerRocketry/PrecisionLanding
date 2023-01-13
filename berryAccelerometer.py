import sensor

import time
import math
from BerryIMU import IMU
import datetime
import os
import sys

RAD_TO_DEG = 57.29578
M_PI = 3.14159265358979323846


class berryAccelerometer(sensor):

    def __init__(self):
        sensor.__init__(self)

    def applySensorReadLogic(self):
        rawSensorData = getRawSensorData()
        convertedSensorData = convertDataToDeg(rawSensorData)
        calibratedSensorData = applyCalibration(convertedSensorData)
        self.callibratedAccYangle = calibratedSensorData[1]
        self.callibratedAccXangle = calibratedSensorData[0]
    
    def getSensorData(self):
        #returns finalized sensor data for use outside class
        return [self.callibratedAccYangle. self.callibratedAccXangle]

    def getRawSensorData(self):
        """
        gets raw accelerameter data from IMU sensor and returns as array
        """
        ACCx = IMU.readACCx()
        ACCy = IMU.readACCy()
        ACCz = IMU.readACCz()
        data = [ACCx,ACCy,ACCz]
        return data

    def applyCalibration(self, data):
        """
        Calibrates raw sensor data and returns value as array
        """
        AccXangle = data[0]
        AccYangle = data[1]
        #convert the values to -180 and +180
        if AccYangle > 90:
            AccYangle -= 270.0
        else:
            AccYangle += 90.0
        calibratedSensorData = [AccXangle, AccYangle]
        return calibratedSensorData

    def convertDataToDeg(self, data):
        """
        Converts sensor data to degree and returns as array
        """
        AccXangle =  (math.atan2(data[1],data[2])*RAD_TO_DEG)
        AccYangle =  (math.atan2(data[2],data[0])+M_PI)*RAD_TO_DEG

        convertedSensorData = [AccXangle, AccYangle]
        return convertedSensorData

    def normalizeData(self):
        self.accXnorm = ACCx/math.sqrt(ACCx * ACCx + ACCy * ACCy + ACCz * ACCz)
        self.accYnorm = ACCy/math.sqrt(ACCx * ACCx + ACCy * ACCy + ACCz * ACCz)

    def getNormalizedData(self):
        return [self.accXnorm, self.accYnorm]
