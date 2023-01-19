import sensor

import time
import math
from BerryIMU import IMU
import datetime
import os
import sys

G_GAIN = 0.070  # [deg/s/LSB]  If you change the dps for gyro, you need to update this value accordingly
AA =  0.40

class berryGyroscope(sensor):

    def __init__(self):
        sensor.__init__(self)
        self.timeA = datetime.datetime.now() 
        self.gyroXangle = 0.0
        self.gyroYangle = 0.0
        self.gyroZangle = 0.0
        self.CFangleX = 0.0
        self.CFangleY = 0.0

    def applySensorReadLogic(self):
        """
        Sensor logic defined to retrieve and calibrate raw sensor data, to be called once per logic iteration
        """
        rawSensorData = self.getRawSensorData()
        self.calculateLP()
        convertedSensorData = self.convertDataToDeg(rawSensorData)
        self.applyCalibration(convertedSensorData)


    def getRawSensorData(self):
        """
        Returns raw sensor data in format relevent to particular sensor implementation
        """
        GYRx = IMU.readGYRx()
        GYRy = IMU.readGYRy()
        GYRz = IMU.readGYRz()
        data = [GYRx, GYRy, GYRz]
        return data

    def calculateLP(self):
        """
        Calculate loop Period(LP). How long between Gyro Reads

        """
        self.timeB = datetime.datetime.now() - self.timeA
        self.timeA = datetime.datetime.now()
        self.LP = self.timeB.microseconds/(1000000*1.0)
        
    def applyFilter(self, gyroxy, loopPeriod, accxy):
        self.CFangleX=AA*(self.CFangleX+gyroxy[0]*self.LP) +(1 - AA) * accxy[0]
        self.CFangleY=AA*(self.CFangleY+gyroxy[1]*self.LP) +(1 - AA) * accxy[1]

    def applyCalibration(self, data);
        #Apply calibration to generate finalized gyro angle data
        x,y,z = data
        self.gyroXangle+=x*self.LP
        self.gyroYangle+=y*self.LP
        self.gyroZangle+=z*self.LP

    def convertDataToDeg(self, data):
        #convert gyro data to degrees, returns converted data
        GYRx, GYRy, GYRz = data
        rate_gyr_x =  GYRx * G_GAIN
        rate_gyr_y =  GYRy * G_GAIN
        rate_gyr_z =  GYRz * G_GAIN
        convertedSensorData = [rate_gyr_x, rate_gyr_y, rate_gyr_z]
        return convertedSensorData

    def getSensorData(self):
        return [self.gyroXangle, self.gyroYangle, self.gyroZangle]


