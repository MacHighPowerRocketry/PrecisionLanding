from Sensors.sensor import sensor

import time
import math
from BerryIMU import IMU
import datetime
import os
import sys

RAD_TO_DEG = 57.29578
M_PI = 3.14159265358979323846


class berryAccelerometer(sensor):

    def __init__(self,logger):
        sensor.__init__(self,logger)

    def applySensorReadLogic(self):
        rawSensorData = self.getRawSensorData()
        convertedSensorData = self.convertDataToDeg(rawSensorData)
        calibratedSensorData =  self.applyCalibration(convertedSensorData)
        self.callibratedAccYangle = calibratedSensorData[1]
        self.callibratedAccXangle = calibratedSensorData[0]
        data = [self.callibratedAccXangle, self.callibratedAccYangle]
        self.normalizeData(data)
    
    def getSensorData(self):
        #returns finalized sensor data for use outside class
        self.applySensorReadLogic()
        return [self.callibratedAccYangle, self.callibratedAccXangle]

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

    
    def normalizeData(self,data):
        ACCx = data[0]
        ACCy = data[1]
        ACCz = IMU.readACCz()
        self.accXnorm = ACCx/math.sqrt(ACCx * ACCx + ACCy * ACCy + ACCz * ACCz)
        self.accYnorm = ACCy/math.sqrt(ACCx * ACCx + ACCy * ACCy + ACCz * ACCz)

    def getNormalizedData(self):
        return [self.accXnorm, self.accYnorm]

    def getPitch(self):
        return math.asin(self.accXnorm)

    def getRoll(self):
        return -math.asin(self.accYnorm/math.cos(self.getPitch()))

    def toString(self):
        x,y = self.getSensorData()
        return "Pitch %s Roll %s Accelerometer X Angle %s Acceleromter Y Angle %s" % (self.getPitch(), self.getRoll(), x, y)
