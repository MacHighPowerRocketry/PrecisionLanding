from Sensors.sensor import sensor
from Sensors.berryAccelerometer import *

import time
import math
from BerryIMU import IMU
import datetime
import os
import sys

M_PI = 3.14159265358979323846


class berryMagnetometer(sensor):
    
    def __init__(self, logger):
        self.logger = logger
        sensor.__init__(self, self.logger)

        ################# Compass Calibration values ############
        # Use calibrateBerryIMU.py to get calibration values
        # Calibrating the compass isnt mandatory, however a calibrated
        # compass will result in a more accurate heading values.
        self.magXmin =  0
        self.magYmin =  0
        self.magZmin =  0
        self.magXmax =  0
        self.magYmax =  0
        self.magZmax =  0

    def applySensorReadLogic(self, pitch, roll):
        """
        Sensor logic defined to retrieve and calibrate raw sensor data, to be called once per logic iteration
        """
        rawSensorData = self.getRawSensorData()
        calibratedSensorData = self.applyCalibration(rawSensorData)
        compensatedTiltValues = self.calculateTiltCompensatedValues(calibratedSensorData, pitch, roll)
        self.heading = self.calculateTiltCompensatedHeading(compensatedTiltValues)

        
    def getSensorData(self):
        #returns tilt heading, compensated by calibrated values
        accelerometer = berryAccelerometer(self.logger)
        self.applySensorReadLogic(accelerometer.getPitch, accelerometer.getRoll)
        return [self.heading]


    def calculateTiltCompensatedHeading(self, data):
        tiltCompensatedHeading = 180 * math.atan2(data[1],data[0])/M_PI
        if tiltCompensatedHeading < 0:
            tiltCompensatedHeading += 360
        return tiltCompensatedHeading

    def calculateTiltCompensatedValues(self, data, pitch, roll):
        """
        Calculate tilt compensated values
        Input: cailbrated sensor data, pitch, roll
        Returns: xComp and yComp as array
        """
        magXcomp = data[0]*math.cos(pitch)+data[2]*math.sin(pitch)
        magYcomp = data[0]*math.sin(roll)*math.sin(pitch)+data[1]*math.cos(roll)-data[2]*math.sin(roll)*math.cos(pitch)
        return [magXcomp, magYcomp]

    def getRawSensorData(self):
        """
        Returns magnetometer x y and z values as array
        """
        MAGx = IMU.readMAGx()
        MAGy = IMU.readMAGy()
        MAGz = IMU.readMAGz()
        return [MAGx, MAGy, MAGz]

    def applyCalibration(self, data):
        mag = data
        mag[0] -= (self.magXmin + self.magXmax) /2
        mag[1] -= (self.magYmin + self.magYmax) /2
        mag[2] -= (self.magZmin + self.magZmax) /2
        return mag

    def toString(self):
        heading = self.roundDataValuesToDecimal(self.getSensorData())
        return "Heading %s "%(self.getSensorData())