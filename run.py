from Sensors import sensor
from Sensors.berryAccelerometer import *
from Sensors.berryGyroscope import *
from Sensors.berryMagnetometer import *
import rocketLogger

logger = rocketLogger.rocketLogger()
logger.dataLog('AccXangle \t AccYangle \t gyroXangle \t gyroYangle \t gyroZangle \t heading  \n ')
accelerometer = berryAccelerometer(logger)
gyroscope = berryGyroscope(logger)
magnetometer = berryMagnetometer(logger)

def manageSensors():
    callSensorLogics()
    logSensorData()

def callSensorLogics():
    #add sensor logic calls here
    accelerometer.applySensorReadLogic()
    gyroscope.applySensorReadLogic()
    magnetometer.applySensorReadLogic(accelerometer.getPitch(), accelerometer.getRoll())

def logSensorData():
    logger.dataLog(str(accelerometer.getSensorData()[0]) + 
                " " + str(accelerometer.getSensorData()[1]) + 
                " " + str(gyroscope.getSensorData()[0]) +
                " " + str(gyroscope.getSensorData()[1]) + 
                " " + str(magnetometer.getSensorData()) + "/n")
    

def main():
    while True:
        manageSensors()

if __name__=="__main__":
    main()
