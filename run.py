from Sensors import *
from time import sleep
import rocketLogger

logger = rocketLogger.rocketLogger()
logger.dataLog('AccXangle \t AccYangle \t gyroXangle \t gyroYangle \t gyroZangle \t heading \t temp \t pressure \t altitude \t gps \n ')


accelerometer = berryAccelerometer.berryAccelerometer(logger)
gyroscope = berryGyroscope.berryGyroscope(logger)
magnetometer = berryMagnetometer.berryMagnetometer(logger, accelerometer)
tempPressureAltitudeSensor = pressureSensor.pressureSensor(logger)
gps = berryGPS.berryGPS(logger)

#sensors = [accelerometer, gyroscope, magnetometer, tempPressureAltitudeSensor, gps]
print("Finished loading sensors")

sensors = [accelerometer,gyroscope,magnetometer]
def logSensorData():
    for sensor in sensors:
        logger.dataLog(sensor.toString())
    logger.dataLog("\n")

 
def main():
    while True:
        sleep(0.5) #wait 50 miliseconds between data dump
        logSensorData()

if __name__=="__main__":
    main()
