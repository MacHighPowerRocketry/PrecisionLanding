from Sensors import sensor
from Sensors.berryAccelerometer import *
from Sensors.berryGyroscope import *
from Sensors.berryMagnetometer import *
from Sensors.pressureSensor import *
from time import sleep
import rocketLogger

logger = rocketLogger.rocketLogger()
logger.dataLog('AccXangle \t AccYangle \t gyroXangle \t gyroYangle \t gyroZangle \t heading  \n ')

accelerometer = berryAccelerometer(logger)
gyroscope = berryGyroscope(logger)
magnetometer = berryMagnetometer(logger)
tempPressureAltitudeSensor = BMP388()

sensors = [accelerometer, gyroscope, magnetometer, tempPressureAltitudeSensor]

def logSensorData():
    for sensor in sensors:
        logger.dataLog(sensor.toString())
    logger.dataLog("\n")
 
def main():
    while True:
        sleep(0.05) #wait 50 miliseconds between data dump
        logSensorData()

if __name__=="__main__":
    main()
