from BerryIMU import IMU
import rocketLogger
import logging

class sensor:

    def __init__(self, logger):
        #logger = rocketLogger()
        IMU.detectIMU()     #Detect if BerryIMU is connected.
        if(IMU.BerryIMUversion == 99):
            logger.debugLog("No IMU detected!", level=logging.WARNING)
        IMU.initIMU() 

    def roundDataValuesToDecimal(self,data, decimal=3):
        roundedData = data
        for item in roundedData:
            item = round(item, decimal)
        return roundedData

    def getSensorData(self):
        #returns finaliozed sensor data
        pass

    def applySensorReadLogic(self):
        """
        Sensor logic defined to retrieve and calibrate raw sensor data, to be called once per logic iteration
        """
        pass

    def getRawSensorData(self):
        """
        Returns raw sensor data in format relevent to particular sensor implementation
        """
        pass

    def applyCalibration(self, data):
        #some code to calibrate data here
        pass

    def convertDataToDeg(self, value):
        #some code to convert data
        return value
